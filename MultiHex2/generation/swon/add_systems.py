from MultiHex2.core.coordinates import screen_to_hex
from MultiHex2.modules.swon.system import System
from MultiHex2.modules.swon.world import World

from MultiHex2.core.enums import ToolLayer
from MultiHex2.master_clicker import Clicker

from PyQt5.QtCore import QPointF


from pyparsing import alphas

from numpy import random as rnd

numbers = [str(each) for each in range(10)]
letters = list(set(alphas.upper()))


def add_systems(map:Clicker,seed=None, **kwargs):
    """
        This step just fills in the map with hexes and some nebulae 
    """
    if seed is not None:
        rnd.seed(seed)
    else:
        seed = rnd.randint(1,10000000)

    requried_args =  ["dimx","dimy","n_systems"]
    for arg in requried_args:
        if arg not in kwargs:
            print(kwargs)
            raise Exception("Could not find requied arg {} in kwargs".format(arg))

    dimensions = [kwargs['dimx'],kwargs['dimy']]

    def choice(iter):
        i_choice = rnd.randint(0, len(iter))
        return iter[i_choice]

    def make_systemname()->str:
        name = ""
        name+=choice(letters)+choice(letters)
        name+="-"
        name+=choice(numbers)+choice(numbers)
        return name

    n_systems = 0
    while n_systems < kwargs["n_systems"]:
        # half of the time, let's just make a neighbor! 
        n_used= map._entityCatalog.next_free_eid()
        if  n_used!=0 and rnd.randint(0,4)<2:
            which_choice = rnd.randint(0, n_used)

            from_hid = map._entityCatalog.gethID(which_choice)
            hid = choice(from_hid.neighbors)
        else:
            x_pos = (0.8*rnd.random() + 0.05)*dimensions[0]
            y_pos = (0.8*rnd.random() + 0.05)*dimensions[1]

            hid = screen_to_hex(QPointF(x_pos, y_pos))

        if not hid in map.hexCatalog:
            continue

        if map.access_entity_hex(hid) is not None:
            continue

        new_sys = System(make_systemname(), rng=rnd)

        colors= [ 
            "red",
            "blue",
            "green",
            "orange",
            "yellow",
            "white"
        ]

        new_sys.icon = "star_{}".format(colors[rnd.randint(0,len(colors))])

        map.registerEntity(new_sys, hid)
        n_systems += 1  