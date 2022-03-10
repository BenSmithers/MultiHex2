from .ridges import generate_ridges
from MultiHex2.tools import Clicker

import json
import os
_f = open(os.path.join(os.path.dirname(__file__), "config.json"),'r')
_config = json.load(_f)
_f.close()



def fullsim(map:Clicker, preset="continental"):
    config = _config[preset]

    generate_ridges(map, **config["mountains"]["values"])
