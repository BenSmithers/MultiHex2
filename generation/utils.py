"""
Define some utilities used by the generators

 - perlin noise generator
"""
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QColor


from math import exp
import numpy as np
import numpy.random as rnd

from MultiHex2.core.core import Hex

class Climatizer:
    def __init__(self, tileset:dict):
        self.tileset = tileset
        self.params = Climatizer.get_params(tileset)
        assert(len(self.params)>=1)

    def _get_climate(self, params:list):
        if len(params)!=len(self.params):
            raise ValueError("Didn't get the right length of params: {}, not {}".format(len(params), len(self.params)))
        
        testing = np.array(params)
        super = ""
        subt = ""
        distance = 10000. # arbitrarily large distance 

        # loop over all the tiles we have
        for super_type in self.tileset:
            for sub_type in self.tileset[super_type]:
                which = self.tileset[super_type][sub_type]["params"]
                temp = np.array([which[param] for param in self.params])

                # get the spatial distance between the tested set of parameters, and all the available tiles  
                dist_between = np.sqrt(np.sum((temp - testing)**2))
                if dist_between<distance:
                    super = super_type
                    subt = sub_type
                    distance = dist_between

        return super, subt

    def apply_climate_to_hex(self, target:Hex):
        """
        Get the climate for this hex, apply it
        """
        these_params = [target.params[param] for param in self.params]
        
        sup, sub = self._get_climate(these_params)

        target.set_params(self.tileset[sup][sub])
        fill = self.tileset[sup][sub]["color"]
        target.set_fill(QColor(fill[0], fill[1], fill[2]))
        target.geography=sub

    @classmethod
    def get_params(cls, tset:dict)->list:
        # get the parameters
        parameters = []
        ignoring = ["color","is_ray","flattype",]
        for super_type in tset:
            for sub_type in tset[super_type]:
                for param in tset[super_type][sub_type]["params"]:
                    if param not in ignoring:
                        parameters.append( param )
                # we really only need to do this for the first entry. So let's break! 
                break
            break
        return( parameters )

def get_loc(x:float, domain:list,closest=False):
    """
    Returns the indices of the entries in domain that border 'x' 
    Raises exception if x is outside the range of domain 
    Assumes 'domain' is sorted!! And this _only_ works if the domain is length 2 or above 
    This is made for finding bin numbers on a list of bin edges 
    """

    if len(domain)<=1:
        raise ValueError("get_loc function only works on domains of length>1. This is length {}".format(len(domain)))


    # I think this is a binary search
    min_abs = 0
    max_abs = len(domain)-1

    lower_bin = int(abs(max_abs-min_abs)/2)
    upper_bin = lower_bin+1

    while not (domain[lower_bin]<=x and domain[upper_bin]>=x):
        if abs(max_abs-min_abs)<=1:
            print("{} in {}".format(x, domain))
            raise Exception("Uh Oh")

        if x<domain[lower_bin]:
            max_abs = lower_bin
        if x>domain[upper_bin]:
            min_abs = upper_bin

        # now choose a new middle point for the upper and lower things
        lower_bin = min_abs + int(abs(max_abs-min_abs)/2)
        upper_bin = lower_bin + 1
    
    assert(x>=domain[lower_bin] and x<=domain[upper_bin])
    if closest:
        return( lower_bin if abs(domain[lower_bin]-x)<abs(domain[upper_bin]-x) else upper_bin )
    else:
        return(lower_bin, upper_bin)

