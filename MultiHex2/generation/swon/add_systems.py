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
        name+=choice(numbers)+choice(numbers)
        name+="-"
        return name

    n_systems = 0
    while n_systems < 10:
        x_pos = (0.8*rnd.random() + 0.05)*dimensions[0]
        y_pos = (0.8*rnd.random() + 0.05)*dimensions[1]

        hid = screen_to_hex(QPointF(x_pos, y_pos))
        if not hid in map.hexCatalog:
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