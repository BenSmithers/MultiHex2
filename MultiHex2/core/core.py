from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF, QColor
from math import sqrt,sin,cos, pi

from MultiHex2.core.map_entities import Government
from MultiHex2.core.map_entities import Entity

from .coordinates import HexID, hex_to_screen, DRAWSIZE, screen_to_hex

import numpy as np
from numpy.random import randint
from collections import deque


RTHREE = sqrt(3)

def get_arrowhead(center:QPointF, _angle)->'list[QPointF]':
    """
    Takes a set of points that can trace an arrow atthe origin
    rotate it to point at the given angle, and shift it to the center point 

    the center point is at the middle-bottom of the arrow
    """
    ARROW = np.array([
        (0,0),
        (1,0),
        (1,3),
        (1.25, 3),
        (0.5, 5),
        (-1.25, 3),
        (-1, 3),
        (-1, 0)
    ])
    angle = _angle - pi/2
    rot = np.array([[cos(angle), sin(angle)],[-sin(angle), cos(angle)]])
    
    new_arrow = np.matmul(ARROW, rot) + np.array(center.x(), center.y())
    return [QPointF(entry[0], entry[1]) for entry in new_arrow]

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
        self._flat = False
        self._color_scale_param = "altitude_base"
        self.wind = np.zeros(2)

    def __getitem__(self, key):
        if key in self._params:
            return self._params[key]
        else:
            return super().__getitem__(key)

    def __setitem__(self,key, value):
        self._params[key] = value

    @property 
    def center(self):
        return QPointF(self.x, self.y)

    @property
    def params(self):
        return self._params
    @property
    def fill(self)->QColor:
        return self._fill
        alt_scale = 0.2
        if self._flat:
            return self._fill
        else:
            return QColor(min( 255, max( 0, self._fill.red()*( 1.0 + alt_scale*self.params[self._color_scale_param]-alt_scale*0.5))),
                        min( 255, max( 0, self._fill.green()*( 1.0 + alt_scale*self.params[self._color_scale_param]-alt_scale*0.5))),
                        min( 255, max( 0, self._fill.blue()*( 1.0 + alt_scale*self.params[self._color_scale_param]-alt_scale*0.5))))


    def set_fill(self, fill:QColor):
        self._fill = fill
    def set_params(self, params:dict,*skipkeys):
        for key in params:
            if key in skipkeys:
                continue
            else:
                self._params[key] = params[key]
    def set_param(self, param:str, value:float):
        self._params[param] = value

    def pack(self)->dict:
        """
        Takes the hex object and save the essentials such that this can be reconstructed later. 
        """
        vals = {
            "red":self._fill.red(),
            "green":self._fill.green(),
            "blue":self._fill.blue(),
            "params":self.params,
            "is_land":self.is_land,
            "flat":self._flat,
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
        new_hx = cls(QPointF(obj["x"], obj["Y"]))
        new_hx._fill = QColor(obj["red"], obj["green"], obj["blue"])
        new_hx._params = obj["params"]
        new_hx.geography=obj["geo"]
        new_hx.wind = np.array(obj["wind"])
        new_hx.is_land=obj["is_land"]
        new_hx._flat = obj["flat"]
        return new_hx

def get_nearest_vertex(point:QPointF):
    """
    Returns the verex nearest the given QPointF

    Neartest vertex should be on the hex that contains this point
    """
    hid_contained = screen_to_hex(point)
    center = hex_to_screen(hid_contained)
    trial_pts = Hex(center)

    min_dist = 10*DRAWSIZE
    min_index = -1
    if len(trial_pts)!=6:
        raise ValueError("WTF? {}".format(trial_pts))
    for i_vertex in range(len(trial_pts)):
        disp = point - trial_pts[i_vertex]
        dist = sqrt(disp.x()**2 + disp.y()**2)
        if min_index==-1:
            min_index = i_vertex
            min_dist = dist
        elif dist<min_dist:
            min_dist = dist
            min_index=i_vertex
    return trial_pts[min_index] 


class Region(QPolygonF):
    """
    Regions are just two polygons, merged together
    """
    def __init__(self, origin:QPolygonF, *hexIDs:HexID):
        super().__init__(origin)
        self._name = "New Region"
        self._hexIDs = list(hexIDs)
        self._fill = QColor(randint(1,255),randint(1,255),randint(1,255))

        self._geography = ""
    
    @property
    def geography(self):
        return self._geography

    def set_geography(self, geo:str):
        self._geography = geo

    def average_location(self):
        mean_x = 0.0
        mean_y = 0.0
        n = len(self._hexIDs)
        for hid in self.hexIDs:
            pt = hex_to_screen(hid)
            mean_x += pt.x()/n
            mean_y += pt.y()/n
        return QPointF(mean_x, mean_y)

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
        new_reg = cls(QPolygonF(verts), *hIDs)
        new_reg._name = packed["name"]
        new_reg._fill=QColor(packed["red"], packed["green"], packed["blue"])
        return new_reg

    def set_name(self, name:str):
        self._name = name
    def set_fill(self,fill:QColor):
        self._fill = fill

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

class County(Region, Government):
    def __init__(self, origin: QPolygonF, *hexIDs: HexID):
        super().__init__(origin, *hexIDs)

class Path:
    """
    A series of points that form a path of some kind. Can be made of either QPointF's or HexIDs
    """
    def __init__(self, *positions):
        self._viable_dtypes = (QPointF, HexID)
        self._dtype = int
        self._step = None #QPointF or integer
        self.name = "New Path"

        for entry in positions:
            if self._dtype == int:
                self._dtype = type(entry)
                if not type(entry) in self._viable_dtypes:
                    raise TypeError("Tried making path with unsupported data type {}".format(type(entry)))
                
            else:
                if type(entry)!=self._dtype:
                    raise TypeError("Inconsistent typing with starting positions")

        self._vertices = deque(positions)

        # verify the step size is acurate 
        
        for i in range(len(self._vertices)-1):
            this_step =  self.get_diff( self._vertices[i+1], self._vertices[i] )
            if self._step is None:
                self._step = this_step
            else:
                if abs(this_step -self._step)>1e-6:
                    raise ValueError("Inconsistent step sizes! {} vs {}".format(self._step, this_step)) 
                    
        self._quality = 1.0
    
    @property
    def quality(self):
        return self._quality
    def get_diff(self, one, other):
        if self._dtype==HexID:
            return one-other
        else:
            return sqrt((one.x()-other.x())**2  + (one.y()-other.y())**2)

    def pack(self)->dict:
        me = {}
        me["dtype"]="HexID" if self._dtype==HexID else "QPointF"
        me["name"]=self.name
        this_verts = []
        for entry in self.vertices:
            
            if self._dtype==HexID:
                what = [entry.xid, entry.yid]
            else:
                what = [entry.x(), entry.y()]
            this_verts.append(what)
        me["verts"] = this_verts
        return me

    @classmethod
    def unpack(cls, this_dict:dict)->'Path':
        datatype = HexID if  this_dict["dtype"]=="HexID" else QPointF
        all_verts = []
        for entry in this_dict["verts"]:
            all_verts.append(datatype(entry[0], entry[1]))

        new_path = cls(*all_verts)
        new_path.name = this_dict["name"]
        return new_path

    def add_to_end(self, other):
        if not isinstance(other, self._dtype):
            raise ValueError("Expected object of dtype {}, got {}".format(self._dtype, type(other)))

        this_step = self.get_diff( other , self._vertices[-1])
        if self._step is None:
            self._step = this_step
        else:
            if abs(this_step - self._step)>1e-6:
                raise ValueError("Inconsistent step sizes! {} vs {}".format(self._step, this_step)) 
            
        self._vertices.append(other)

    def add_to_start(self, other):
        if not isinstance(other, self._dtype):
            raise ValueError("Expected object of dtype {}, got {}".format(self._dtype, type(other)))

        # add
        this_step = self.get_diff( other , self._vertices[0])
        if abs(this_step- self._step)>1e-6:
            raise ValueError("Inconsistent step sizes! {} vs {}".format(self._step, this_step)) 
        
        self._vertices.appendleft(other)


    def __iter__(self):
        return self.vertices.__iter__()

    def __contains__(self, thing):
        """
        Implements "thing in Path" method
        """
        if not isinstance(thing, self._dtype):
            return False

        return thing in self._vertices

    def __len__(self):
        return len(self._vertices)

    @property
    def vertices(self):
        return self._vertices

    def pop_from_end(self):
        """
        Removes the end point from the path and returns it
        """
        return self._vertices.pop()

    def pop_from_start(self):
        """
        Removes the start point from the path and returns it 
        """
        return self._vertices.popleft()


    def get_end(self):
        return self._vertices[-1]

    def get_start(self):
        return self._vertices[0]


class GeneralCatalog:
    def __init__(self):
        self._idCatalog = {} # objectID -> object
        self._interface = {} # objectID -> screenID 

    def __contains__(self, id:int):
        return id in self._idCatalog

    def get_next_id(self)->int:
        id = 0
        while id in self._idCatalog:
            id+=1
        return id

    def register(self, obj)->int:
        id = self.get_next_id()
        self._idCatalog[id] = obj

        return id

    def get(self, id:int):
        if id in self._idCatalog:
            return self._idCatalog[id]
        else:
            return
        
    def get_sid(self, id:int):
        if id in self._interface:
            return self._interface[id]
        else:
            return

    def update_obj(self, id:int, obj, suppress_warning=False):
        if (id not in self._idCatalog) and (not suppress_warning):
            raise KeyError("Object not here!")
        
        self._idCatalog[id] = obj

    def update_sid(self, id:int, sid):
        if id not in self._idCatalog:
            print("sid {} {} catalog".format(id, "in" if sid in self._interface else "not in"))
            raise KeyError("Obj {} not registered".format(id))
        
        self._interface[id] = sid
        
    def remove(self, hid):
        """
        Remove from catalog
        """
        if hid in self._idCatalog:
            del self._idCatalog[hid]
        else:
            raise ValueError("Error, QGraphicsItem {} not in catalog.".format(hid))

        if hid in self._interface:
            del self._interface[hid]
        else:
            raise ValueError("Tried removing hexID {} from catalog, but no entry found in interface".format(hid))

    def __getitem__(self, key):
        return self._idCatalog[key]

    def __iter__(self):
        return self._idCatalog.__iter__()

class PathCatalog(GeneralCatalog):
    """
    Object for keeping track of Paths, their screen IDs, and the hexes bordering these paths 
    """

    def __init__(self):
        GeneralCatalog.__init__(self)
        self._hexint = {} # hexID -> pids 

    def get(self, id: int)->Path:
        return super().get(id)

    def _assoc(self, path_id:int, what):
        """
        Associates 'whatever' with that path id. 
        """
        if what in self._hexint:
            self._hexint[what] += [path_id]
        else:
            self._hexint[what] = [path_id]
    def _de_assoc(self, path_id:int, what):
        """
            Removes the above association
        """

        if what in self._hexint:
            self._hexint[what].remove(path_id)
        else:
            raise ValueError("Asked to de-associate {} with the path_id {}, but they were never associated".format(what, path_id))

    def remove(self, pid):
        """
        We load the road and check all the entries 
        """
        this_path = self.get(pid)
        for vert in this_path.vertices:
            self._de_assoc(pid,vert)

        return super().remove(pid)

    def add_to(self, pid:int, what, end:bool):
        this_path = self.get(pid)
        if end:
            this_path.add_to_end(what)
        else:
            this_path.add_to_start(what)
        self._assoc(pid, what)


    def pop_from(self, pid:int, end:bool)->HexID: #probably hexID, could be QPointF
        this_path = self.get(pid)
        if end:
            popped = this_path.pop_from_end()
        else:
            popped = this_path.pop_from_start()
        self._de_assoc(pid, popped)
        return popped

    def paths_here(self, hID:HexID)->'list[int]':
        if hID in self._hexint:
            return self._hexint[hID]
        else:
            return []

    def register(self, path:Path)->int:
        pid = GeneralCatalog.register(self, path)

        for vertex in path:
            self._assoc(pid, vertex)
        return pid


class RegionCatalog(GeneralCatalog):
    """
    Object for keeping track of Regions and the hexes that encompass them 
    """
    def __init__(self):
        GeneralCatalog.__init__(self)
        self._hidcatalog = {} # hexID -> regionID

    def get_sid(self, id):
        """
        Gets the scene id for the region at the specified HexID/Region ID
        """
        if isinstance(id, HexID):
            if id not in self._hidcatalog:
                return
            elif self._hidcatalog[id] not in self._interface:
                return
            else:
                return self._interface[self._hidcatalog[id]]
        elif isinstance(id, int): #region id
            return GeneralCatalog.get_sid(self, id)
        else:
            raise TypeError("Not sure what to do with {}".format(type(id)))
    def get(self, rid)->Region:
        """
        Returns region for a region ID
        """
        return GeneralCatalog.get(self,rid)

    def get_rid(self, id:HexID)->int:
        """
        Returns Region ID for a hex id, or returns None if the hex isn't in a region
        """
        if id in self._hidcatalog:
            return self._hidcatalog[id]
        else:
            return

    def update_sid(self, rid:int, *sid):
        self._interface[rid] = sid

    def delete_region(self, rID:int):
        for hexID in self._idCatalog[rID].hexIDs:
            del self._hidcatalog[hexID]

        del self._idCatalog[rID]
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

        region = self._idCatalog[rid]
        region = region.subtract(Region(Hex(hex_to_screen(hID)), hID))
        self._idCatalog[rid] = region

        if (region.hexIDs)==0:
            self.delete_region(rid)

    def __iter__(self):
        return self._idCatalog.__iter__()

    def __getitem__(self, key)->Region:
        return self._idCatalog[key]

    def __len__(self):
        return len(self._idCatalog.keys())

class EntityCatalog:
    """
    Class for keeping track of Entities, their IDs, their QGraphicsScene hashes, and where they are on the map 

    TODO: incorporate GeneralCatalog stuff with this 
    """
    def __init__(self):
        self._eidCatalog = {} # eID->Entity 
        self._hIDtoEnt = {} #hexID -> eIDs 
        self._eIDtoHex = {} #eID -> hexID
        self._hIDtoScreen = {} #eID -> ScreenID

    def __iter__(self):
        return self._eidCatalog.__iter__()

    def get(self, eID)->Entity:
        if eID in self._eidCatalog:
            return self._eidCatalog[eID]
        
    def __contains__(self, key):
        return key in self._eidCatalog
    def next_free_eid(self)->int:
        eID = 0
        while eID in self._eidCatalog:
            eID+=1
        return eID

    def register(self, hID:HexID, entity:Entity, *screenID):
        eID = self.next_free_eid()
        self._eidCatalog[eID] = entity
        self._eIDtoHex[eID] = hID

        if hID in self._hIDtoEnt:
            self._hIDtoEnt[hID].append(eID)
        else:
            self._hIDtoEnt[hID] = [eID]
        
        self._hIDtoScreen[hID] = screenID

        return eID

    def remove(self, eID:int):
        del self._eidCatalog[eID]

        hID = self._eIDtoHex[eID]
        self._hIDtoEnt[hID].remove(eID)
        if len(self._hIDtoEnt[hID])==0:
            del self._hIDtoEnt[hID]

        del self._eIDtoHex[eID]
        del self._hIDtoScreen[hID]

    def update_sid(self, hID:HexID, *sID):
        self._hIDtoScreen[hID] = sID

    def update_entity(self, eID:int, entity:Entity):
        self._eidCatalog[eID] = entity

    def access_entities_at(self, hID:HexID)->list:
        if hID in self._hIDtoEnt:
            return self._hIDtoEnt[hID]
        else:
            return []
    def access_entity(self, eID:int)->Entity:
        if eID in self._eidCatalog:
            return self._eidCatalog[eID]
    def getSID(self, hexID:int):
        if hexID in self._hIDtoScreen:
            return self._hIDtoScreen[hexID]
    def gethID(self, eID:int)->HexID:
        if eID in self._eIDtoHex:
            return self._eIDtoHex[eID]
    def change_hID(self, eID:int, new_hid:HexID):
        old_hid = self.gethID(eID)


        self._hIDtoEnt[old_hid].remove(eID)

        if len(self._hIDtoEnt[old_hid])==0:
            del self._hIDtoEnt[old_hid]

        if new_hid in self._hIDtoEnt:
            self._hIDtoEnt[new_hid].append(eID)
        else:
            self._hIDtoEnt[new_hid] = [eID]
        self._eIDtoHex[eID]= new_hid



class HexCatalog(GeneralCatalog):
    """
    class for keeping track of Hexes, their IDs, and their QGraphicsScene hashes
    """
    _dtype = Hex
    def __init__(self, dtype:type):
        GeneralCatalog.__init__(self)
        HexCatalog._dtype = dtype

    def get_next_id(self) -> int:
        raise NotImplementedError("You shouldn't be using this function with a HexCatalog; the IDs are not enumerated!")

    def get_all_hids(self):
        return self._idCatalog.keys()

    def get(self, id: int)->Hex:
        return super().get(id)

    def remove(self, hid:HexID):
        """
        Remove from catalog
        """
        if hid in self._idCatalog:
            del self._idCatalog[hid]
        else:
            raise ValueError("Error, QGraphicsItem {} not in catalog.".format(hid))

        if hid in self._interface:
            del self._interface[hid]
        else:
            raise ValueError("Tried removing hexID {} from catalog, but no entry found in interface".format(hid))
    

    def register(self, item:_dtype, hid:HexID):
        """
        Called when we're registering 
        """
        self._idCatalog[hid] = item
        self._interface[hid] = None
            