
from numpy import random as rnd
from math import sqrt
import numpy as np

from ..utils import point_is_in, gauss
from ..utils import perlin, bilinear_interp, get_loc
from MultiHex2.tools import Clicker
from MultiHex2.core import Hex, screen_to_hex, HexID, hex_to_screen
from MultiHex2.core import DRAWSIZE

from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPointF

from math import sqrt

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
    print("{} vs {}".format(dimx, dimy))

    stepsize = RTHREE*DRAWSIZE
    corner = 0.5*stepsize

    horiz_points = np.arange(corner, dimy, stepsize)
    print("Doing {} streamers".format(len(horiz_points)))
    for latitude in horiz_points:
        left = screen_to_hex(QPointF(DRAWSIZE, latitude))        
        right = screen_to_hex(QPointF(dimx, latitude-1))
        route = map.get_route_a_star(left, right, True)
        for i in range(len(route)):
            if i==len(route)-1:
                wind = get_step(route[i-1], route[i])
            else:
                wind = get_step(route[i], route[i+1])
            
            hexobj = map.accessHex(route[i])
            hexobj.wind = hexobj.wind + wind
            map.addHex(hexobj, route[i])


def simulate_clouds(map:Clicker, seed=None, **kwargs):
    """

        cloud_survival_len = 8 - number of hexes a cloud should be able to survive over land 
        cloud_regen_rate = 1 - how quickly a cloud 
    """
    if seed is not None:
        rnd.seed(seed)




def erode_land(map:Clicker, seed=None, **kwargs):
    """
    Choose a random hex on the map that's land. Look at neighbors, move to next lowest neighboring hex.
    If altitude gradient exceeds a threshold, remove \eps altitude from start hex and add it to buffer
    If altitude gradient is less than threshold, remove \eps from buffer and split the \eps between present and subsequent hex  

    Repeat until buffer is empty. 
    """
    if seed is not None:
        rnd.seed(seed)

    
