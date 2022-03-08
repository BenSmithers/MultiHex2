from textwrap import indent
from turtle import hideturtle
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF, QColor
from math import sqrt,sin,cos
from PyQt5.QtWidgets import QGraphicsItem

from core.coordinates import HexID, hex_to_screen, screen_to_hex

from numpy.random import randint

RTHREE = sqrt(3)
DRAWSIZE = 30.

def save(clicker, filename:str):
    """
    Saves the clicker state to a file 
    """
    out_dict = {"hexes":{}}
    hexes = clicker._hexCatalog
    for hID in hexes._hidcatalog:
        hex=hexes._hidcatalog[hID]
        hex_dict = {
            "red":hex.fill.red(),
            "green":hex.fill.green(),
            "blue":hex.fill.blue(),
            "params":hex.params
        }


        out_dict["hexes"]["{}-{}".format(hID.xid, hID.yid)]=hex_dict
    
def load(clicker, filename:str):
    pass

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
        new._hexIDs += other.hexIDs
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
        print("registering {}".format(rid))

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
        region.subtract(Region(Hex(hex_to_screen(hID)), hID))
        self._ridcatalog[rid] = region

        if (region.hexIDs)==0:
            self.delete_region(rid)


class Catalog:
    _dtype = Hex
    def __init__(self, dtype:type):
        Catalog._dtype = dtype
        self._hidcatalog = {} # hex id -> obj
        self._sidcatalog = {} # screen id -> obj
        self._interface = {} # hexid to screen id

    def getSID(self,hID:HexID):
        return self._interface[hID]

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
            self._sidcatalog[sid] = None
            self._interface[hid] = None
        else:
            raise ValueError("Tried removing hexID {} from catalog, but no entry found in interface".format(hid))
    

    def register(self, item:_dtype, screenid:QGraphicsItem, hid:HexID):
        """
        Called when we're registering 
        """
        self._hidcatalog[hid] = item
        self._sidcatalog[screenid] = item
        self._interface[hid] = screenid
            

    def __getitem__(self, key)->_dtype:
        return self._hidcatalog[key]

    def __contains__(self, key)->bool:
        return key in self._hidcatalog