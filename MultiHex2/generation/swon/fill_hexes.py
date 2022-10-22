"""
Fill the map with hexes
"""

from MultiHex2.core.enums import ToolLayer
from MultiHex2.master_clicker import Clicker
from MultiHex2.core import Hex
from MultiHex2.core import Region
from MultiHex2.generation.utils import perlin
from MultiHex2.core.coordinates import DRAWSIZE, hex_to_screen, screen_to_hex
from MultiHex2.generation.name_gen import create_name


from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor


from numpy import random as rnd
from math import sqrt


def generate(map:Clicker,seed=None, **kwargs):
    """
        This step just fills in the map with hexes and some nebulae 
    """
    if seed is not None:
        rnd.seed(seed)
    else:
        seed = rnd.randint(1,10000000)

    requried_args = ["dimx","dimy"]
    for arg in requried_args:
        if arg not in kwargs:
            raise Exception("Could not find requied arg {} in kwargs".format(arg))

    dimensions = [kwargs['dimx'],kwargs['dimy']]

    noise = perlin(dimensions[0],octave=10, seed=seed)

    """
    drawsize is the radius
    """
    i_x = 0
    i_y = 0

    # vertical separation DRAWSIZE*SQRT(3)
    # horizontal separation is DRAWSIZE*sqrt(3)/2
    # 0,0 is 0,0

    max_x = int(dimensions[0]/(DRAWSIZE*sqrt(3)/2))+1
    max_y = int(dimensions[1]/(DRAWSIZE*sqrt(3)))+1

    RTHREE = sqrt(2)

    superset = map.tileset["space"]

    fill = superset["deepspace"]["color"]

    while i_x < max_x:
        while i_y < max_y:
            x_pos = i_x*DRAWSIZE*RTHREE/2 
            y_pos = i_y*DRAWSIZE*RTHREE + 0.2*DRAWSIZE
            
            i_y += 1

            hid = screen_to_hex(QPointF(x_pos, y_pos) )

            if hid in map.hexCatalog:
                continue

            new_hex = Hex(hex_to_screen(hid))
            new_hex.set_fill(QColor(fill[0], fill[1], fill[2]))
            new_hex.set_params(superset["deepspace"]["params"])
            new_hex.geography = "deep space"
            map.addHex(new_hex, hid)
            
        i_x+=1 

    neb_fill = superset["nebula"]["color"]
    i_nebula = 0

    def make_nebula(what):
        this_hex = map.accessHex(what)
        this_hex.set_fill(QColor(neb_fill[0], neb_fill[1], neb_fill[2]))
        this_hex.set_params(superset["nebula"]["params"])
        this_hex.geography = "nebula"

    while i_nebula < 10:
        x_pos = (0.9*rnd.random() + 0.05)*DRAWSIZE[0]
        y_pos = (0.9*rnd.random() + 0.05)*DRAWSIZE[1]

        hid = screen_to_hex(QPointF(x_pos, y_pos) )
        if not hid in map.hexCatalog:
            raise Exception("How is there no hex here...")
        
        make_nebula(hid)
        this_hex= map.accessHex(hid)
        # new region here too 
        this_nebula = Region(this_hex, hid)
        this_nebula.set_name(create_name("nebula"))
        rid = map.addRegion(this_nebula, ToolLayer.terrain)

        for neigh_id in hid.neighbors:
            if rnd.random() > 0.6:
                continue

            map.regionAddHex(rid, neigh_id, ToolLayer.terrain)
            make_nebula(neigh_id)




        i_nebula+=1 

