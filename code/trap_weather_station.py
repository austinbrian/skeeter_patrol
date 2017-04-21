#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 16:24:50 2017

@author: michaelsanders
"""

"""
Mapping of each trap to its nearest weather station--compares distance in km between a trap and each airport weather station, and returns the station number ('Station' column) of the nearest weather station.

Weather station info from Kaggle:

Station 1: CHICAGO O'HARE INTERNATIONAL AIRPORT Lat: 41.995 Lon: -87.933 Elev: 662 ft. above sea level
Station 2: CHICAGO MIDWAY INTL ARPT Lat: 41.786 Lon: -87.752 Elev: 612 ft. above sea level

"""

station_coords = {
        1: (41.995,-87.933),
           2: (41.786,-87.752)}

train['Coordinates'] = train[['Latitude', 'Longitude']].apply(tuple, axis=1)

def assign_station(i):
    if distance(station_coords[1], i) < distance(station_coords[2], i):
        return 1
    else:
        return 2

train['Weather_Station'] = train.Coordinates.apply(assign_station)

## Testing area

# index 2 says it should be O'Hare; Index 5 says it should be Midway.  Manually calculating distances of each 
# of those traps to those airports to see if the assignment was correct.
#trap2_ohare = distance(train.loc[2,'Coordinates'], station_coords[1])
#trap2_midway = distance(train.loc[2,'Coordinates'], station_coords[2])
#trap5_ohare = distance(train.loc[5,'Coordinates'], station_coords[1])
#trap5_midway = distance(train.loc[5,'Coordinates'], station_coords[2])

#trap2_ohare
#trap2_midway
#trap5_midway
#trap5_ohare

# It worked.