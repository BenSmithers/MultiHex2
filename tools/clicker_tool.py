
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent, QMainWindow, QApplication
from PyQt5.QtWidgets import QGraphicsItem

from MultiHex2.core.core import DRAWSIZE
from MultiHex2.core import Catalog, RegionCatalog
from MultiHex2.core import Hex, HexID, Region
from MultiHex2.core import screen_to_hex
from MultiHex2.actions import ActionManager
from MultiHex2.tools.basic_tool import Basic_Tool
from MultiHex2.tools.regiontools import RegionAdd
from actions.baseactions import NullAction
from core.coordinates import hex_to_screen

import json
from collections import deque
from math import inf
import numpy as np

DEBUG = True

class Clicker(QGraphicsScene, ActionManager):
    """
        This takes the place of the whole map object. Keeps track of tools
    """
    def __init__(self, parent, parent_window:QMainWindow):
        QGraphicsScene.__init__(self, parent)
        ActionManager.__init__(self)

        self._parent_window = parent_window # used for passing keyboard events up to the gui manager

        self._highlighting_cursor = True
        self._highlight = None
        self._highlighted_id = None
        self._tool = Basic_Tool(self)

        self._alltools={}
        self.add_tool("basic", Basic_Tool) # a purely internal tool, is selected when the user presses escape 
        self.select_tool("basic")

        self._primary = Qt.LeftButton
        self._secondary = Qt.RightButton
        self._primary_held = False
        self._secondary_held  = False

        self._hexCatalog = Catalog(dtype=Hex)
        self._biomeCatalog = RegionCatalog()

        self._pen = QtGui.QPen() # STROKE EFFECTS
        self._pen.setColor(QtGui.QColor(240,240,240))
        self._pen.setStyle(Qt.PenStyle.SolidLine )
        self._pen.setWidth(5)
        self._brush = QtGui.QBrush() #FILL EFFECTS

        self.dimensions = (4000,3000)

        self._debug_wind = {}
            
        
    def save(self, filename:str):
        """
        Saves the clicker state to a file 
        """
        out_dict = {
            "hexes":{},
            "regions":{},
            "drawsize":DRAWSIZE
            }
        hexes = self._hexCatalog
        for hID in hexes._hidcatalog:
            hex=hexes._hidcatalog[hID]
            out_dict["hexes"]["{}.{}".format(hID.xid, hID.yid)]=hex.pack()
        for rID in self._biomeCatalog:
            region=self._biomeCatalog[rID]
            out_dict["regions"]["{}".format(rID)]=region.pack()

        f = open(filename, 'wt')
        json.dump(out_dict, f, indent=4)
        f.close()
        
        
    def load(self, filename:str):
        """
        clears out the catalogs in the clicker and replaces them with our own 
        """
        self.clear()
        self._hexCatalog = Catalog(dtype=Hex)
        self._biomeCatalog = RegionCatalog()
        f = open(filename,'rt')
        in_dict = json.load(f)
        f.close()

        for str_hid in in_dict["hexes"].keys():
            split = str_hid.split(".")
            hid = HexID(int(split[0]), int(split[1]))
            hexobj = Hex.unpack(in_dict["hexes"][str_hid])
            self.addHex(hexobj, hid)
        for str_rid in in_dict["regions"].keys():
            reg = Region.unpack(in_dict["regions"][str_rid])
            self.addRegion(reg)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        self._parent_window.keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        event.accept()
        if event.key() == QtCore.Qt.Key_Plus or event.key()==QtCore.Qt.Key_PageUp or event.key()==QtCore.Qt.Key_BracketRight:
            self._parent_window.scale( 1.05, 1.05 )

        if event.key() == QtCore.Qt.Key_Minus or event.key()==QtCore.Qt.Key_PageDown or event.key()==QtCore.Qt.Key_BracketLeft:
            self._parent_window.scale( 0.95, 0.95 )

        # check if the user did Ctrl+Z for undo or Ctrl+R for redo
        if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            if event.key()==QtCore.Qt.Key_Z:
                self.undo()
            if event.key()==QtCore.Qt.Key_R:
                self.redo()

    def _get_cost_between(self, start_id:HexID, end_id:HexID, ignore_water:bool):
        """
        Function for calculating the movement cost between neighboring hexes 
        Used by the get_route_between_hexes functionm

        -> does not account for locations on map. This is just a raw distance, not including getting closer to the final destination 
        """
        if start_id not in self.hexCatalog:
            raise KeyError("start_id {} not in catalog!".format(start_id))
        if end_id not in self.hexCatalog:
            return(inf)

        start_neighs = start_id.neighbors
        if end_id not in start_neighs:
            return(inf) #you can't teleport. This is an infiinite cost move...

        # We need to be able to have type-specific cost implementations. The Hexmap does not know what kind of map it is
        # So the Hexes themselves will be responsible for calculating the cost.
        # Subtypes of Hexes will implement unique cost functions 

        start_hex = self.hexCatalog[start_id]
        return(start_hex.get_cost( self._hexCatalog[end_id], ignore_water))

    def _get_heuristic(self, start:HexID, end:HexID)->float:
        return self._hexCatalog[start].get_heuristic(self._hexCatalog[end])
    
    def get_route_a_star(self, start_id:HexID, end_id:HexID, ignore_water:bool):
        """
        Finds quickest route between two given HexIDs. Both IDs must be on the Hexmap.
        Always steps closer to the target

        Returns ordered list of HexIDs representing shortest found path between start and end (includes start and end)
        """

        openSet = deque([start_id])
        cameFrom = {}

        gScore = {}
        gScore[start_id] = 0.

        fScore = {}
        fScore[start_id] = self._get_heuristic(start_id,end_id)

        def reconstruct_path(cameFrom:HexID, current:HexID):
            total_path = [current]
            while current in cameFrom.keys():
                current = cameFrom[current]
                total_path.append(current)
            
            return(total_path[::-1])

        while len(openSet)!=0:
            # find minimum fScore thing in openSet
            min_id = None
            min_cost = None
            current = openSet[0]

            if current==end_id:
                return reconstruct_path(cameFrom, current)

            openSet.popleft()
            for neighbor in current.neighbors:
                try:
                    tentative_gScore = gScore[current] + self._get_cost_between(current, neighbor, ignore_water)
                except KeyError:
                    tentative_gScore = inf

                if neighbor in gScore:
                    neigh = gScore[neighbor]
                else:
                    neigh = inf

                if tentative_gScore < neigh:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + self._get_heuristic(neighbor,end_id)
                    if neighbor not in openSet:

                        if len(openSet)==0:
                            openSet.appendleft(neighbor)
                        else:
                            iter = 0
                            while fScore[neighbor]>fScore[openSet[iter]]:
                                iter += 1
                                if iter==len(openSet):
                                    break

                            openSet.insert(iter,neighbor)
        return([])


    @property
    def hexCatalog(self):
        return self._hexCatalog

    @property
    def tool(self):
        return self._tool
    def select_tool(self, tool_name:str):
        self._tool.deselect()
        tool = self._alltools[tool_name]
        self._highlighting_cursor = tool.highlight
        self._tool = tool
        # update the widget part with the tool's config widget 

    def add_tool(self, tool_name:str, tool:Basic_Tool):
        if tool_name in self._alltools:
            raise ValueError("Cannot add tool {}, already exists in tool dict {}".format(tool_name, self._alltools.keys()))
        self._alltools[tool_name]=tool(self)
        # TODO 
        # add button to button grid
        # when you click on the button, the select tool function is called with the proper name 

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if event.button() == self._primary:
            self._primary_held = True 
        elif event.button()==self._secondary:
            self._secondary_held = True

    def mouseMoveEvent(self, event:QGraphicsSceneMouseEvent) -> None:
        self._tool.mouse_moved(event)
        event.accept()

        if self._primary_held:
            action = self._tool.primary_mouse_held(event)
        elif self._secondary_held:
            action = self._tool.primary_mouse_held(event)
        
        if self._primary_held or self._secondary_held:
            if (action is not None):
                if not isinstance(action, NullAction):
                    self.add_to_meta(action)
                    self._meta_event_holder = True

        if self._highlighting_cursor:
            loc = screen_to_hex(event.scenePos())
            if not loc==self._highlighted_id:
                self._highlighted_id=loc
                center = hex_to_screen(loc)
                if self._highlight is not None:
                    self.removeItem(self._highlight)
                    self._highlight=None
                new_hex = Hex(center)
                self._brush.setStyle(0)
                self._pen.setColor(QtGui.QColor(110,228,230))
                self._pen.setStyle(1)
                self._highlight = self.addPolygon(new_hex, self._pen, self._brush)

        else:
            if self._highlight is not None:
                self.removeItem(self._highlight)
                self._highlight = None

    def mouseReleaseEvent(self, event:QGraphicsSceneMouseEvent) -> None:
        if event.button() == self._primary:
            action = self._tool.primary_mouse_released(event)
            self._primary_held=False
        elif event.button() == self._secondary:
            action = self._tool.secondary_mouse_released(event)
            self._secondary_held = False
        if (event.button()==self._primary) or (event.button()==self._secondary):
            if self._meta_event_holder:
                self._meta_event_holder = False
                if not isinstance(action, NullAction):
                    self.add_to_meta(action)
                self.finish_meta()
            else:
                if not isinstance(action, NullAction):
                    self.do_now(action)

    def accessHex(self, coords:HexID):
        """
        returns the hex at the specified hex coordinates, else returns None 
        """
        if coords in self._hexCatalog:
            return self._hexCatalog[coords]
        else:
            return

    def addHex(self, hexobj:Hex, coords:HexID):
        """
        Draws a hex here and registers it 
        """
        
        self._hexCatalog.register(hexobj, coords)
        sid = self.drawHex(coords)
        self._hexCatalog.updateSID(coords, sid)

    def eraseHex(self, coords:HexID)->None:
        sid = self._hexCatalog.getSID(coords)
        if sid is not None:
            self.removeItem(sid)
            self._hexCatalog.updateSID(coords, None)

    def drawHex(self, coords)->QGraphicsItem:
        self.eraseHex(coords)
        hexobj = self._hexCatalog[coords]

        self._brush.setStyle(Qt.BrushStyle.SolidPattern)
        self._brush.setColor(hexobj.fill)
        self._pen.setWidth(1)
        self._pen.setColor(QtGui.QColor(240,240,240))
        sid = self.addPolygon(hexobj, self._pen, self._brush)
        sid.setZValue(0)

        if DEBUG:
            if coords in self._debug_wind:
                self.removeItem(self._debug_wind[coords])
                del self._debug_wind[coords]
            
            loc = hex_to_screen(coords)
            self._pen.setStyle(1)
            self._debug_wind[coords] = self.addLine(loc.x(), loc.y(), loc.x()+0.5*hexobj.wind[0], loc.y()+0.5*hexobj.wind[1], self._pen)
            self._debug_wind[coords].setZValue(5)

        return sid


    def removeHex(self, coords:HexID):
        # remove drawing
        sid = self._hexCatalog.getSID(coords)
        self.removeItem(sid)
        self._hexCatalog.remove(coords)
        self.update()

    def regionAddHex(self,rid:int, coords:HexID):
        """
        Adds a hex to a region
        """
        self._biomeCatalog.add_hex(coords, rid) # update the catalog so it knows about the new association

        region = self._biomeCatalog.get_region(rid) # access the region from the catalog
        new_region = Region(Hex(hex_to_screen(coords)), coords) 
        region = region.merge(new_region) # convert the new space into a region, merge it
        self._biomeCatalog.updateRegion(rid, region) # make the catalog aware of the modified region
        self.drawRegion(rid) # redraw it 

    def accessRegion(self, rid:int)->'Region':
        """
        Returns the region at this rid from the catalog
        """
        return self._biomeCatalog.get_region(rid)
    def accessHexRegion(self,hid:HexID)->int:
        """
        Returns the region at this hexid, returns None if none exists
        """
        return self._biomeCatalog.get_rid(hid)
    def mergeRegions(self, rid1:int, rid2:int):
        region1 = self.accessRegion(rid1)
        region2 = self.accessRegion(rid2)
        if region1 is None:
            raise ValueError("Cannot merge region {}, does not exist".format(rid1))
        if region2 is None:
            raise ValueError("Cannot merge region {}, does not exist".format(rid2))
        
        region1 = region1.merge(region2)
        self._biomeCatalog.updateRegion(rid1, region1)
        self._biomeCatalog.delete_region(rid2)

    def get_next_rid(self):
        return self._biomeCatalog.get_next_rid()

    def deleteRegion(self, rid:int):
        """
        Just straight up delete the region
        """
        if isinstance(self.tool, RegionAdd):
            self.tool.select(-1)
        sid = self._biomeCatalog.getSID(rid) 
        self.removeItem(sid) # undraw
        self._biomeCatalog.delete_region(rid)  # clear it from the catalog 

    def addRegion(self, region:Region)->int:
        """
        Add the new region, which spans this set of Hexes 
        """
        rid = self._biomeCatalog.register_region(region) # add the region to the catalog
        sceneID = self.drawRegion(rid) 
        self._biomeCatalog.updateSID(rid, sceneID) # draw it and update the catalog with the scene ID (sid)
        return rid

    def regionRemoveHex(self, coords:HexID):
        """
            removes a hex from a region
        """
        rid = self._biomeCatalog.get_rid(coords) # get the region id 
        if rid is None:
            # not in a region
            return

        self._biomeCatalog.remove_hex(coords)

        if rid in self._biomeCatalog:
            self.drawRegion(rid)


    def eraseRegion(self, rid):
        """
        Removes the drawing of the rid region
        """
        sid = self._biomeCatalog.get_sid(rid)
        if sid is not None:
            self.removeItem(sid)

        self._biomeCatalog.updateSID(rid, None)

    def drawRegion(self, rid:int):
        """
            See if it has been drawn, erase it, and redraw it
        """
        self.eraseRegion(rid)

        region = self._biomeCatalog.get_region(rid)

        self._brush.setStyle(6)
        self._brush.setColor(region.fill)
        self._pen.setColor(region.fill)
        self._pen.setStyle(0)

        new_sid = self.addPolygon(region,pen=self._pen, brush=self._brush)
        new_sid.setZValue(100)
        self._biomeCatalog.updateSID(rid, new_sid)
        self.update()
        return new_sid


