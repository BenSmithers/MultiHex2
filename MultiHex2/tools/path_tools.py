"""
Here, we define the various path tools. These include (or will include)
    - the road selector tool
    - the new road tool 

"""

from MultiHex2.tools.basic_tool import Basic_Tool, ToolLayer
from MultiHex2.actions.baseactions import NullAction
from MultiHex2.actions.pathactions import Add_Delete_Road, Add_To_Road_End
from MultiHex2.core.coordinates import screen_to_hex, hex_to_screen
from MultiHex2.core.core import Road

from PyQt5 import QtGui
from PyQt5.QtWidgets import QGraphicsSceneEvent

import os


art_dir = os.path.join( os.path.dirname(__file__),'..','assets','buttons')


class PathSelector(Basic_Tool):
    def __init__(self, parent=None):
        self._selected_road = -1 #-1 means None
        super().__init__(parent)

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

    def mouse_moved(self, event):
        return NullAction()

    def primary_mouse_released(self, event:QGraphicsSceneEvent):
        if self.state==5: #new road
            loc = event.scenePos()
            coords = screen_to_hex(loc)
            new_road = Road(coords)
            pid = self.parent.next_free_rid()

            return Add_Delete_Road(pid = pid, road=new_road)

        elif self.state==4: #add to end of road
            pass
        
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