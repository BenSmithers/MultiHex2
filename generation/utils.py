"""
Define some utilities used by the generators

 - perlin noise generator
"""
from math import exp
from PyQt5.QtCore import QPointF
import numpy.random as rnd

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