from PyQt5.QtCore import QPointF
from math import sqrt

RTHREE = sqrt(3)
DRAWSIZE = 20.

    
class HexID:
    """
        MultiHex2 uses a cubic coordinate system for the hexes. 
    """
    def __init__(self, xid:int, yid:int):
        """
        In cubic coordinates, the sum of all indices is zero. So we only need two IDs to get the third
        """
        self._xid = xid
        self._yid = yid
        self._zid = 0 - xid - yid
    def __str__(self):
        return "({}, {}, {})".format(self._xid, self._yid, self._zid)
    @property
    def xid(self)->int:
        return self._xid
    @property
    def yid(self)->int:
        return self._yid
    @property
    def zid(self)->int:
        return self._zid
    def __hash__(self):
        return hash((self._xid, self._yid))
    def __eq__(self, other):
        if other.__class__!=HexID:
            return False
        else:
            return (self.xid == other.xid) and (self.yid==other.yid)
    def __add__(self, other:'HexID'):
        return HexID(self.xid + other.xid, self.yid + other.yid)
    
    @property
    def neighbors(self):
        nb = [
            HexID(self.xid+1,self.yid), HexID(self.xid+1, self.yid-1), HexID(self.xid, self.yid+1),
            HexID(self.xid-1, self.yid),HexID(self.xid-1, self.yid+1), HexID(self.xid, self.yid-1)
        ]
        return nb

    def in_range(self, dist:int):
        results = []
        for i in range(-dist, dist+1):
            for j in range(max(-dist, -i-dist), min(dist, -i+dist)+1):
                results.append(self + HexID(i,j))
        return results
    def __repr__(self) -> str:
        return "{}_{}_{}".format(self._xid, self._yid, self._zid)

    def __sub__(self, other:'HexID')->int:
        """
            returns the distance between this and another HexID
        """
        inter_id = HexID(self.xid - other.xid, self.yid - other.yid)

        return int((abs(inter_id.xid) + abs(inter_id.yid) + abs(inter_id.zid))/2)

        # -30 degrees, increment by 60 with each

M = (3.0 / 2.0, 0.0, RTHREE/2.0, RTHREE, # F0-F3
               2.0 / 3.0, 0.0, -1.0 / 3.0, RTHREE / 3.0) #b0-b3

def screen_to_hex(point:QPointF)->HexID:
    """
        Returns the HexID for the spot under the cursor in pixel-space 
    """
    fq = (M[4]*point.x())/DRAWSIZE
    fr = (M[6]*point.x() + M[7]*point.y())/DRAWSIZE

    q = round(fq)
    r = round(fr)
    s = -q-r

    q_diff = abs(q-fq)
    r_diff = abs(r-fr)
    s_diff = abs(s+fq+fr)
    if q_diff > r_diff and q_diff > s_diff:
        q = -r-s
    elif r_diff > s_diff:
        r = -q-s
    else:
        pass
    return HexID(q, r)

def hex_to_screen(id:HexID)->QPointF:
    """
        Returns the pixel location of the center of the gien HexID 
    """
    x_loc = DRAWSIZE*(M[0]*id.xid)
    y_loc = DRAWSIZE*(M[2]*id.xid + M[3]*id.yid)
    return QPointF(x_loc, y_loc)

def get_adjacent_vertices(_point:QPointF, flip=False)->'list[QPointF]':
    """
    Returns the vertices adjacent to a given vertex. **this assumes that the point given lies on a vertex of a Hex**

    there are one of two kinds of vertices:
        1  opens right
        2  opens left

    I can't draw these, it breaks the linter 

    We don't know which this is. So, we look to the left of the vertex (step of DRAWSIZE), and up/down from it some small step. 
    We access the IDs for each of those perturbed points; if they're the same it's type 2, otherwise type 1

        @flip - if this is true, this intentionally inverts the vertex type and returns points inside the three hexes neighboring this given vertex
    """
    point = _point
    x_step = -0.5*DRAWSIZE
    y_step = 0.1*DRAWSIZE
    type_1 = screen_to_hex(point + QPointF(x_step, y_step)) != screen_to_hex(point + QPointF(x_step, -y_step))



    if type_1!=flip:
        return point+QPointF(-DRAWSIZE, 0.0),point+QPointF(0.5*DRAWSIZE, 0.5*RTHREE*DRAWSIZE), point+QPointF(0.5*DRAWSIZE, -0.5*RTHREE*DRAWSIZE) 
    else:
        return point+QPointF(DRAWSIZE, 0.0),point+QPointF(-0.5*DRAWSIZE, 0.5*RTHREE*DRAWSIZE), point+QPointF(-0.5*DRAWSIZE, -0.5*RTHREE*DRAWSIZE) 

def get_adjacent_hexIDs(_point:QPointF)->'list[HexID]':
    """
    Here we return the IDs of the Hexes around the given point. This assumes the given point is on a hex! 
    """
    these_points = get_adjacent_vertices(_point, True)

    return [screen_to_hex(point) for point in these_points]



def get_IDs_from_step(_start:QPointF, _end:QPointF)->'tuple[HexID]':
    """
    These QPointF's must be DRAWSIZE away from each other and are interpreted as neiboring vertices of an edge between hexes. 

    This returns the two HexIDs corresponding to the hexes that share that edge 
    """
    start =_start
    end = _end

    diff = end - start
    # sanity!
    diff_mag = sqrt(diff.x()**2 + diff.y()**2)
    if not abs(diff_mag-DRAWSIZE)<1e-6:
        raise ValueError("Points {} and {} are {} apart; an incorrect distance".format(start, end, diff_mag))

    # want vector normal to the difference vector 
    # define that normal vector be 0.5*drawsize long

    norm_y_sq = (0.25*(diff.x()*DRAWSIZE)**2)/(diff.y()**2 + diff.x()**2)
    norm_x = sqrt(0.25*DRAWSIZE**2 - norm_y_sq)
    norm_y = sqrt(norm_y_sq)

    # from the start point, step half way along the difference vector, then go off at the normal 
    p1 = start + QPointF(diff.x()*0.5+norm_x, diff.y()*0.5+norm_y)
    p2 = start + QPointF(diff.x()*0.5-norm_x, diff.y()*0.5-norm_y)

    return screen_to_hex(p1), screen_to_hex(p2)

