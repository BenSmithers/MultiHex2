import json
import os

from MultiHex2.generation.utils import Table

_fname = os.path.join(os.path.dirname(__file__), "..","..","resources","swon_data.json")
_obj = open(_fname, 'r')
_data = json.load(_obj)
_obj.close()

atmo = Table()
for key in _data["atmosphere"]:
    atmo.add_entry(_data["atmosphere"][key]["min"], "{} - {}".format(key, _data["atmosphere"][key]["text"]))

temp = Table()
for key in _data["temperature"]:
    temp.add_entry(_data["temperature"][key]["min"], "{} - {}".format(key, _data["temperature"][key]["text"]))

bio = Table()
for key in _data["biosphere"]:
    bio.add_entry(_data["biosphere"][key]["min"], "{} - {}".format(key, _data["biosphere"][key]["text"]))

tl = Table()
for key in _data["tech level"]:
    tl.add_entry(_data["tech level"][key]["min"], "TL{} - {}".format(key, _data["tech level"][key]["text"]))

pop = Table()
for key in _data["population"]:
    pop.add_entry(_data["population"][key]["min"], _data["population"][key]["text"])
