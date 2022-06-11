from .baseactions import MapAction
from MultiHex2.core import Hex

from PyQt5.QtWidgets import QGraphicsScene

class Add_Remove_Hex(MapAction):
    def __init__(self, **kwargs):
        """
        This action addds hexes to the map where there was either 
            1. a hex already there 
            2. no hex already there 
        """
        MapAction.__init__(self, recurring=None,**kwargs)

        self.needed = ["hexID","hex"]
        self.verify(kwargs)
        self.newHex = kwargs["hex"]
        self.hexID = kwargs["hexID"]
        if not isinstance(self.newHex, Hex) and (self.newHex is not None):
            raise TypeError("AddHex actions require {} or {}, not {}".format(Hex, None, type(self.newHex)))

        self._drawtype = True
    

    def __call__(self, map:QGraphicsScene):
        if (self.hexID not in map.hexCatalog) and (self.newHex is None):
            raise ValueError("Tried removing hex from tile that doesn't exist.")
        
        # we set aside what was already there (if anything), and tell the map to get rid of it. 
        # then we register the new hex and make the inverter function 
        if self.hexID in map.hexCatalog:
            old_hex = map.hexCatalog[self.hexID]
            map.removeHex(self.hexID)
        else:
            old_hex = None

    
        if isinstance(self.newHex, Hex):
            map.addHex(self.newHex, self.hexID)
        
        return Add_Remove_Hex(hex=old_hex, hexID=self.hexID)