from MultiHex2.master_clicker import Clicker

import numpy as np
import json
import os 

"""
Should follow the same general procedure as the actual Sector Generation 

    1. lay out star systems 
    2. roll for the number of planets in each one 


 5/16 hexes should have star systems. We should also use Perlin noise to generate a PDF for star system selection so there is a natural "clumping" of sectors 
    1. Choose position randomly
    2. Generate number (0,1), and sample from perlin noise there. If RNG is < perlin noise, keep the point. 
    3. Get hexID here. If hex already has star system here, check neighbors for empty hex (choose random neighbor start point)
"""

def fullsim(map:Clicker, **kwargs):
    if "config" in kwargs:
        config = kwargs["config"]
    else:
        _f = open(os.path.join(os.path.dirname(__file__), "config.json"),'r')
        config = json.load(_f)
        _f.close()

    if "seed" in kwargs:
        seed = np.random.randint(1,100000000)
    else:
        seed = kwargs["seed"]

    