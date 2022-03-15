from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF, QColor
from math import sqrt,sin,cos
from PyQt5.QtWidgets import QGraphicsItem

from core.coordinates import HexID, hex_to_screen, DRAWSIZE

import numpy as np
from numpy.random import randint

RTHREE = sqrt(3)

class Hex(QPolygonF):
    def __init__(self, center:QPointF):
        """
        Construct like a polygon, must pass a list of QPointF objects 
        """
        points = [
            QPointF(center.x()+DRAWSIZE, center.y()),
            QPointF(center.x()+DRAWSIZE*0.5, center.y()+DRAWSIZE*0.5*RTHREE),
            QPointF(center.x()-DRAWSIZE*0.5, center.y()+DRAWSIZE*0.5*RTHREE),
            QPointF(center.x()-DRAWSIZE, center.y()),
            QPointF(center.x()-DRAWSIZE*0.5, center.y()-DRAWSIZE*0.5*RTHREE),
            QPointF(center.x()+DRAWSIZE*0.5, center.y()-DRAWSIZE*0.5*RTHREE)
        ]
        super().__init__(points)

        # store relevant hex parameters. These will be set by the brushes, adjusters, generators, etc. 
        # used to store any special parameters 
        self._params = {}
        self._fill = QColor(255,255,255)
        self.x = center.x()
        self.y = center.y()
        self.genkey = '0000'
        self.geography = ""
        self.is_land = False
        self.wind = np.zeros(2)

    @property 
    def center(self):
        return QPointF(self.x, self.y)

    @property
    def params(self):
        return self._params
    @property
    def fill(self)->QColor:
        return self._fill

    def set_fill(self, fill:QColor):
        self._fill = fill
    def set_params(self, params:dict):
        self._params = params
    def set_param(self, param:str, value:float):
        self._params[param] = value
    
    def get_cost(self, other:'Hex', ignore_water=False):
        """
        Gets the cost of movement between two hexes. Used for routing
        """
        # xor operator
        # both should be land OR both should be water
        if (self.is_land ^ other.is_land) and not ignore_water:
            water_scale = 5.
        else:
            water_scale = 1.


        # prefer flat ground!
        lateral_dist=(self.center - other.center)
        lateral_dist = lateral_dist.x()*lateral_dist.x() + lateral_dist.y()*lateral_dist.y()

        mtn_scale =1.0
        if other.geography=="peak" or other.geography=="ridge":
            mtn_scale=100.0
        elif other.geography=="mountain":
            mtn_scale=50.0
        

        alt_dif = abs(10*(other.params["altitude_base"] - self.params["altitude_base"])) if self.is_land else 0.

        return(mtn_scale*water_scale*(0.1*lateral_dist + DRAWSIZE*RTHREE*alt_dif))

    def get_heuristic(self, other:'Hex'):
        """
        Estimates the total cost of going from this hex to the other one
        """
        lateral_dist = (self.center - other.center)
        lateral_dist= lateral_dist.x()*lateral_dist.x() + lateral_dist.y()*lateral_dist.y()
        alt_dif = abs(2*(other.params["altitude_base"] - self.params["altitude_base"]))
        return(0.1*lateral_dist + DRAWSIZE*RTHREE*alt_dif)

    def pack(self)->dict:
        """
        Takes the hex object and save the essentials such that this can be reconstructed later. 
        """
        vals = {
            "red":self.fill.red(),
            "green":self.fill.green(),
            "blue":self.fill.blue(),
            "params":self.params,
            "x":self.x,
            "Y":self.y,
            "geo":self.geography,
            "wind":list(self.wind)
        }
        return vals
    @classmethod
    def unpack(cls, obj:dict)->'Hex':
        """
        Alternate of `pack` function. 
        """
        new_hx = Hex(QPointF(obj["x"], obj["Y"]))
        new_hx._fill = QColor(obj["red"], obj["green"], obj["blue"])
        new_hx._params = obj["params"]
        new_hx.geography=obj["geo"]
        new_hx.wind = np.array(obj["wind"])
        return new_hx

class Region(QPolygonF):
    """
    Regions are just two polygons, merged together
    """
    def __init__(self, origin:QPolygonF, *hexIDs:HexID):
        super().__init__(origin)
        self._name = ""
        self._hexIDs = list(hexIDs)
        self._fill = QColor(randint(1,255),randint(1,255),randint(1,255))

    @property
    def hexIDs(self)->list:
        return self._hexIDs
    @property
    def name(self)->str:
        return self._name
    @property
    def fill(self)->QColor:
        return self._fill

    def pack(self)->dict:
        """
            Converts the Region into a dictionary that can later be unpacked with the 'unpack' function 
        """
        hids = {
            "xids":[hid.xid for hid in self._hexIDs],
            "yids":[hid.yid for hid in self._hexIDs]
        }
        points = []
        for pt in range(len(self)):
            points.append([ self[pt].x(), self[pt].y()])
        return {
            "vertices":points,
            "hIDs":hids,
            "name":self._name,
            "red":self.fill.red(),
            "green":self.fill.green(),
            "blue":self.fill.blue()
        }
    @classmethod
    def unpack(cls, packed:dict)->'Region':
        verts = [QPointF(item[0], item[1]) for item in packed["vertices"]]
        hIDs = [HexID(packed["hIDs"]["xids"][i], packed["hIDs"]["yids"][i]) for i in range(len(packed["hIDs"]["yids"]))]
        new_reg = Region(QPolygonF(verts), *hIDs)
        new_reg._name = packed["name"]
        new_reg._fill=QColor(packed["red"], packed["green"], packed["blue"])
        return new_reg

    def set_name(self, name:str):
        self._name = name

    def merge(self, other:'Region')->'Region':
        """
        Combines the regions together, returns Region
        """
        combined = self.united(other)
        new = Region(combined, *self._hexIDs)
        new._hexIDs += other.hexIDs
        new._name = self._name
        new._fill = self._fill
        return new

    def subtract(self, other:'Region')->'Region':
        combined = self.subtracted(other)
        new = Region(combined,*self._hexIDs)
        #new._hexIDs += other.hexIDs
        for id in other.hexIDs:
            if id in self._hexIDs:
                new._hexIDs.remove(id)

        new._name = self._name
        new._fill = self._fill
        return new

