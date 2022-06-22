"""
Here, we define the various path tools. These include (or will include)
    - the road selector tool
    - the new road tool 

"""

from MultiHex2.tools.basic_tool import Basic_Tool, ToolLayer
from MultiHex2.actions.baseactions import MetaAction, NullAction
from MultiHex2.actions.pathactions import Add_Delete_Road, Add_To_Road_End
from MultiHex2.core.coordinates import screen_to_hex, hex_to_screen, HexID, get_adjacent_vertices
from MultiHex2.core.core import Path, Road
from MultiHex2.tools.widgets import PathWidget

from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsSceneEvent

import os

art_dir = os.path.join( os.path.dirname(__file__),'..','assets','buttons')

"""
Codeblock for path drawing... 

path = QtGui.QPainterPath()
path.addPolygon( QtGui.QPolygonF( QPointF's... ))
self._step_object = self.parent.scene.addPath( path, pen=self.QPen, brush=self.QBrush )
"""

class PathSelector(Basic_Tool):
    def __init__(self, parent=None):
        Basic_Tool.__init__(self, parent)
        self._selected_road = -1 #-1 means None
        self.highlight=True
        self._vertex_mode = False

    @classmethod
    def widget(self):
        return PathWidget

    def get_next_steps(self, event:QGraphicsSceneEvent)->list:
        """
        Utility function for when drawing a path. 
            This gets the next step of the path for when you're drawing a path. 
            It looks at the end of the presently selected path, and where the mouse is. 
                In non-vertex mode it gets the path to the mouse (A* algorithm ftw)
                In vertex mode it just gets the next step to the mouse (greedy)
        """
        start = self.get_selected_road.get_end()
        loc = event.scenePos()
        if self._vertex_mode:
            adjacent = get_adjacent_vertices(loc)
            id_closest = None
            dist_closest = 0.0
            
            # find which of these QPointF's is closest to the mouse 
            for each in adjacent:
                this_dist = (each.x()-loc.x())**2 + (each.y() - loc.y())**2
                if id_closest is None:
                    id_closest = each
                    dist_closest = this_dist
                else:
                    if this_dist < dist_closest:
                        dist_closest = this_dist
                        id_closest = each
            return [id_closest,]
                
        else:
            end_id = screen_to_hex(loc)
            return self.parent.get_route_a_star(start, end_id, False)

    def mouse_moved(self, event):
        if self.state==4:
            if self.get_selected_road is None:
                self.set_state(0)

            next_step = self.get_next_steps(event)
            if self.vertex_mode:
                route = [self.get_selected_road.get_end()] + next_step
            else:
                route = [hex_to_screen(entry) for entry in next_step]

            path = QtGui.QPainterPath()
            path.addPolygon( QtGui.QPolygonF( route ))
            #self._step_object = self.parent.scene.addPath( path, pen=self.QPen, brush=self.QBrush )

            self._polygon = path
        return NullAction()

    @property
    def get_selected_road(self)->Path:
        raise NotImplementedError("Implementation will depend on what kind of path this is")

    @property
    def vertex_mode(self)->bool:
        return self._vertex_mode

    @property
    def selected_road(self)->int:
        return self._selected_road
    
    def select_road(self, road_id:int)->None:
        self._selected_road = road_id

    @classmethod
    def tool_layer(cls):
        return ToolLayer.null

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "temp.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "temp.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "Path Selector Tool"

class RiverSelector(PathSelector):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._vertext_mode = True

    @classmethod
    def altText(cls):
        return "River Selector Tool"

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "river_icon.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "river_icon.svg")).scaled(48,48)
    
    @classmethod
    def tool_layer(cls):
        return ToolLayer.terrain

class RoadSelector(PathSelector):
    def __init__(self, parent=None):
        super().__init__(parent)

    @property
    def get_selected_road(self)->Road:
        if self.selected_road==-1:
            return None
        else:
            return self.parent.get_path(self.selected_road)

    @classmethod
    def altText(cls):
        return "Road Selector Tool"

    @classmethod
    def tool_layer(cls):
        return ToolLayer.civilization
    

class NewRoadTool(RoadSelector):
    def __init__(self, parent=None):
        """
        Multiple possible states! 
            5 - making new road
            4 - adding to end of road
            3 - adding to start of road
            0 - selecting mode
        """
        super().__init__(parent)
        self.auto_state = 5
        self.highlight_icon="plus"


    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "new_road.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "new_road.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "New Road Tool"


    def primary_mouse_released(self, event:QGraphicsSceneEvent):
        if self.state==5: #new road
            
            loc = event.scenePos()
            coords = screen_to_hex(loc)
            new_road = Road(coords)
            pid = self.parent.next_free_rid()
            print("Making new road? ROD {}".format(pid))
            self.set_state(4)
            self.select_road(pid)
            return Add_Delete_Road(pid = pid, road=new_road)

        elif self.state==4: #add to end of road
            route = self.get_next_steps(event)[1:]
            # skip the first step! 

            all_actions = [Add_To_Road_End(pid= self.selected_road, hexID = entry) for entry in route]
            combo = MetaAction(*all_actions)
            return combo
        
        elif self.state==3: # add to start of road
            pass

        return NullAction()


    
class NewRiverTool(RiverSelector):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.auto_state = 1
        self.highlight_icon="river_icon"


    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "new_river.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "new_river.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "New River Tool"