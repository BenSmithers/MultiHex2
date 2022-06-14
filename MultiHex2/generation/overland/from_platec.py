
from argparse import ArgumentError
from MultiHex2.tools import Clicker
from MultiHex2.core import hex_to_screen, screen_to_hex, Hex
from MultiHex2.core import DRAWSIZE
from ..utils import perlin

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor

import numpy.random as rnd
import numpy as np
from math import pi, acos, exp, sin


import platec

def sigmoid(val):
    return 1./(1+exp(-val))

def get_color(alt):
        top = (138, 123, 63)
        bot = (230, 217, 165)

        return QColor(
            bot[0] + (top[0]-bot[0])*alt,
            bot[1] + (top[1]-bot[1])*alt,
            bot[2] + (top[2]-bot[2])*alt
        )

def gen_land(map:Clicker, seed=None, **kwargs):
    """
    Generates the ridgelines, can provide an optional seed
    """
    if seed is not None:
        rnd.seed(seed)
    else:
        seed = rnd.randint(1,10000)

    requried_args = ["dimx","dimy"]
    for arg in requried_args:
        if arg not in kwargs:
            raise ArgumentError("Could not find requied arg {} in kwargs".format(arg))

    scale = 5
    dimensions = [kwargs['dimx'],kwargs['dimy']]   
    map.dimensions=tuple(dimensions)

    sea_level = 0.65

    print("doing platec stuff, seed {}".format(seed))
    # these were some of the generation presets, decided against changing them, not sure what they all do
            # seed, width, height, sea_level, erosion_period, folding_ratio, aggr_overlap_abs, aggr_overlap rel, cycle count, number of plates
    p = platec.create(seed, int(dimensions[1]/scale), int(dimensions[0]/scale),sea_level, 61, 0.010, 5000, 0.10, 2, 8)
    print("starting")
    while platec.is_finished(p)==0: 
        platec.step(p)

    heightmap  = np.reshape( platec.get_heightmap(p), (int(dimensions[0]/scale), int(dimensions[1]/scale) ))
    peak = np.max(heightmap)
    trough = np.min(heightmap)
    print("Min/max alt {} and {}".format( 2*sigmoid(trough-sea_level)-1.0,  2*sigmoid(peak-sea_level)-1.0 ))
    pnoise = perlin(dimensions[0],octave=5, seed=seed)
    pnoise += perlin(dimensions[0],octave=10, seed=seed)
    pnoise += perlin(dimensions[0],octave=2, seed=seed) 

    pnoise += 0.5

    print("Max alt and min alt: {}, {}".format(trough, peak))
    for i in range(len(heightmap)):
        for j in range(len(heightmap[i])):
            pos = QPointF(scale*i, scale*j)
            loc = screen_to_hex(pos)

            if loc not in map.hexCatalog:
                new_hex = Hex(hex_to_screen(loc))

                new_hex.set_param("is_land", 10*int(heightmap[i][j]>sea_level))
                new_hex.is_land=heightmap[i][j]>sea_level  

                new_hex.set_param("altitude_base",  2*sigmoid(heightmap[i][j]-sea_level)-1.0 )
                new_hex.set_param("rainfall_base",0.0)
                fract = 0.00 - heightmap[i][j]/(2*peak) # will range from -0.5 to 0.00, use it to make high places colder
                new_hex.set_param("temperature_base",pnoise[i][j]*0.3 + fract + sin(pi*j/len(heightmap[i])) )

                if heightmap[i][j]>16:
                    new_hex.geography="ridge"
                    new_hex.set_fill(QColor(99,88,60))
                elif heightmap[i][j]>3.2:
                    new_hex.geography="mountain"
                    new_hex.set_fill(QColor(97, 78, 46))
                else:
                    if new_hex.is_land:
                        new_hex.set_fill(QColor(153, 171, 104))
                    else:
                        new_hex.set_fill(QColor(135, 208, 232))

                map.addHex(new_hex, loc)
