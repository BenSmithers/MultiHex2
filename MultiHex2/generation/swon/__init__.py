from MultiHex2.master_clicker import Clicker

import numpy as np
import json
import os 

"""
Should follow the same general procedure as the actual Sector Generation 

    1. lay out star systems 
    2. roll for the number of planets in each one 
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

    