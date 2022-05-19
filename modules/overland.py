"""
This is the main provided module for overland maps 
"""

import os

from MultiHex2.tools.hextools import HexBrush,HexSelect
from MultiHex2.tools.regiontools import CivAdd, RegionAdd
from MultiHex2.tools.route_test_tool import RouteTester
from MultiHex2.tools.entity_tools import EntitySelector, AddEntityTool, AddSettlement
from MultiHex2.tools.map_use_tool import MapUse

from MultiHex2.modules.modules_core import Module
from MultiHex2.generation.overland import fullsim

class Overland(Module):
    def __init__(self):
        super().__init__()

        self._name = "overland"

        self._tools = {
            "hex_select":HexSelect,
            "hex_brush":HexBrush,
            "region_add":RegionAdd,
            "county_add":CivAdd,
            "entity_select":EntitySelector,
            "entity_add":AddEntityTool,
            "settlement_add":AddSettlement,
            "map_use":MapUse
        }

        self._tileset_location=os.path.join(os.path.dirname(__file__), "..","resources","tilesets","main.json")

        self._generator = fullsim

        self._skip_geo = ["mountain","ridge", "peak"]
