
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent, QMainWindow, QApplication
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsView, QGraphicsDropShadowEffect

from MultiHex2.core.core import DRAWSIZE, GeneralCatalog, PathCatalog, Road
from MultiHex2.core import HexCatalog, RegionCatalog, EntityCatalog
from MultiHex2.core import Hex, HexID, Region, Entity
from MultiHex2.core import screen_to_hex
from MultiHex2.actions import ActionManager
from MultiHex2.tools.basic_tool import Basic_Tool, ToolLayer
from MultiHex2.tools.regiontools import RegionAdd
from MultiHex2.core.map_entities import Settlement, IconLib
from MultiHex2.clock import Time, Clock
from MultiHex2.actions.baseactions import NullAction
from MultiHex2.core.coordinates import hex_to_screen
from MultiHex2.generation.utils import Climatizer

import json
from collections import deque
from math import inf
import numpy as np
from time import time

import gzip

DEBUG = True

class Clicker(QGraphicsScene, ActionManager):
    """
        This takes the place of the whole map object. Keeps track of tools
    """
    def __init__(self, parent:QGraphicsView, parent_window:QMainWindow):
        QGraphicsScene.__init__(self, parent)
        ActionManager.__init__(self)

        self.parent = parent
        self._parent_window = parent_window # used for passing keyboard events up to the gui manager
        self.file_name = ""

        self._highlight = None
        self._highlighted_id = None
        self._icon_ghost = None
        self._tool = Basic_Tool(self)

        self._alltools={}
        self.add_tool("basic", Basic_Tool) # a purely internal tool, is selected when the user presses escape 
        self.select_tool("basic")

        self._primary = Qt.LeftButton
        self._secondary = Qt.RightButton
        self._primary_held = False
        self._secondary_held  = False

        self._hexCatalog = HexCatalog(dtype=Hex)
        self._biomeCatalog = RegionCatalog()
        self._countyCatalog = RegionCatalog()
        self._entityCatalog = EntityCatalog()
        self._roadCatalog = PathCatalog()

        self._pen = QtGui.QPen() # STROKE EFFECTS
        self._pen.setColor(QtGui.QColor(240,240,240))
        self._pen.setStyle(Qt.PenStyle.SolidLine )
        self._pen.setWidth(5)
        self._brush = QtGui.QBrush() #FILL EFFECTS

        self.dimensions = (4000,3000)

        self._debug_wind = {}

        self.iconLibrary = IconLib()

        self.module = ""
        self.tileset = ""

    def set_primary_mouse(self, left_button=True):
        if left_button:
            self._primary = Qt.LeftButton
            self._secondary = Qt.RightButton
        else:
            self._primary = Qt.RightButton
            self._secondary = Qt.LeftButton

    def apply_tileset(self, tileset:dict)->None:
        climate = Climatizer(tileset)
        self.tileset = tileset
        for hID in self.hexCatalog:
            if self.hexCatalog[hID].geography in self._parent_window.module.skip_geo:
                continue
            climate.apply_climate_to_hex(self.hexCatalog[hID])
            self.drawHex(hID)
        
    def save(self, filename:str):
        """
        Saves the clicker state to a json file.

        TODO: look into using bzip2 to zip the json files. If it's fast enough, it might be worth doing!  
        """
        out_dict = {
            "hexes":{},
            "bregions":{},
            "cregions":{},
            "entities":{},
            "drawsize":DRAWSIZE,
            "dimensions":[self.dimensions[0], self.dimensions[1]],
            "module":self.module,
            "time":{
                "year":self._clock.time.year,
                "month":self._clock.time.month,
                "day":self._clock.time.day,
                "hour":self._clock.time.hour,
                "minute":self._clock.time.minute
            }
        }
        t1 = time()
        hexes = self._hexCatalog
        for hID in hexes:
            hex = hexes.get(hID)
            out_dict["hexes"]["{}.{}".format(hID.xid, hID.yid)]=hex.pack()
        for rID in self._biomeCatalog:
            region=self._biomeCatalog[rID]
            out_dict["bregions"]["{}".format(rID)]=region.pack()
        for rID in self._countyCatalog:
            region = self._countyCatalog[rID]
            out_dict["cregions"]["{}".format(rID)]=region.pack()
        if False:
            for eID in self._entityCatalog:
                entity = self._entityCatalog.access_entity(eID)
                out_dict["entities"]["{}".format(eID)]=entity.pack()
        
        t2 = time()

        f = open(filename, 'wt')
        json.dump(out_dict, f, indent=4)
        f.close()
        t3 = time()

        #print("Packing took {} seconds".format(t2-t1))
        #print("Dumping took {} seconds".format(t3-t2))

        self.file_name = filename
        
        
    def load(self, filename:str):
        """
        clears out the catalogs in the clicker and replaces them with our own 
        """
        self.clear()
        self._hexCatalog = HexCatalog(dtype=Hex)
        self._biomeCatalog = RegionCatalog()
        f = open(filename,'rt')
        in_dict = json.load(f)
        self.file_name = filename
        f.close()
        for str_hid in in_dict["hexes"].keys():
            split = str_hid.split(".")
            hid = HexID(int(split[0]), int(split[1]))
            hexobj = Hex.unpack(in_dict["hexes"][str_hid])
            self.addHex(hexobj, hid)
        for str_rid in in_dict["bregions"].keys():
            reg = Region.unpack(in_dict["bregions"][str_rid])
            self.addRegion(reg, ToolLayer.terrain )
        for str_rid in in_dict["cregions"].keys():
            reg = Region.unpack(in_dict["cregions"][str_rid])
            self.addRegion(reg, ToolLayer.civilization)

        _time_dict= in_dict["time"]
        time = Time(minute=_time_dict["minute"], hour=_time_dict["hour"], 
                     day=_time_dict["day"], month=_time_dict["month"],year=_time_dict["year"]
            )

        self.configure_with_clock(Clock(time))

        self.module=in_dict["module"]

        self._parent_window.ui.clock.set_time(time)
        self._parent_window.ui.events.update()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Called when a keyboard button is depressed
        """
        self._parent_window.keyPressEvent(event)

    def keyReleaseEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        Called when a keyboard button is released
        """
        event.accept()
        if event.key() == QtCore.Qt.Key_Plus or event.key()==QtCore.Qt.Key_PageUp or event.key()==QtCore.Qt.Key_BracketRight:
            self.parent.scale( 1.05, 1.05 )

        if event.key() == QtCore.Qt.Key_Minus or event.key()==QtCore.Qt.Key_PageDown or event.key()==QtCore.Qt.Key_BracketLeft:
            self.parent.scale( 0.95, 0.95 )

        # check if the user did Ctrl+Z for undo or Ctrl+R for redo
        if QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            if event.key()==QtCore.Qt.Key_Z:
                self.undo()
            if event.key()==QtCore.Qt.Key_R:
                self.redo()

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

        loc = screen_to_hex(event.scenePos())
        if self.tool.highlight: 
            if self._icon_ghost is not None:
                    self.removeItem(self._icon_ghost)
                    self._icon_ghost = None   
            if not loc==self._highlighted_id:
                # idea - ask the tool for the polygon to use for this! 
                # TODO should be smart about it - if the "new_hex is a Hex do addPolygon", otherwise add it as a path? 

                self._highlighted_id=loc
                if self._highlight is not None:
                    self.removeItem(self._highlight)
                    self._highlight=None
                new_hex =  self.tool.get_polygon() # Hex(center)

                self._brush.setStyle(0)
                self._pen.setColor(QtGui.QColor(110,228,230)) # how did I choose this color? It should ask the tool for this color 
                self._pen.setStyle(1)
                if isinstance(new_hex, Hex):
                    self._highlight = self.addPolygon(new_hex, self._pen, self._brush)
                elif isinstance(new_hex, QtGui.QPainterPath):
                    self._highlight = self.addPath(new_hex, self._pen, self._brush)
                else:
                    raise NotImplementedError("Polygon is of type {}".format(type(new_hex)))

        else:
            if self._highlight is not None:
                self.removeItem(self._highlight)
                self._highlight = None


            if self.tool.highlight_icon!="":
                if self.tool.state==1:
                    this_pos = hex_to_screen(loc)
                    offset = self.iconLibrary.access(self.tool.highlight_icon).width()/2
                    if self._icon_ghost is None:
                        # make it
                        self._icon_ghost = self.addPixmap(self.iconLibrary.access(self.tool.highlight_icon))
                        self._icon_ghost.setZValue(200)
                    self._icon_ghost.setPos(this_pos - QtCore.QPointF(offset, offset))
                elif self.tool.state == 0:
                    if self._icon_ghost is not None:
                        self.removeItem(self._icon_ghost)
                        self._icon_ghost = None
            else:
                if self._icon_ghost is not None:
                    self.removeItem(self._icon_ghost)
                    self._icon_ghost = None

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        action = self._tool.double_click_event(event)
        if not isinstance(action, NullAction):
            self.do_now(action)

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

    def _get_heuristic(self, start:HexID, end:HexID,ignore_water=False)->float:
        return self._hexCatalog[start].get_heuristic(self._hexCatalog[end],ignore_water)
    
    def get_route_a_star(self, start_id:HexID, end_id:HexID, ignore_water:bool)->'list[HexID]':
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

        def reconstruct_path(cameFrom:HexID, current:HexID)->'list[HexID]':
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

    ########################### ENTITY METHODS #################################

    def nextFreeEID(self)->int:
        return self._entityCatalog.next_free_eid()
    def registerEntity(self, entity, hID:HexID):
        temp_sid = -1
        self._entityCatalog.register(hID, entity, temp_sid)
        self.draw_entities_at_hex(hID)
    def updateEntity(self, eID:int, entity:Entity):
        self._entityCatalog.update_entity(eID, entity)
        here = self._entityCatalog.gethID(eID)
        self.draw_entities_at_hex(here)
    def removeEntity(self, eID:int):
        here = self._entityCatalog.gethID(eID)
        this_sid = self._entityCatalog.getSID(here)
        self.removeItem(this_sid)
        self._entityCatalog.remove(eID)

    def accessEid(self,eID)->Entity:
        return self._entityCatalog.access_entity(eID)

    def eIDs_at_hex(self, coords:HexID):
        """
        returns eIDs at this HexID
        """
        return self._entityCatalog.access_entities_at(coords)

    def draw_entities_at_hex(self, coords:HexID):
        """
        Drawing hierarchy goes
            Mobile > Settlement > Anything Else

        If there's something more, maybe add a little plus sign? 
        """
        pos = hex_to_screen(coords)

        # remove anything already here! 
        here = self._entityCatalog.getSID(coords)
        if (here is not None) and here!=-1:
            self.removeItem(here)
        self.update()


        these_entities = self.eIDs_at_hex(coords)
        if len(these_entities)==0:
            return
        for eID in these_entities:
            this_entity = self.accessEid(eID)

            # mobiles not yet implemented 
            if isinstance(this_entity, Settlement):
                break
        # current values of (eID, this_entity) are what we'll use 
        use_this_pm = self.iconLibrary.access(this_entity.icon)

        offset = QtCore.QPointF(use_this_pm.width()/2, use_this_pm.height()/2)
        sid = self.addPixmap(use_this_pm)
        sid.setPos(pos-offset)
        sid.setZValue(20)
        self._entityCatalog.update_sid(coords, sid)

    

    @property
    def hexCatalog(self):
        return self._hexCatalog

    #################################### PATH ACCESS METHODS #####################

    def _get_path_cat(self, layer:ToolLayer)->GeneralCatalog:
        """
            shorthand for getting the catalog corresponding to this layer
        """
        if layer==ToolLayer.null or layer==ToolLayer.terrain:
            return NotImplementedError("Nothing for {}. Did you use a relative import? Don't!".format(layer))
        elif layer==ToolLayer.civilization:
            return self._roadCatalog
        else:
            raise NotImplementedError("Nothing for {}. Did you use a relative import? Don't!".format(layer))

    def get_path(self, id:int)->Road:
        using = self._get_path_cat(self.tool.tool_layer())

        if id in using:
            return using[id]
        else:
            return None

    @property
    def roadCatalog(self):
        return self._roadCatalog

    def next_free_rid(self):
        return self._roadCatalog.get_next_id()

    def register_road(self, road:Road):
        rid = self._roadCatalog.register(road)
        self.draw_road(rid)

    def remove_road(self, rid:int):
        sid = self._roadCatalog.get_sid(rid)
        self.removeItem(sid)
        self._roadCatalog.remove(rid)

    def draw_road(self, rid):

        """
         self.addPath(new_hex, self._pen, self._brush)
         path = QtGui.QPainterPath()
         path.addPolygon( QtGui.QPolygonF( route ))
        """

        current_sid = self._roadCatalog.get_sid(rid)
        if (current_sid is not None) and current_sid!=-1:
            self.removeItem(current_sid)
        self.update()

        this_path = self.get_path(rid)
        if this_path is None:
            self._roadCatalog.remove(rid)
            return
        else:
            verts = [hex_to_screen(vert) for vert in this_path.vertices]
            path = QtGui.QPainterPath()
            path.addPolygon(QtGui.QPolygonF(verts))
            self._pen.setStyle(1)
            self._pen.setWidth(3)
            self._pen.setColor(QtGui.QColor(245,245,245))
            self._brush.setStyle(0)
            self.addPath(path, self._pen, self._brush)


    #################################### TOOL ACCESS METHODS ################################3

    @property
    def tool(self):
        return self._tool
    def select_tool(self, tool_name:str):
        old_layer = self._tool.tool_layer()

        self._tool.deselect()
        tool = self._alltools[tool_name]
        self._tool = tool
        self._tool.set_state(tool.auto_state)

        if (self._tool.tool_layer() != ToolLayer.null):
            self.reDrawRegions()

        # update the widget part with the tool's config widget 

    def clear_tools(self):
        self._alltools = {}
        self.add_tool("basic", Basic_Tool) 
        self.select_tool("basic")

    def add_tool(self, tool_name:str, tool:Basic_Tool):
        if tool_name in self._alltools:
            raise ValueError("Cannot add tool {}, already exists in tool dict {}".format(tool_name, self._alltools.keys()))
        self._alltools[tool_name]=tool(self)

    ######################### HEX METHODS #############################

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
        self._hexCatalog.update_sid(coords, sid)

    def eraseHex(self, coords:HexID)->None:
        sid = self._hexCatalog.get_sid(coords)
        if sid is not None:
            self.removeItem(sid)
            self._hexCatalog.update_sid(coords, None)

    def drawHex(self, coords)->QGraphicsItem:
        self.eraseHex(coords)
        hexobj = self._hexCatalog[coords]

        self._brush.setStyle(Qt.BrushStyle.SolidPattern)
        self._brush.setColor(hexobj.fill)
        self._pen.setWidth(1)
        self._pen.setStyle(1)
        self._pen.setColor(QtGui.QColor(170,170,170))
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
        sid = self._hexCatalog.get_sid(coords)
        self.removeItem(sid)
        self._hexCatalog.remove(coords)
        self.update()

    ############################### REGION METHODS ###################################3

    def _get_region_cat(self, layer:ToolLayer):
        """
            shorthand for getting the catalog corresponding to this layer
        """
        if layer==ToolLayer.null or layer==ToolLayer.terrain:
            return self._biomeCatalog
        elif layer==ToolLayer.civilization:
            return self._countyCatalog
        else:
            raise NotImplementedError("Nothing for {}. Did you use a relative import? Don't!".format(layer))

    def regionAddHex(self,rid:int, coords:HexID, layer:ToolLayer):
        """
        Adds a hex to a region
        """
        using = self._get_region_cat(layer)

        using.add_hex(coords, rid) # update the catalog so it knows about the new association

        region = using.get(rid) # access the region from the catalog
        new_region = Region(Hex(hex_to_screen(coords)), coords) 
        region = region.merge(new_region) # convert the new space into a region, merge it
        using.update_obj(rid, region) # make the catalog aware of the modified region


        self.drawRegion(rid, layer) # redraw it 

    def accessRegion(self, rid:int, layer:ToolLayer)->'Region':
        """
        Returns the region at this rid from the catalog
        """
        return self._get_region_cat(layer).get(rid)
    def accessHexRegion(self,hid:HexID, layer:ToolLayer)->int:
        """
        Returns the region at this hexid, returns None if none exists
        """
        return self._get_region_cat(layer).get_rid(hid)
        
    def mergeRegions(self, rid1:int, rid2:int, layer:ToolLayer):
        """
        Merges the two regions
        """
        region1 = self.accessRegion(rid1, layer)
        region2 = self.accessRegion(rid2, layer)
        if region1 is None:
            raise ValueError("Cannot merge region {}, does not exist".format(rid1))
        if region2 is None:
            raise ValueError("Cannot merge region {}, does not exist".format(rid2))
        
        using = self._get_region_cat(layer)
        region1 = region1.merge(region2)
        using.update_obj(rid1, region1)
        using.delete_region(rid2)

    def get_next_rid(self, layer:ToolLayer):
        return self._get_region_cat(layer).get_next_id()

    def deleteRegion(self, rid:int, layer:ToolLayer):
        """
        Just straight up delete the region
        """
        if isinstance(self.tool, RegionAdd):
            self.tool.select(-1)

        using = self._get_region_cat(layer)
        sids = using.get_sid(rid) 
        for sid in sids:
            self.removeItem(sid) # undraw
        using.delete_region(rid, layer)  # clear it from the catalog 

    def addRegion(self, region:Region, layer:ToolLayer)->int:
        """
        Add the new region, which spans this set of Hexes 
        """
        using = self._get_region_cat(layer)

        rid = using.register(region) # add the region to the catalog
        sceneID = self.drawRegion(rid, layer) 
        return rid

    def regionRemoveHex(self, coords:HexID, layer:ToolLayer):
        """
            removes a hex from a region
        """
        using = self._get_region_cat(layer)

        rid = using.get_rid(coords) # get the region id 
        if rid is None:
            # not in a region
            return

        using.remove_hex(coords)

        if rid in self._biomeCatalog:
            self.drawRegion(rid, layer)


    def eraseRegion(self, rid, layer:ToolLayer):
        """
        Removes the drawing of the rid region
        """
        using = self._get_region_cat(layer)
        sids = using.get_sid(rid)
        if sids is not None:
            for sid in sids:
                self.removeItem(sid)

        using.update_sid(rid, None)

    def reDrawRegions(self):
        print("redrawing! Selected {}".format(self.tool.tool_layer()))

        using = self._get_region_cat(ToolLayer.terrain)
        for rid in using:
            self.drawRegion(rid, ToolLayer.terrain)

        using = self._get_region_cat(ToolLayer.civilization)
        for rid in using:
            self.drawRegion(rid, ToolLayer.civilization)


    def drawRegion(self, rid:int, layer:ToolLayer):
        """
            See if it has been drawn, erase it, and redraw it

            If the selected tool is Terrain, we draw borders for the biomes only 
            If the selected 

        """

        active = self._tool.tool_layer()
        civmode = (active.value== 2) or (active.value ==3)
            

        using = self._get_region_cat(layer)
        self.eraseRegion(rid, layer)
        region = using.get(rid)

        if (civmode and layer==ToolLayer.civilization) or ((not civmode) and layer==ToolLayer.terrain):
            self._brush.setStyle(1)
            self._brush.setColor(QtGui.QColor(region.fill.red(), region.fill.green(), region.fill.blue(), 100))
            self._pen.setColor(region.fill)
            self._pen.setStyle(0)
            font_size = 16
        else: # don't fill 
            self._brush.setStyle(0)
            self._brush.setColor(QtGui.QColor(region.fill.red(), region.fill.green(), region.fill.blue(), 1))
            self._pen.setColor(region.fill)
            self._pen.setStyle(0)
            font_size = 12

        new_sid = self.addPolygon(region,pen=self._pen, brush=self._brush)
        new_sid.setZValue(100)

        drop = QGraphicsDropShadowEffect()
        drop.setOffset(1)
        font = QtGui.QFont("Decorative")
        new_color= QtGui.QColor( 250, 250, 250)

        font.setPointSize( font_size )

        loc = region.average_location()

        text_sid = self.addText(region.name, font)
        
        width = text_sid.boundingRect().width()
        if width>300:
            text_sid.setTextWidth(300)
            width = 300
            
        loc = QtCore.QPointF( loc.x()-width*0.5, loc.y())

        text_sid.setPos(loc)
        text_sid.setZValue(110)
        text_sid.setGraphicsEffect( drop )
        text_sid.setDefaultTextColor( new_color )

        using.update_sid(rid, new_sid, text_sid)
        self.update()
        return new_sid, text_sid


