from MultiHex2.core import Settlement
from MultiHex2.modules.swon import World
from MultiHex2.modules.swon.world import UnhabWorld

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
            gen_planets = roll2(rng)+1
            worlds = [UnhabWorld(name="{}-{}".format(name, i), rng=rng) for i in range(gen_planets)]

        self._wards = list(sorted(worlds, key=lambda world:world.temperature))


    def add_ward(self, new_ward:World):
        """
        Adds a world to the system 
        """
        return super().add_ward(new_ward)

