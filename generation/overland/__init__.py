from .sim_weather import simulate_wind,simulate_clouds
from MultiHex2.tools import Clicker
from .from_platec import gen_land

import json
import os
import numpy as np
_f = open(os.path.join(os.path.dirname(__file__), "config.json"),'r')
_config = json.load(_f)
_f.close()



def fullsim(map:Clicker, preset="continental"):
    config = _config[preset]
    seed = np.random.randint(1,100000000)

    #generate_ridges(map, **config["mountains"]["values"])
    #generate_land(map, **config["land"]["values"])
    gen_land(map,seed=seed, **config["mountains"]["values"])
    simulate_wind(map,seed=seed, **config)
    simulate_clouds(map,seed=seed, **config)
    for id in map.hexCatalog.get_all_hids():
        map.drawHex(id)
