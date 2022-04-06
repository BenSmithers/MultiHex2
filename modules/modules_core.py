"""
Define the base class we use to create modules. 

Modules provide... 
    - a set of tools
    - a world generator
    - a **main** tileset 
"""

import os
from MultiHex2.tools.clicker_tool import Clicker

def generic(map:Clicker, **kwargs):
    return

class Module:
    def __init__(self):
        
        # Toolname (str) -> Tool 
        self._tools = {}

        self._name = "Default Module"
    
        self._tileset_location = ""
        self._generator = generic
        self._skip_geo=[] 

    @property
    def skip_geo(self):
        """
        when assigning a geography/climate to a hex (using the apply_tileset function)
        skip the hexes that have these geographies
        """
        return self._skip_geo

    @property
    def tileset(self):
        return self._tileset_location

    @property
    def generator_function(self):
        return self._generator

    @property
    def name(self)->str:
        return self._name

    @property
    def tools(self)->dict:
        return self._tools
