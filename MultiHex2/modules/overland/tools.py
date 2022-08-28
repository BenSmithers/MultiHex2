import os

from MultiHex2.tools import PathSelector

from MultiHex2.modules.overland import River, Road
from MultiHex2.generation.overland.make_rivers import _pour_river
from MultiHex2.core.enums import ToolLayer

from MultiHex2.widgets.widgets import RiverWidget, RoadWidget

from MultiHex2.actions.pathactions import Add_Delete_Road, Add_To_Road_End, Add_To_Road_Start
from MultiHex2.actions.pathactions import Add_Delete_River, Add_To_River_End, Add_To_River_Start

from PyQt5 import QtGui


art_dir = os.path.join( os.path.dirname(__file__),'..',"..",'assets','buttons')


class RiverSelector(PathSelector):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._vertex_mode = True
        self._pathtype = River
        self._actiontypes = [Add_Delete_River, Add_To_River_End, Add_To_River_Start]

    def double_click_event(self, event):
        loc = event.scenePos()
        _pour_river(self.parent, loc)
        return super().double_click_event(event)


    @property
    def get_selected_path(self) -> River:
        return super().get_selected_path

    @classmethod
    def altText(cls):
        return "River Selector Tool"

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "select_river.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "select_river.svg")).scaled(48,48)
    
    @classmethod
    def tool_layer(cls):
        return ToolLayer.terrain

    @classmethod
    def widget(self):
        return RiverWidget

class RoadSelector(PathSelector):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._pathtype = Road
        self._actiontypes = [Add_Delete_Road,Add_To_Road_End,Add_To_Road_Start]

    @classmethod
    def widget(self):
        return RoadWidget


    def select_path(self, road_id: int) -> None:
        super().select_path(road_id)    
        this_road = self.get_selected_path
        if this_road is not None:
            self.widget_instance.ui.quality_spin.setValue(this_road.quality)

    @property
    def get_selected_path(self) -> Road:
        return super().get_selected_path

    @classmethod
    def altText(cls):
        return "Road Selector Tool"

    @classmethod
    def tool_layer(cls):
        return ToolLayer.civilization

class NewRoadTool(RoadSelector):
    def __init__(self, parent=None):
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

    
class NewRiverTool(RiverSelector):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.auto_state = 5
        self.highlight_icon="river_icon"
        self._vertex_mode = True

    @classmethod
    def buttonIcon(cls):
        assert(os.path.exists(os.path.join(art_dir, "new_river.svg")))
        return QtGui.QPixmap(os.path.join(art_dir, "new_river.svg")).scaled(48,48)

    @classmethod
    def altText(cls):
        return "New River Tool"