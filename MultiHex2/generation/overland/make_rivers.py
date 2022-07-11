from numpy import random as rnd

from MultiHex2.tools import Clicker
from MultiHex2.core import screen_to_hex, HexID, hex_to_screen
from MultiHex2.core.core import Hex, River
from MultiHex2.core.coordinates import get_adjacent_hexIDs, get_adjacent_vertices, get_IDs_from_step
from MultiHex2.generation.name_gen import create_name

from PyQt5.QtCore import QPointF
from PyQt5 import QtGui
from copy import deepcopy
from MultiHex2.tools.basic_tool import ToolLayer

"""
River idea: 
    have the river go greedily downhill
    if the river sees it can only go up, make the hex directly forward from it into a "lake" tile with the same altitude. 
    Then do a outwards fill from that lake tile turning every land tile beside it into lake tiles as well
    Then with the river, pop off the end of it until the end is adjacent to the lake (or at least not next to a lake)
"""


def near_water(map, point:QPointF):
    ids = get_adjacent_hexIDs(point)
    are_land = [map.hexCatalog.get(id).is_land for id in ids]

    # if all are land, return False
    # if any are water, return True
    return not all(are_land)

def meta_river_merge(map, pid1:int, pid2:int):
    river1 = map.get_path_cat(ToolLayer.terrain).get(pid1)
    river2 = map.get_path_cat(ToolLayer.terrain).get(pid2)

    map.remove_path(pid1, ToolLayer.terrain)
    map.remove_path(pid2, ToolLayer.terrain)

    river1.merge_with(river2)

    map.register_path(river1, ToolLayer.terrain)




def _pour_river(map, where=None):
    dimx, dimy = map.dimensions

    def average_alt_around_vertex(where:QPointF)->float:        
        n_included = 0
        total = 0.0
        for hid in get_adjacent_hexIDs(where):
            if hid in map.hexCatalog:
                n_included += 1
                total += map.hexCatalog.get(hid).params["altitude_base"]
        
        if n_included==0:
            raise ValueError("Tried getting average of vertex away from map: {}".format(where))

        return total/n_included

    def make_hex_into_lake(id:HexID, net_alt):
        map.hexCatalog.get(id).geography = "lake"
        map.hexCatalog.get(id).set_param("altitude_base", net_alt/3.0)
        map.hexCatalog.get(id).set_param("is_land", 0.0)
        map.hexCatalog.get(id).is_land = False
        map.hexCatalog.get(id).set_fill(QtGui.QColor( 122, 177, 204 ))
        map.drawHex(id)

    if where is not None:
        sample_point = where
    else:
        sample_point = QPointF( (rnd.random()*0.8+0.1)*dimx , (rnd.random()*0.8+0.1)*dimy)
    this_hexid = screen_to_hex(sample_point)

    # we make a hex object to get its vertices
    this_hex = map.hexCatalog.get(this_hexid)
    if not this_hex.is_land:
        return 1

    start_vertex = this_hex[rnd.randint(0,6)] # this _should_ be a QPointF
    if near_water(map, start_vertex):
        return 1

    new_river = River(start_vertex)
    new_river.name = create_name("river")
    """
        1. Get river end. Check neighboring hexes; if one is ocean or map-edge, END
        2. Get neighboring vertices. For each vertex, check hexes around it and average the altitudes
        3. 
    """
    make_lake = False
    while True:
        end_pt = new_river.get_end()
        adjacent_hexes = get_adjacent_hexIDs(end_pt)

        # ------------- IF neighbors are ocean or unmapped, end here! 
        done = False
        for each in adjacent_hexes:
            if each not in map.hexCatalog:
                done = True
                break
            elif not map.hexCatalog.get(each).is_land:
                done = True
                break
        if done:
            break

        # --------------- Figure out neighboring altitudes
        verts = get_adjacent_vertices(end_pt)
        alt_here = average_alt_around_vertex(end_pt)
        eff_alts = [average_alt_around_vertex(vert) for vert in verts]

        i_choice = -1
        choice_alt = 1000000
        for i_neighbor in range(len(verts)):
            if len(new_river)!=1:
            # --------- make sure this neighbor vertex isn't on the path
                is_on = new_river.get_diff( new_river.vertices[-2], verts[i_neighbor]) < 1e-6
                if is_on: 
                    continue

            if eff_alts[i_neighbor]<alt_here: # if downhill
                if eff_alts[i_neighbor]<choice_alt: # if MORE downhill than other direction
                    i_choice = i_neighbor
                    choice_alt = eff_alts[i_choice]
            
        # nothing is downhill
        if i_choice==-1:
            # START LAKE FORMATION 
            make_lake = True
            break 

        # ---------- add the chosen vertex to the river 

        new_river.add_to_end(verts[i_choice])

        # ---------- check if we can merge! 
        
    # get the rivers near the end of this path 
    hex_ids_here = get_adjacent_hexIDs(verts[i_choice])
    pids_here = []
    for hid in hex_ids_here:
        pids_here += map.get_path_cat(ToolLayer.terrain).paths_here(hid)
    pids_here = list(set(pids_here))

    for pid in pids_here:
        other_river = deepcopy(map.get_path_cat(ToolLayer.terrain).get(pid))

        can_merge = other_river.check_contains(new_river.get_end())
        if can_merge:
            map.remove_path(pid, ToolLayer.terrain)

            other_river.merge_with(new_river)
            map.register_path(other_river, ToolLayer.terrain)

            return 5 
        # check! 

    if make_lake:
        
        if len(new_river)==1:
            hids = get_adjacent_hexIDs(new_river.get_end())

            net_alt = 0.0
            for id in hids:
                net_alt += map.hexCatalog.get(id).params["altitude_base"]
            for id in hids:
                make_hex_into_lake(id, net_alt)
            
            return 2
        elif len(new_river)==0:
            raise ValueError("Unreachable!")
        else:
            step = new_river.get_end() + new_river.get_end() - new_river.vertices[-2]
            start_hex = screen_to_hex(step)

            compare_to = map.hexCatalog.get(start_hex).params["altitude_base"]
            make_hex_into_lake(start_hex, compare_to)

            # okay, now pop the end off the lake until the neihbor hexes aren't lake hexes 
            while True:
                left,right = get_IDs_from_step(new_river.get_end(), new_river.vertices[-2])
                left_land  = map.hexCatalog.get(left).is_land
                right_land  = map.hexCatalog.get(right).is_land

                if left_land and right_land:
                    break
                else:
                    new_river.pop_from_end()
                    if len(new_river) <=1:
                        break

    if len(new_river)==1:
        return 2

    map.register_path(new_river, ToolLayer.terrain)
    return 0


def pour_rivers(map:Clicker, seed=None, **kwargs):

    n_rivers = 20
    if seed is not None:
        rnd.seed(seed)

    n_done = 0
    while n_done < n_rivers:
        
        new_river_result =  _pour_river(map)
        if new_river_result==0:
            n_done += 1