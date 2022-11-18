from MultiHex2.core.coordinates import screen_to_hex
from MultiHex2.modules.swon.system import System
from MultiHex2.modules.swon.world import World

from MultiHex2.core.enums import ToolLayer
from MultiHex2.master_clicker import Clicker
from MultiHex2.core.enums import OverlandRouteType

from MultiHex2.core.core import Path

from PyQt5.QtCore import QPointF


from pyparsing import alphas

from numpy import random as rnd

numbers = [str(each) for each in range(10)]
letters = list(set(alphas.upper()))

"""
Systems should have a max number of hyperlane routes they can establish based on their population 
    4   - 0
    6   - 0 
    9   - 1 
    11  - 2 hyperlanes

For each system we consider the value of connecting with other system
    - distance suppresses the cost 
    - largest jump effects cost. Max 1 has no effect, max 2 has small penalty, max 3 has big penalty, anything more than that makes the route worthless 
    - certain World Tags can increase the value 
Then we choose the top N value systems and connect them with routes 
"""

MIN_POP = 8
TWO_POP = 10

def add_hyperlanes(map:Clicker,seed=None, **kwargs):
    """
        This step just fills in the map with hexes and some nebulae 
    """
    if seed is not None:
        rnd.seed(seed)
    else:
        seed = rnd.randint(1,10000000)

    requried_args = []
    for arg in requried_args:
        if arg not in kwargs:
            print(kwargs)
            raise Exception("Could not find requied arg {} in kwargs".format(arg))

    
    for eid in range(map.nextFreeEID()):
        this_system = map.accessEid(eid)

        assert isinstance(this_system, System), "Found non-system entity?? {}".format(this_system)

        primary_world = this_system.get_primary_world()
        if primary_world._population_raw<MIN_POP:
            continue
            

        available_goods = primary_world.list_available_goods()

        start_hid = map.get_eid_loc(eid)

        possible_routes = []

        for other_eid in range(map.nextFreeEID()):
            # check all the other systems 
            if eid==other_eid:
                continue

            dest_hid = map.get_eid_loc(other_eid)

            distance = abs(dest_hid - start_hid)

            # skip them if they're too far away to be profitable 
            if distance > 3: 
                continue
            if distance == 0:
                continue

            other_world = map.accessEid(other_eid).get_primary_world()

            # calculate the possible profit we can gain by moving each available good from here to the other world 
            for good in available_goods:
                pp = primary_world.get_purchase_price(good)
                sp = other_world.get_sale_price(good)

                profit = (sp - pp) / distance
                
                # if there is profit, consider it for sales! 
                if profit > 0:
                    possible_routes.append([start_hid, dest_hid, good, profit ])

        if len(possible_routes)>0:
            # now we sort our possible routes 
            # we use the negative since sorted does low->high 
            possible_routes = sorted(possible_routes, key = lambda x: -1*x[-1])
            route = map.get_route_a_star(possible_routes[0][0], possible_routes[0][1], OverlandRouteType.aerial)
            if len(route)==0:
                print(possible_routes[0])

            new_path = Path(*route)
            new_path.name = "{} Hyperlane".format(possible_routes[0][2].name)
            map.register_path(new_path, ToolLayer.civilization)

        if len(possible_routes)>1:
            if primary_world._population_raw>TWO_POP:
                route = map.get_route_a_star(possible_routes[1][0], possible_routes[1][1], OverlandRouteType.aerial)

                new_path = Path(*route)
                new_path.name = "{} Hyperlane".format(possible_routes[1][2].name)
                map.register_path(new_path, ToolLayer.civilization)
            

    map.update()