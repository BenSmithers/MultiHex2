"""
Module for making and editing Stars Without Number (Swon) maps
"""

import os
from MultiHex2.generation.swon.widget import SwoNConfigWidget 

from MultiHex2.modules.modules_core import Module

from MultiHex2.tools.hextools import HexBrush,HexSelect
from MultiHex2.tools.hextools import HexBrush,HexSelect
from MultiHex2.tools.regiontools import CivAdd, RegionAdd
from MultiHex2.tools.entity_tools import EntitySelector, AddEntityTool, AddSettlement
from MultiHex2.tools.entity_tools import MobileSelector, NewMobile
from MultiHex2.modules.overland.tools import NewRoadTool, RoadSelector
from MultiHex2.tools.map_use_tool import MapUse

from .tools import AddSystem
from MultiHex2.generation.swon import fullsim

class SwoN(Module):
    def __init__(self):
        super().__init__()

        self._name = "Stars Without Number"

        self._tools = {
            "hex_select":HexSelect,
            "hex_brush":HexBrush,
            "region_add":RegionAdd,
            "entity_select":EntitySelector,
            "road_select":RoadSelector,
            "road_add":NewRoadTool,
            "settlement_add":AddSystem,
            "county_add":CivAdd,
            "mobile_select":MobileSelector,
            "new_mobile":NewMobile,
            "map_use":MapUse
        }

        self._tileset_location=os.path.join(os.path.dirname(__file__), "..","..","resources","tilesets","swon.json")
        self._icon_folder=os.path.join(os.path.dirname(__file__), "..", "..","assets","swon_icons")

        self._generator = fullsim
        self._generation_config_widget = SwoNConfigWidget