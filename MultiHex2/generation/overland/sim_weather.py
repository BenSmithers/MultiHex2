
from numpy import random as rnd
from math import sqrt, cos, sin
import numpy as np

from MultiHex2.tools import Clicker
from MultiHex2.core import screen_to_hex, HexID, hex_to_screen
from MultiHex2.core import DRAWSIZE

from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPointF

from tqdm import tqdm

from math import sqrt, pi

RTHREE = sqrt(3)

def get_step(start:HexID, end:HexID)->np.ndarray:
    """
    Returns a numpy array representing the vector pointing from `start` hex to `end` hex 
    """
    p1 = hex_to_screen(start)
    p2 = hex_to_screen(end)
    diff = p2-p1
    return np.array([diff.x(), diff.y()])

def simulate_wind(map:Clicker, seed=None, **kwargs):
    """
    Drops "streamers" along each the top left side of the map from the upper-left corner and downwards.
    At each one, it tries to find a route to the opposite side of the map, avoiding mountains.
    """
    if seed is not None:
        rnd.seed(seed)

    dimx, dimy = map.dimensions
    print("---> Simulating Wind")

    stepsize = RTHREE*DRAWSIZE
    corner = 0.5*stepsize

    horiz_points = np.arange(corner, dimy, stepsize)
    for latitude in tqdm(horiz_points):
        left = screen_to_hex(QPointF(DRAWSIZE, latitude))
        if not left in map.hexCatalog:
            raise KeyError("Something's wrong with the config, {} not in catalog".format(left))
        right = screen_to_hex(QPointF(dimx-DRAWSIZE, latitude))
        if not right in map.hexCatalog:
            raise KeyError("Something's wrong with the config, {} not in catalog".format(right))

        if latitude<0.5*dimy:
            route = map.get_route_a_star(left, right, True)
        else:
            route = map.get_route_a_star(right, left, True)
        for i in range(len(route)):
            if i==len(route)-1:
                wind = get_step(route[i-1], route[i])
            else:
                wind = get_step(route[i], route[i+1])
           
            if latitude > 0.5*dimx:
                bump = 0.25*DRAWSIZE
            else:
                bump = -0.25*DRAWSIZE
            wind[1]+=bump
            
            hexobj = map.accessHex(route[i])
            hexobj.wind = hexobj.wind + wind
            #map.addHex(hexobj, route[i])

        horiz_points = np.arange(corner, dimy*0.5, stepsize)


def get_color(rain):
    top = (50, 168, 82)
    bot = (181, 196, 118)

    return QColor(
        max(bot[0] + (top[0]-bot[0])*rain, 1),
        max(bot[1] + (top[1]-bot[1])*rain,1),
        max(bot[2] + (top[2]-bot[2])*rain,1)
    )

def simulate_clouds(map:Clicker, seed=None, **kwargs):
    """

        cloud_survival_len = 8 - number of hexes a cloud should be able to survive over land 
        cloud_regen_rate = 1 - how quickly a cloud 
    """
    if seed is not None:
        rnd.seed(seed)

    print("---> Simulating clouds")

    dimx, dimy = map.dimensions
    stepsize = RTHREE*DRAWSIZE
    corner = 0.5*stepsize
    
    c2c = 1.7320*DRAWSIZE

    horiz_points = np.arange(corner, dimy, stepsize)
    for latitude in tqdm(horiz_points):
        if latitude<0.5*dimy:
            start = screen_to_hex(QPointF(0.1*DRAWSIZE, latitude))
        else:
            start = screen_to_hex(QPointF(dimx - 0.6*DRAWSIZE, latitude))
        
        regen_rate = 0.7

        while True:
            # get shadow

            under = map.accessHex(start)
            if under is None:
                break
            mag = np.sqrt(np.sum(under.wind**2))

            factor = mag/c2c
            reservoir = 15*factor

            if reservoir>=8*factor:
                shadow = start.in_range(2)
            elif reservoir>5*factor:
                shadow = start.neighbors
            else:
                shadow = [start]
            
            step = c2c*under.wind/(np.sqrt(np.sum(under.wind**2)))
            if np.isnan(step).any():
                step = c2c*np.array([1,1])
                rot_angle = rnd.rand()*2*pi
                factor = 1.0
            else:
                # random rotation 0 +/- 15 degrees
                rot_angle = rnd.randn()*60*pi/180
            step[0] =  cos(rot_angle)*step[0]  + sin(rot_angle)*step[1]
            step[1] =  -sin(rot_angle)*step[0] + cos(rot_angle)*step[1]

            step = QPointF(step[0], step[1])
            
            nextone = screen_to_hex(hex_to_screen(start)+step)


            scale =1.0
            if map.accessHex(nextone) is not None:
                if under.is_land:
                    adiff = map.accessHex(nextone).params["altitude_base"] - under.params["altitude_base"]
                    if adiff>0.5:
                        scale = 2.0
                    elif adiff>0.1:
                        scale = 1.5
                    elif adiff>-0.05:
                        scale = 1.0
                    elif adiff >-0.2:
                        scale=0.25
                    else:
                        scale=0.05

            if reservoir>=0:
                for each in shadow:
                    dishex = map.accessHex(each)

                    if dishex is not None:
                        dishex.set_param("rainfall_base",dishex.params["rainfall_base"]+0.05*factor*scale)
                        if dishex.is_land:
                            if not (dishex.geography=="ridge" or dishex.geography=="peak" or dishex.geography=="mountain"):
                                dishex.set_fill(get_color(dishex.params["rainfall_base"]))

                reservoir-=(1*factor)/scale
            
            if not under.is_land:
                reservoir+=regen_rate
                if reservoir<10*factor:
                    reservoir+=regen_rate

            
            start = nextone
    
    return
    print("---> Smoothing")
    total = 0
    for hexID in tqdm(map.hexCatalog):
        total += 1
        if total%100 == 0:
            print("doing something...")
        rain_sum = map.hexCatalog.get(hexID).params["rainfall_base"]
        n_count = 1
        for neighbor in hexID.neighbors:
            if neighbor in map.hexCatalog:
                n_count += 1
                rain_sum += map.hexCatalog.get(neighbor).params["rainfall_base"]
        map.hexCatalog.get(hexID).set_param("rainfall_base", rain_sum/n_count)
            
                
        

def erode_land(map:Clicker, seed=None, **kwargs):
    """
    Choose a random hex on the map that's land. Look at neighbors, move to next lowest neighboring hex.
    If altitude gradient exceeds a threshold, remove eps altitude from start hex and add it to buffer
    If altitude gradient is less than threshold, remove eps from buffer and split the eps between present and subsequent hex  

    Repeat until buffer is empty. 
    """
    if seed is not None:
        rnd.seed(seed)

    
