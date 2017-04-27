#!bin/bash/python
# Libraries
import pandas as pd
import numpy as np
import math

# read in data
test = pd.read_csv('../data/input/test.csv')
weather = pd.read_csv('../data/input/weather.csv')

# column transformations
weather.Date = pd.DatetimeIndex(weather.Date)
test.Date = pd.to_datetime(test.Date)
weather.PrecipTotal = weather.PrecipTotal.str.strip() # to remove the leading spaces
weather = weather.replace('T', 0.005)
weather = weather.replace('M', np.nan)

weather_excluded = ['Depth', 'Water1', 'SnowFall', 'Depart', 'Heat', 'Cool', 'Sunrise', 'Sunset']
weather_keep = [column for column in weather.columns if column not in weather_excluded]
weather = weather[weather_keep]

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

'''
Calculate distance in KM between two sets of coordinates (lat/lon tuples).  Uses Haversine formula.  Credit to https://gist.github.com/rochacbruno/2883505 and http://www.movable-type.co.uk/scripts/latlong.html

This formula works as-is.  I tested it using Google Maps distance calculator as a validator.
'''

def distance(loc1, loc2):
#     print (loc1, loc2)
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

"""
Mapping of each trap to its nearest weather station--compares distance in km between a trap and each airport weather station, and returns the station number ('Station' column) of the nearest weather station.

Weather station info from Kaggle:

Station 1: CHICAGO O'HARE INTERNATIONAL AIRPORT Lat: 41.995 Lon: -87.933 Elev: 662 ft. above sea level
Station 2: CHICAGO MIDWAY INTL ARPT Lat: 41.786 Lon: -87.752 Elev: 612 ft. above sea level

"""

station_coords = {
        1: (41.995,-87.933),
           2: (41.786,-87.752)}

test['Coordinates'] = test[['Latitude', 'Longitude']].apply(tuple, axis=1)

def assign_station(i):
    if distance(station_coords[1], i) < distance(station_coords[2], i):
        return 1
    else:
        return 2

test['Weather_Station'] = test.Coordinates.apply(assign_station)

# rename the extra trap
test.loc[test['Coordinates'] == (41.992478000000006, -87.862994999999998), 'Trap'] = 'T009Alt'
test.loc[test['Coordinates'] == (41.763733000000002, -87.742301999999995) , 'Trap'] = 'T035Alt'


# setting up column to build out weather types
weather_types = {'\+FC': 'TORNADO/WATERSPOUT','FC': 'FUNNEL CLOUD','TS': 'THUNDERSTORM','GR': 'HAIL','RA': 'RAIN',
'DZ': 'DRIZZLE','SN': 'SNOW','SG': 'SNOW GRAINS','GS': 'SMALL HAIL ANDOR SNOW PELLETS','PL': 'ICE PELLETS',
'IC': 'ICE CRYSTALS','FG\+': 'HEAVY FOG','FG': 'FOG','BR': 'MIST','UP': "UNKNOWN PRECIPITATION",'HZ': 'HAZE','FU': 'SMOKE',
'VA': 'VOLCANIC ASH','DU': 'WIDESPREAD DUST','DS': 'DUSTSTORM','PO': 'SAND_DUST WHIRLS',
'SA': 'SAND','SS': 'SANDSTORM','PY': 'SPRAY','SQ': 'SQUALL','DR': 'LOW DRIFTING','SH': 'SHOWER','FZ': 'FREEZING',
'MI': 'SHALLOW','PR': 'PARTIAL','BC': 'PATCHES','BL': 'BLOWING','VC': 'VICINITY'}

# builds out the identifying weather features
for i in weather_types:
    weather[i] = 0
    weather.loc[weather.CodeSum.str.contains(i) == True,i] = 1

weather.drop('CodeSum',axis=1,inplace=True)

n_weather = weather.iloc[12:,:] # for every day in the weather dataset after the 6th one
for i in range(1,7): # Hard-coded range of the last 6 days
    n_date = "_date-"+str(i)
    n_weather.loc[:,n_date] = n_weather.Date-pd.DateOffset(i)
    n_weather = pd.merge(left=n_weather,right=weather,left_on=[n_date,'Station'],right_on=['Date','Station'],suffixes =('',n_date))

# Creating de-duped df of traps and coordinates.
traps_master = test[['Trap', 'Coordinates']]
# Drop duplicates
traps_master.drop_duplicates(inplace=True)

# Create list of column names to use with for loops below
trap_cols = traps_master.Trap.tolist()

# Create dictionary of Trap IDs and corresponding lat/lon coordinate tuples
trap_dict = traps_master.set_index('Trap')['Coordinates'].to_dict()

# Creates dictionary where key is a Trap name, and the value for each is a list of the distances to every other trap.
distance_dict = {}
for i in trap_cols:
    dist_list = []
    for k in trap_dict:
        dist = distance(trap_dict[k], trap_dict[i])
        dist_list.append(dist)
    distance_dict[i] = dist_list


# Creates dictionary where key is a Trap name, and the value for each is a list of the compass bearings from every other trap.
bearing_dict = {}
for c in trap_cols:
    bearing_list = []
    for q in trap_dict:
        bearing = compass_bearing(trap_dict[q], trap_dict[c])
        bearing_list.append(bearing)
    bearing_dict[c] = bearing_list

# Creates df of relative distances.  To be merged with a left join into test df.
dist_df = pd.DataFrame.from_dict(distance_dict, orient='index')
distance_labels = dist_df.index.tolist()
distance_cols = []
for c in distance_labels:
    label = c + '_dist'
    distance_cols.append(label)
dist_df.columns = [distance_cols]
dist_df['Trap'] = dist_df.index
# dist_df.to_csv('../data/relative_locations.csv')


# Creates df of relative bearings.  To be merged with a left join into test df.
bearing_df = pd.DataFrame.from_dict(bearing_dict, orient='index')
bearing_labels = bearing_df.index.tolist()
bearing_cols = []
for c in bearing_labels:
    label = c + '_bearing'
    bearing_cols.append(label)
bearing_df.columns = [bearing_cols]
bearing_df['Trap'] = bearing_df.index
# bearing_df.to_csv('../data/relative_bearings.csv')
test = pd.merge(test, dist_df, how='left', left_on='Trap', right_on='Trap')
test = pd.merge(test, bearing_df, how='left', left_on='Trap', right_on='Trap')
test = pd.merge(test,n_weather,left_on=['Date','Weather_Station'],right_on=['Date','Station'])

# test = pd.read_csv('../data/input/test.csv')
species = set(test.Species)
species = [i for i in species]
species_labels = {}
for i,v in enumerate(species):
    species_labels[v] = i
test['species_labels'] = test['Species'].map(species_labels)

# Convert the date to the epoch
test['Epoch'] = test.Date.astype(np.int64) // 10**9

# test.to_csv('~/DropBox/DSI/test_transformed.csv')
