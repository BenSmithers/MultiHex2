from collections import deque
from MultiHex2.tools import Clicker
from MultiHex2.core import screen_to_hex, hex_to_screen, HexID

from numpy import random as rnd    

from PyQt5.QtCore import QPointF

from MultiHex2.core import Region
from MultiHex2.tools.basic_tool import ToolLayer
from MultiHex2.generation.name_gen import create_name


def add_biomes(map:Clicker, seed=None, **kwargs):
    print("Adding Biomes")
    if seed is not None:
        rnd.seed(seed)

    dimx, dimy = map.dimensions

    n_regions = 60
    reg_size = 25

    while len(map._biomeCatalog) < n_regions:
        spot = QPointF(dimx*rnd.random(), dimy*rnd.random())

        locid = screen_to_hex(spot)

        this_hex = map.accessHex(locid)
        if this_hex is None:
            continue

        rid = map.accessHexRegion(locid, ToolLayer.terrain)
        if rid is not None:
            continue

        if this_hex.geography == "ocean":
            if rnd.randint(1,5)!=1:
                continue

        new_region = Region(this_hex, locid)
        new_region.set_name( create_name(this_hex.geography))
        new_region.set_geography(this_hex.geography)
        print("    spreading {}".format(new_region.name))

        rid = map.addRegion(new_region, ToolLayer.terrain)

        ids_to_propagate = deque([locid, ])

        while len(ids_to_propagate)!=0:
            
            if len(map.accessRegion(rid, ToolLayer.terrain).hexIDs)>reg_size and rnd.random()>0.50:
                ids_to_propagate.popleft()
                continue
        
            neighbors = ids_to_propagate[0].neighbors
            for neighbor in neighbors:
                if len(map.accessRegion(rid, ToolLayer.terrain).hexIDs)>reg_size and rnd.random()>0.50:
                    continue
                if map.accessHexRegion(neighbor, ToolLayer.terrain) is not None:
                    continue
                if map.accessHex(neighbor) is None:
                    continue
                if map.accessHex(neighbor).geography == new_region.geography:
                    map.regionAddHex(rid, neighbor, ToolLayer.terrain)
                    ids_to_propagate.append(neighbor)

            ids_to_propagate.popleft()