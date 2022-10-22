"""
This is the main provided module for overland maps 
"""

import os

from MultiHex2.tools.hextools import HexBrush,HexSelect
from MultiHex2.tools.regiontools import CivAdd, RegionAdd
from MultiHex2.tools.entity_tools import EntitySelector, AddEntityTool, AddSettlement
from MultiHex2.tools.entity_tools import MobileSelector, NewMobile
from MultiHex2.modules.overland.tools import NewRoadTool, RoadSelector, NewRiverTool, RiverSelector
from MultiHex2.tools.map_use_tool import MapUse
from MultiHex2.core import Hex

from MultiHex2.modules.modules_core import Module
from MultiHex2.generation.overland import fullsim

from MultiHex2.generation.overland.widget import OverlandConfigWidget

from PyQt5 import QtGui

class Overland(Module):
    def __init__(self):
        super().__init__()

        self._name = "overland"

        self._tools = {
            "hex_select":HexSelect,
            "hex_brush":HexBrush,
            "river_select":RiverSelector,
            "river_add":NewRiverTool,
            "region_add":RegionAdd,
            "entity_select":EntitySelector,
            "entity_add":AddEntityTool,
            "road_select":RoadSelector,
            "road_add":NewRoadTool,
            "settlement_add":AddSettlement,
            "county_add":CivAdd,
            "mobile_select":MobileSelector,
            "new_mobile":NewMobile,
            "map_use":MapUse
        }

        self._tileset_location=os.path.join(os.path.dirname(__file__), "..","..","resources","tilesets","main.json")

        self._generator = fullsim

        self._skip_geo = ["mountain","ridge", "peak"]

        self._icon_folder=""

        self._generation_config_widget = OverlandConfigWidget

    def color_correct(self, which:Hex)->QtGui.QColor:
        alt_scale = 0.2
        if which._flat:
            return which.fill
        else:
            return QtGui.QColor(min( 255, max( 0, which._fill.red()*( 1.0 + alt_scale*which.params["altitude_base"]-alt_scale*0.5))),
                        min( 255, max( 0, which._fill.green()*( 1.0 + alt_scale*which.params["altitude_base"]-alt_scale*0.5))),
                        min( 255, max( 0, which._fill.blue()*( 1.0 + alt_scale*which.params["altitude_base"]-alt_scale*0.5))))
