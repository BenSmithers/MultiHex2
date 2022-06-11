"""
This is the main provided module for overland maps 
"""

import os

from MultiHex2.tools.hextools import HexBrush,HexSelect
from MultiHex2.tools.regiontools import CivAdd, RegionAdd
from MultiHex2.tools.route_test_tool import RouteTester
from MultiHex2.tools.entity_tools import EntitySelector, AddEntityTool, AddSettlement
from MultiHex2.tools.path_tools import NewRoadTool, RoadSelector, NewRiverTool, RiverSelector
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
            "river_select":RiverSelector,
            "river_add":NewRiverTool,
            "region_add":RegionAdd,
            "entity_select":EntitySelector,
            "entity_add":AddEntityTool,
            "road_select":RoadSelector,
            "road_add":NewRoadTool,
            "settlement_add":AddSettlement,
            "county_add":CivAdd,
            "map_use":MapUse
        }

        self._tileset_location=os.path.join(os.path.dirname(__file__), "..","resources","tilesets","main.json")

        self._generator = fullsim

        self._skip_geo = ["mountain","ridge", "peak"]
