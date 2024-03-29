from MultiHex2.core import Settlement, Government
from MultiHex2.core.map_entities import Entity
from MultiHex2.modules.swon import World
from MultiHex2.modules.swon.world import UnhabWorld

from .widgets import WorldWidget, SystemWidget

import numpy as np

def roll2(rng=None):
    if rng is None:
        rng = np.random
    return rng.randint(1,7)+rng.randint(1,7)


class System(Settlement):
    """
    Systems are collections of worlds 
    """
    def __init__(self, name, rng=None, *worlds):
        is_ward = False
        super().__init__(name, None, is_ward)

        

        if len(worlds)==0:
            gen_planets = roll2(rng)-2
            self._primary_world = World(name+" prime")
            worlds = [self._primary_world,] 
            worlds += [UnhabWorld(name="{}-{}".format(name, i), rng=rng) for i in range(gen_planets)]
        else:
            self._primary_world = worlds[0]

        self._wards = list(sorted(worlds, key=lambda world:100-world.temperature))

    def get_primary_world(self)->World:
        return self._primary_world


    def add_ward(self, new_ward:World):
        """
        Adds a world to the system 
        """
        return super().add_ward(new_ward)

    @staticmethod
    def widget(self):
        return [SystemWidget]
