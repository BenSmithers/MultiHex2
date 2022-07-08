from numpy import random as rnd

from MultiHex2.tools import Clicker
from MultiHex2.core import screen_to_hex, HexID, hex_to_screen
from MultiHex2.core.core import Hex, River
from MultiHex2.core.coordinates import get_adjacent_hexIDs, get_adjacent_vertices

from PyQt5.QtCore import QPointF

from MultiHex2.tools.basic_tool import ToolLayer

"""
River idea: 
    have the river go greedily downhill
    if the river sees it can only go up, make the hex directly forward from it into a "lake" tile with the same altitude. 
    Then do a outwards fill from that lake tile turning every land tile beside it into lake tiles as well
    Then with the river, pop off the end of it until the end is adjacent to the lake (or at least not next to a lake)
"""

def near_water(map:Clicker, point:QPointF):
    ids = get_adjacent_hexIDs(point)
    are_land = [map.hexCatalog.get(id).is_land for id in ids]

    # if all are land, return False
    # if any are water, return True
    return not all(are_land)

def meta_river_merge(map:Clicker, pid1:int, pid2:int):
    river1 = map.get_path_cat(ToolLayer.terrain).get(pid1)
    river2 = map.get_path_cat(ToolLayer.terrain).get(pid2)

    map.remove_road(pid1, ToolLayer.terrain)
    map.remove_road(pid2, ToolLayer.terrain)

    river1.merge_with(river2)

    map.register_path(river1, ToolLayer.terrain)

def pour_rivers(map:Clicker, seed=None, **kwargs):

    n_rivers = 5
    if seed is not None:
        rnd.seed(seed)

    n_done = 0
    while n_done < n_rivers:
        dimx, dimy = map.dimensions
        
        sample_point = QPointF( (rnd.random()*0.8+0.1)*dimx , (rnd.random()*0.8+0.1)*dimy)
        this_hexid = screen_to_hex(sample_point)

        # we make a hex object to get its vertices
        this_hex = map.hexCatalog.get(this_hexid)
        if not this_hex.is_land:
            continue

        start_vertex = this_hex[rnd.randint(0,6)] # this _should_ be a QPointF
        if near_water(start_vertex):
            continue

        new_river = River(start_vertex)
        """
            1. Get river end. Check neighboring hexes; if one is ocean or map-edge, END
            2. Get neighboring vertices. For each vertex, check hexes around it and average the altitudes
            3. 
        """
        while True:
            verts = get_adjacent_vertices(new_river.get_end())
            
            eff_alts = []
            for vert in verts:
                neighbor = get_adjacent_hexIDs(vert)



        n_done += 1