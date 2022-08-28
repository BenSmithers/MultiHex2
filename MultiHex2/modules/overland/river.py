"""
Implements sub-types of the core MultiHex classes 

    + River (Path)
    + River Catalog (Path Catalog)

"""


from MultiHex2.core.core import Path, PathCatalog, GeneralCatalog
from MultiHex2.core.coordinates import HexID, get_IDs_from_step

from copy import deepcopy
from collections import deque

from PyQt5.QtCore import QPointF



class River(Path):
    def __init__(self, *positions):
        super().__init__(*positions)

        self._tributaries = []

    @property
    def width(self):
        """
        Calculates a "width" for the river depending on the number of tributaries it has (And how many tributaries those tributaries have)
        """
        base_width = 3.0
        TRIB_SCALE = 0.5

        if len(self.tributaries)!=0:
            t1_width = self.tributaries[0].width
            t2_width = self.tributaries[1].width

            base_width += t1_width*TRIB_SCALE + t2_width*TRIB_SCALE

        return base_width

    @property
    def vertices(self)->'list[QPointF]':
        return super().vertices
    
    @property 
    def tributaries(self)->'list[River]':
        return self._tributaries

    def get_footprint(self)->'list[HexID]':
        """
        Gets a list of all the hexIDs underneath/beside this river
        """
        all_hids = []

        for i_v in range(len(self._vertices)-1):
            besides = list(get_IDs_from_step(self._vertices[i_v], self._vertices[i_v+1]))
            all_hids += besides
        
        return list(set(all_hids))

    def check_contains(self, other:QPointF)->bool:
        """
        Returns whether or not the QPointF "other" is contained in the vertices of this river 
        """
        if len(self.tributaries)==0:
            return other in self.vertices
        else:
            trib1 = self.tributaries[0].check_contains(other)
            if trib1:
                return trib1
            else:
                trib2 = self.tributaries[1].check_contains(other)
                return trib2

    def merge_into(self, other:'River')->bool:
        """
        Merges this river with another one; requires the end of this river be on the target river 

        `merge_with` should be the prefered way to merge rivers since it maintains the same main body of the river (and its names and stuff)
        """
        
        this_end = self.get_end()
        if this_end in other.vertices:
            intersect_index = other.vertices.index(this_end)

            intermediate = list(other._vertices)

            trib1_verts = intermediate[intersect_index:]
            new_verts = intermediate[:(intersect_index+1)]
            trib1 = River(*trib1_verts)
            trib2 = River(*self.vertices)

            self._vertices = deque(new_verts)
            self._tributaries = [trib1, trib2]

            return True
        else:
            # check tributaries of other River
            these_tribs = other.tributaries
            if len(these_tribs)!=0:
                retval = self.merge_into(these_tribs[0])
                if retval:
                    return retval #merged with a tributary 
                
                retval = self.merge_into(these_tribs[1])
                if retval:
                    return retval
                
            return False

    def merge_with(self, other:'River'):
        """
        Requires river "other" to end on a vertex on this River 
        """
        other_end = other.get_end()

        if other_end in self.vertices:
            intersect_index =self._vertices.index(other_end)

            intermediate = list(self._vertices)


            lower_half = intermediate[intersect_index:]
            upper_half = intermediate[:(intersect_index+1)]

            self._vertices = deque(lower_half)
            trib1 = River(*upper_half)
            trib1._tributaries=deepcopy(self._tributaries)

            trib2 = other
            self._tributaries = [trib1, trib2]

            return True

        else:
            these_tribs = self.tributaries()
            if len(these_tribs)!=0:
                retval = self.tributaries[0].merge_with(other)
                if retval:
                    return retval
                retval = self.tributaries[1].merge_with(other)
                
                return retval
                

class RiverCatalog(PathCatalog):
    """
    Specific case of the path catalog; we need special rules here for associations/de-associations 
    """

    def _de_assoc(self, path_id: int, river:River):
        for i_v in range(len(river)-1):
            _start = river.vertices[i_v]
            _end = river.vertices[i_v+1]
            hid1, hid2 = get_IDs_from_step(_start, _end)
            super()._de_assoc(path_id, hid1)
            super()._de_assoc(path_id, hid2)

        tribs = river.tributaries
        for trib in tribs:
            self._de_assoc(path_id, trib)

    def _assoc(self,path_id: int, river:River):
        """
        Sepcific associator since rivers can have tributaries. These are other rivers that share a singular path ID number
        """
        for i_v in range(len(river)-1):
            _start = river.vertices[i_v]
            _end = river.vertices[i_v+1]
            hid1, hid2 = get_IDs_from_step(_start, _end)
            super()._assoc(path_id, hid1)
            super()._assoc(path_id, hid2)

        tribs = river.tributaries
        for trib in tribs:
            self._assoc(path_id, trib)

    def remove(self, pid):
        """
        We load the road and check all the entries 
        """
        this_path = self.get(pid)
        self._de_assoc(pid, this_path)

        return GeneralCatalog.remove(self, pid)

    def register(self, river: River) -> int:
        """
        Similar to the default Path register thing, but now we look at the HexIDs on the side of these steps 
        """
        pid = GeneralCatalog.register(self, river)

        if len(river.vertices)==1:
            return pid

        self._assoc(pid, river)
        
        return pid

    def add_to(self, pid, what, end:bool):
        """
        Same changes as present in the "register" function
        """
        this_path = self.get(pid)
        start_vertex = this_path.get_end() if end else this_path.get_start()
        if end:
            this_path.add_to_end(what)
        else:
            this_path.add_to_start(what)
        
        hid1, hid2 = get_IDs_from_step(start_vertex, what)
        self._assoc(pid, hid1, hid2)

    def get(self, id: int) -> River:
        return super().get(id)

    def update_sid(self, id: int, *sid):
        self._interface[id] = sid