"""
Define the base class we use to create modules. 

Modules provide... 
    - a set of tools
    - a world generator
    - a **main** tileset 
"""

import os
from MultiHex2.master_clicker import Clicker
from MultiHex2.generation.generation_config_widget import GenConfigWidget

def generic(map:Clicker, **kwargs):
    return

class Module:
    def __init__(self):
        
        # Toolname (str) -> Tool 
        self._tools = {}

        self._name = "Default Module"

        self._text_source = "Morrowind"
    
        self._tileset_location = ""
        self._generator = generic
        self._skip_geo=[]
        self._icon_folder=""
        self._generation_config_widget = GenConfigWidget

    @property
    def generation_config(self):
        """
        Returns the widget that can be used to configure the world generator this module uses! 
        """
        return self._generation_config_widget

    @property
    def icon_folder(self)->str:
        """
        An extra folder for providing more icons. 
        """
        return self._icon_folder

    @property
    def text_source(self):
        """
        Which name file to load in for making MCMC tables and generating names 
        """
        return self._text_source

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
