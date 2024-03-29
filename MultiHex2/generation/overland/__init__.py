from MultiHex2.master_clicker import Clicker
from .fill_land import generate_land
from .ridges import generate_ridges
from .biome_maker import add_biomes
from .make_rivers import pour_rivers

from MultiHex2.clock import Time,Clock
import json
import os
import numpy as np
from numpy.random import randint




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

    print("Using seed {}".format(seed))

    year = randint(800, 16000)
    month = randint(0,12)
    day  = randint(0,30)
    map.configure_with_clock(Clock(Time(hour=12, day=day, month=month, year=year)))

    generate_ridges(map,seed=seed, **config["mountains"]["values"])
    generate_land(map,seed=seed, **config["land"]["values"])
    map.module = "overland"
    #gen_land(map,seed=seed, **config["mountains"]["values"])
    pour_rivers(map, seed=seed, **config)
    #simulate_wind(map,seed=seed, **config)
    #simulate_clouds(map,seed=seed, **config)
    tset_file = open(os.path.join(os.path.dirname(__file__), "..","..","resources","tilesets", "main.json"),'r')
    tset = json.load(tset_file)
    tset_file.close()
    
    print("---> Assigning Tiles")
    map.apply_tileset(tset)
    add_biomes(map, seed=seed, **config)
    