class RegionCatalog:
    """
    Object for keeping track of Regions and the hexes that encompass them 
    """
    def __init__(self):
        self._hidcatalog = {} # hexID -> regionID
        self._ridcatalog = {} # regionID -> Region
        self._interface = {} # regionID -> screenID

    def __contains__(self, rid):
        return rid in self._ridcatalog

    def getSID(self, id):
        """
        Gets the scene id for the region atthe specified HexID/Region ID
        """
        if isinstance(id, HexID):
            if id not in self._hidcatalog:
                return
            elif self._hidcatalog[id] not in self._interface:
                return
            else:
                return self._interface[self._hidcatalog[id]]
        elif isinstance(id, int): #region id
            if id not in self._interface:
                return
            else:
                return self._interface[id]
        else:
            raise TypeError("Not sure what to do with {}".format(type(id)))
    def get_region(self, rid)->Region:
        """
        Returns region for a region ID
        """
        if rid in self._ridcatalog:
            return self._ridcatalog[rid]
        else:
            return 
    def get_rid(self, id:HexID)->int:
        """
        Returns Region ID for a hex id, or returns None if the hex isn't in a region
        """
        if id in self._hidcatalog:
            return self._hidcatalog[id]
        else:
            return
    def get_sid(self, rid:int):
        """
            return the screen id if the region has an entry, otherwise returns NONE
        """
        if rid in self._interface:
            return self._interface[rid]
        else: 
            return

    def updateSID(self, rid:int, sid):
        self._interface[rid] = sid

    def updateRegion(self, rid:int, region:Region):
        self._ridcatalog[rid] = region

    def get_next_rid(self):
        rid = 1
        while rid in self._ridcatalog:
            rid+=1
        return rid

    def register_region(self, region:Region)->int:
        """
        Takes a region and the hexes that start as part of it, register them in the dictionaries 
        """
        rid = self.get_next_rid()

        self._ridcatalog[rid] = region

        for id in region.hexIDs:
            self._hidcatalog[id]=rid

        return rid
    def delete_region(self, rID:int):
        for hexID in self._ridcatalog[rID].hexIDs:
            del self._hidcatalog[hexID]

        del self._ridcatalog[rID]
        del self._interface[rID]

    def add_hex(self, hID:HexID, rID:int):
        self._hidcatalog[hID] = rID

    def remove_hex(self, hID:HexID):
        """
            Subtracts from the hex
        """
        rid = self._hidcatalog[hID]
        if hID not in self._hidcatalog:
            return

        del self._hidcatalog[hID]

        region = self._ridcatalog[rid]
        region = region.subtract(Region(Hex(hex_to_screen(hID)), hID))
        self._ridcatalog[rid] = region

        if (region.hexIDs)==0:
            self.delete_region(rid)

    def __iter__(self):
        return self._ridcatalog.__iter__()

    def __getitem__(self, key)->Region:
        return self._ridcatalog[key]


class Catalog:
    _dtype = Hex
    def __init__(self, dtype:type):
        Catalog._dtype = dtype
        self._hidcatalog = {} # hex id -> obj
        self._interface = {} # hexid to screen id

    def get_all_hids(self):
        return self._hidcatalog.keys()

    def updateSID(self, hID:HexID, sid=None):
        if sid is None:
            del self._interface[hID]     
        else:
            self._interface[hID] = sid

    def getSID(self,hID:HexID)->QGraphicsItem:
        if hID in self._interface:
            return self._interface[hID]
        else:
            return

    def remove(self, hid:HexID):
        """
        Remove from catalog
        """
        if hid in self._hidcatalog:
            del self._hidcatalog[hid]
            self._hidcatalog[hid] = None
        else:
            raise ValueError("Error, QGraphicsItem {} not in catalog.".format(hid))

        if hid in self._interface:
            sid = self._interface[hid]
            self._interface[hid] = None
        else:
            raise ValueError("Tried removing hexID {} from catalog, but no entry found in interface".format(hid))
    

    def register(self, item:_dtype, hid:HexID):
        """
        Called when we're registering 
        """
        self._hidcatalog[hid] = item
        self._interface[hid] = None
            

    def __getitem__(self, key)->_dtype:
        return self._hidcatalog[key]

    def __contains__(self, key)->bool:
        return key in self._hidcatalog

    def __iter__(self):
        return self._hidcatalog.__iter__()