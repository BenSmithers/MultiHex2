"""
Generate ridgelines  and mountains
"""

from argparse import ArgumentError
from MultiHex2.tools import Clicker
from MultiHex2.core import hex_to_screen, screen_to_hex, Hex
from MultiHex2.core import DRAWSIZE
from ..utils import point_is_in, get_distribution, gauss

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor

import numpy.random as rnd
from math import pi, acos

def generate_ridges(map:Clicker, seed=None, **kwargs):
    """
    Generates the ridgelines, can provide an optional seed
    """
    if seed is not None:
        rnd.seed(seed)

    requried_args = ["dimx","dimy","n_peaks","zones","sigma","avg_range"]
    for arg in requried_args:
        if arg not in kwargs:
            raise ArgumentError("Could not find requied arg {} in kwargs".format(arg))

    dimensions = [kwargs['dimx'],kwargs['dimy']]
    n_peaks = kwargs['n_peaks']
    zones = kwargs['zones']
    sigma       = kwargs['sigma']
    avg_range   = kwargs['avg_range']

    angles = [330., 30., 90., 150., 210., 270.]
    
    map.dimensions=tuple(dimensions)

    def make_continent():
        print("making continent")
        ids_to_propagate = []
        x_center = 0.60*rnd.random()*dimensions[0] + 0.20*dimensions[0]
        y_cos  = 1.8*rnd.random() - 0.9
        y_center = acos( y_cos )*dimensions[1]/( pi )
        for j in range(n_peaks):
            while True:
                place = QPointF( gauss( x_center, 300), gauss( y_center, 300) )
                if not point_is_in(place, dimensions):
                    print("Failed at {} {}".format(place.x(), place.y()))
                    continue 
                
                loc_id = screen_to_hex( place )
                new_hex_center = hex_to_screen( loc_id )

                new_hex = Hex(new_hex_center)
                new_hex.genkey = '11000000'
                new_hex._fill = QColor(99,88,60)
                new_hex.set_param("altitude_base",1.0)
                new_hex.set_param("rainfall_base",0.0)
                new_hex.geography="peak"
                new_hex.is_land = True
                if map.accessHex(loc_id) is None:
                    map.addHex( new_hex, loc_id )
                    ids_to_propagate.append( loc_id )
                    new_hex = None
                    break
                    
        direction = 360*rnd.random()

        # build the neighbor function
        distribution = get_distribution( direction, sigma)
        neighbor_weights = [ distribution( angle ) for angle in angles]

        # calculate CDF of neighbor weights 
        neighbor_cdf = [0. for weight in neighbor_weights]
        for index in range(len(neighbor_weights)):
            if index == 0:
                neighbor_cdf[0] = neighbor_weights[0]
            else:
                neighbor_cdf[index] = neighbor_cdf[index - 1] + neighbor_weights[index]

        print("spreading sturff now")
        while len(ids_to_propagate)!=0:
            if rnd.random()>(1.-(1./avg_range)):
                #terminate this ridgeline
                ids_to_propagate.pop()
                continue
            else:
                index = 0 
                die_roll = rnd.random()
                while neighbor_cdf[index]<die_roll:
                    index += 1
                # scan over until you find the one corresponding to this die roll

                target_ids = ids_to_propagate[-1].neighbors
                target_id = target_ids[index]

                place = hex_to_screen( target_id )
                if not point_is_in(place, dimensions):
                    print("not here!")
                    ids_to_propagate.pop(0)
                    continue
            
                new_hex = Hex( place )
                new_hex.genkey = '11000000'
                new_hex._fill = QColor(99,88,60)
                new_hex.is_land=True
                new_hex.set_param("altitude_base",0.98)
                new_hex.set_param("rainfall_base",0.0)
                new_hex.geography="ridgeline"
            

                if map.accessHex(target_id) is None:
                    map.addHex( new_hex, target_id)
                    ids_to_propagate.pop()
                    ids_to_propagate.append( target_id )
                    new_hex = None
                    continue
    for i in range(zones):
        make_continent()
