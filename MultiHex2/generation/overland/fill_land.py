from numpy import random as rnd
from math import floor
import numpy as np

from ..utils import point_is_in, gauss
from ..utils import perlin, bilinear_interp, get_loc
from MultiHex2.tools import Clicker
from MultiHex2.core import hex_to_screen, Hex

from PyQt5.QtGui import QColor

def generate_land(map:Clicker, seed=None, **kwargs):
    if seed is not None:
        rnd.seed(seed)

    requried_args = ["land_spread","land_width","mnt_thicc","water_spread","water_width"]
    for arg in requried_args:
        if arg not in kwargs:
            raise Exception("Could not find requied arg {} in kwargs".format(arg))

    dimensions = map.dimensions

    # avearge decrease in altitude from one regular land tile to another
    land_spread     = kwargs['land_spread']
    # standard deviation 
    land_width      = kwargs['land_width']

    # average thickness of mountainness around ridgeline 
    mnt_thicc       = kwargs['mnt_thicc']

    # average decrease in elevation from water tile to another Plus its standard deviatino
    water_spread    = kwargs['water_spread']
    water_width     = kwargs['water_width']

    ids_to_propagate = list( map.hexCatalog.get_all_hids())

    while len(ids_to_propagate) != 0:
        
        parent = map.hexCatalog[ids_to_propagate[0]]
        
        if parent.genkey[0]=='1':
            perc = 0. 
        else:
            if mnt_thicc <= 1.:
                perc = 1.
            else:
                perc = 1.0/mnt_thicc
        

        if rnd.random() > (1. - perc):
            ids_to_propagate.pop(0)
        else:
            # equal probability of spreead
            neighbors = ids_to_propagate[0].neighbors
            
            sanitized_neighbors = []
            for index in range(len(neighbors)):
                if neighbors[index] not in map.hexCatalog:
                    sanitized_neighbors.append( neighbors[index] )

            # now we have a sanitized list of ids guaranted to be uninstantiated
            if len(sanitized_neighbors)==0:
                ids_to_propagate.pop(0)
                continue
            else:
                which = int(floor( len(sanitized_neighbors )*rnd.random() ))
                if which >= len(sanitized_neighbors):
                    raise Exception("wtf??? {}".format(which))
                center = hex_to_screen( sanitized_neighbors[which] )

                if not point_is_in(center, dimensions):
                    ids_to_propagate.pop(0)
                    continue

                new_hex = Hex(center)
                new_hex.genkey = '01000000'
                new_hex.set_param("altitude_base", 1.0)
                new_hex.set_param("rainfall_base",0.0)
                new_hex.is_land=True
                new_hex.geography="mountain"
                new_hex.set_fill(QColor(97, 78, 46))
                
                alt_shift = parent.params["altitude_base"] - gauss(0.25, 0.05)
                if alt_shift < 0.2:
                    new_hex.set_param("altitude_base", 0.2)
                else:
                    new_hex.set_param("altitude_base", alt_shift)

                # register the hex, add it to the appendables. 
                # if this throws an error, don't catch. That means I made logic mistakes 
                map.addHex( new_hex, sanitized_neighbors[which] )
                ids_to_propagate.append( sanitized_neighbors[which] )
                ids_to_propagate.pop(0)

    ids_to_propagate = list( map.hexCatalog.get_all_hids())

    def get_color(alt):
        top = (138, 123, 63)
        bot = (230, 217, 165)

        return QColor(
            bot[0] + (top[0]-bot[0])*alt,
            bot[1] + (top[1]-bot[1])*alt,
            bot[2] + (top[2]-bot[2])*alt
        )

    while len(ids_to_propagate)!=0:
        parent = map.hexCatalog[ids_to_propagate[0]]
        if parent.genkey[0]=='1': # can pretty much guarantee these aren't exposed
            ids_to_propagate.pop(0)
            continue
        else:
            neighbors = ids_to_propagate[0].neighbors

            sanitized_neighbors = []
            for neighbor in neighbors:
                if neighbor not in map.hexCatalog:
                    sanitized_neighbors.append( neighbor )
            
            if len(sanitized_neighbors)==0:
                ids_to_propagate.pop(0)
                continue
            else:
                # okay, so now we need to create the neighbors... 
                for neighbor in sanitized_neighbors:
                    center = hex_to_screen(neighbor)
                    if not point_is_in(center, dimensions):
                        continue

                    if parent.is_land:
                        new_alt = parent.params["altitude_base"] - gauss(land_spread, land_width)
                    else:
                        new_alt = parent.params["altitude_base"] - gauss(water_spread, water_width)

                    if new_alt > 0:
                        new_hex = Hex( center )
                        new_hex.is_land = True
                        new_hex.geography="land"
                        new_hex.set_fill(QColor(200, 160, 130))
                    else:
                        new_hex = Hex( center )
                        new_hex.is_land = False
                        new_hex.geography = "ocean"
                        new_hex.set_fill(QColor(111, 134, 168))

                    new_hex.set_param("altitude_base", new_alt)
                    new_hex.set_param("rainfall_base",0.0)
                    map.addHex( new_hex, neighbor )
                    ids_to_propagate.append( neighbor )
                ids_to_propagate.pop(0)

    def smooth():
        for hid in map.hexCatalog.get_all_hids():
            hex = map.hexCatalog[hid]
            if hex.geography=="ridge" or hex.geography=="peak" or hex.geography=="mountain":
                continue
            cu = hex.params["altitude_base"]
            total = 1
            for neigh in hid.neighbors:
                if neigh in map.hexCatalog:
                    total+=1
                    cu += map.hexCatalog[neigh].params["altitude_base"]
            

            hex.set_param("altitude_base", cu/total)

    smooth()
    smooth()

    noise = perlin(1000,seed)
    
    max_dim = max(map.dimensions)
    noise_coords = np.linspace(0,max_dim, 1000)
    print("perlin time")
    total = len(map.hexCatalog.get_all_hids())
    count = 0
    for hid in map.hexCatalog.get_all_hids():
        count +=1 
        if count%1000==0:
            print("{} of {} done".format(count, total))
        hex = map.hexCatalog[hid]
        if hex.geography=="ridge" or hex.geography=="peak" or hex.geography=="mountain":
                continue
        pos = hex_to_screen(hid)

        x_noise = 1000*int(pos.x()/max_dim)
        y_noise = 1000*int(pos.y()/max_dim)

        value = noise[x_noise][y_noise]*0.1

        new_alt = hex.params["altitude_base"]*(1+value)
        new_alt = max(min(new_alt, 1), -10)
        hex.set_param("altitude_base", hex.params["altitude_base"]*(1+value))
        alt = hex.params["altitude_base"]
        if (alt)>0:
            hex.is_land=True
            hex.geography="land"
            hex.set_fill(QColor(200, 160, 130))
        else:
            hex.is_land=False
            hex.geography="ocean"
            hex.set_fill(QColor(111, 134, 168))
        map.drawHex(hid)

