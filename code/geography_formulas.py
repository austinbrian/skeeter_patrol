#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 16:51:20 2017

@author: michaelsanders
"""

import math
import numpy as np

''' 
Calculate distance in KM between two sets of coordinates (lat/lon tuples).  Uses Haversine formula.  Credit to https://gist.github.com/rochacbruno/2883505 and http://www.movable-type.co.uk/scripts/latlong.html

This formula works as-is.  I tested it using Google Maps distance calculator as a validator.
'''

def distance(loc1, loc2):
    lat1, lon1 = loc1
    lat2, lon2 = loc2
    radius = 6371 # radius of Earth in KM

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

# Testing formula with two traps from the train data
#point1 = (train_set.loc[2, "Latitude"], train_set.loc[2, "Longitude"])
#point2 = (train_set.loc[4, "Latitude"], train_set.loc[4, "Longitude"])

#dist = distance(point1, point2)
# Confirmed on Google maps



'''
Formula for calculating compass bearing between two lat/lon tuples.  Credit:  https://gist.github.com/jeromer/2005586
Corrected output error in which returned bearing (in degrees) needed to be subtracted from 360 in order to be correct.  
Validated this change on https://www.sunearthtools.com/tools/distance.php and with manual orienteering using Google 
maps in place of a physical map.

Other than that change at the end of the formula, the code was taken from the gist page linked above.
'''


def compass_bearing(loc1, loc2):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `loc1: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `loc2: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(loc1) != tuple) or (type(loc2) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(loc1[0])
    lat2 = math.radians(loc2[0])

    diffLong = math.radians(loc1[1] - loc2[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = 360 - ((initial_bearing + 360) % 360) ## Mike: this originally returned an incorrect bearing
                         ## corrected by subtracting result from 360

    return compass_bearing



## Testing with same example from distance calc:
#bearing = compass_bearing(point1, point2)
#bearing
    
    
    
    
    