def bilinear_interp(p0, p1, p2, q11, q12, q21, q22):
    """
    Performs a bilinear interpolation on a 2D surface
    Four values are provided (the qs) relating to the values at the vertices of a square in the (x,y) domain
        p0  - point at which we want a value (len-2 tuple)
        p1  - coordinates bottom-left corner (1,1) of the square in the (x,y) domain (len-2 tuple)
        p2  - upper-right corner (2,2) of the square in the (X,y) domain (len-2 tuple)
        qs  - values at the vertices of the square (See diagram), any value supporting +/-/*
                    right now: floats, ints, np.ndarrays 
        (1,2)----(2,2)
          |        |
          |        |
        (1,1)----(2,1)
    """

    
    # check this out for the math
    # https://en.wikipedia.org/wiki/Bilinear_interpolation

    x0 = p0[0]
    x1 = p1[0]
    x2 = p2[0]
    y0 = p0[1]
    y1 = p1[1]
    y2 = p2[1]

    if not (x0>=x1 and x0<=x2):
        raise ValueError("You're doing it wrong. x0 should be between {} and {}, got {}".format(x1,x2,x0))
    if not (y0>=y1 and y0<=y2):
        raise ValueError("You're doing it wrong. y0 should be between {} and {}, got {}".format(y1,y2,y0))

    # this is some matrix multiplication. See the above link for details
    # it's not magic, it's math. Mathemagic 
    mat_mult_1 = [q11*(y2-y0) + q12*(y0-y1) , q21*(y2-y0) + q22*(y0-y1)]
    mat_mult_final = (x2-x0)*mat_mult_1[0] + (x0-x1)*mat_mult_1[1]

    return( mat_mult_final/((x2-x1)*(y2-y1)) )

def perlin(granularity, seed=0)->np.ndarray:
    """
    returns a mesh of perlin noise given a seed and granularity 
    
    returns numpy array with values ranging between -0.5 and 0.5
    """
    lin = np.linspace(0,5,granularity,endpoint=False)
    x,y = np.meshgrid(lin, lin)

    # permutation table
    np.random.seed(seed)
    p = np.arange(256,dtype=int)
    np.random.shuffle(p)
    p = np.stack([p,p]).flatten()
    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coordinates
    xf = x - xi
    yf = y - yi
    # _fade factors
    u = _fade(xf)
    v = _fade(yf)
    # noise components
    n00 = _gradient(p[p[xi]+yi],xf,yf)
    n01 = _gradient(p[p[xi]+yi+1],xf,yf-1)
    n11 = _gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
    n10 = _gradient(p[p[xi+1]+yi],xf-1,yf)
    # combine noises
    x1 = _lerp(n00,n10,u)
    x2 = _lerp(n01,n11,u) # FIX1: I was using n10 instead of n01
    return _lerp(x1,x2,v) # FIX2: I also had to reverse x1 and x2 her

def _lerp(a,b,x):
    "linear interpolation"
    return a + x * (b-a)

def _fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def _gradient(h,x,y):
    "grad converts h to the right _gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h%4]
    return g[:,:,0] * x + g[:,:,1] * y

def gauss(mean, dev):
    return (rnd.randn()*dev + mean)

def point_is_in(point:QPointF, dimensions):
    """
    Returns whether or not a Point is within the bounds of a map of given dimensions.

    @param Point    - a Point object
    @param dimensions - list-like 
    """

    return( point.x() < dimensions[0] and point.x() > 0 and point.y() < dimensions[1] and point.y()>0)



def angle_difference( theta_1, theta_2 ):
    """
    Returns the absolute difference between two angles

    @param theta_1 - first angle [degrees]
    @param theta_2 - second angle [degrees]
    """
    if not isinstance( theta_1, float):
        raise TypeError("theta_1 not {}, it's {}".format(float, type(theta_1)))
    if not isinstance( theta_2, float):
        raise TypeError("theta_2 not {}, it's {}".format(float, type(theta_2)))

    if not (theta_1 >= 0 and theta_1<=360):
        raise Exception("bad angle {}".format(theta_1))
    if not (theta_2 >= 0 and theta_2<=360):
        raise Exception("bad angle {}".format(theta_2))
    
    return(min([(360.) - abs(theta_1-theta_2), abs(theta_1-theta_2)]) )

def get_distribution( direction, variance=20. ):
    """
    Creates a normalized, discrete, gaussian distribution centered at a given angle and with a given variance. Distribution applies to the six angles correlated with the directions to a Hexes' neighbors' centers. 

    @param direction - mean of distribution
    @param variance -  variance of distribution
    """
    normalization = 0
#    variance = 20.
    angles = [150., 90., 30., 330., 270., 210.]

    # We do this to calculate the overall normalization
    for angle in angles:
        normalization += exp( -1.*(angle_difference(angle, direction)**2)/(2*variance**2))

    # Then prepare a function returning normalized probabilities 
    def distribution(angle): 
        return( (1./normalization)*exp(-1*(angle_difference(angle, direction)**2)/(2*variance**2)))

    return( distribution )