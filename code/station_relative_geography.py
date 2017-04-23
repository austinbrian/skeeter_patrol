#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 17:27:07 2017

@author: michaelsanders
"""

"""
Code for mapping every trap's relative position to every other trap in terms of a) distance (km) and b) compass bearing (in degrees).  Note, the bearing value shows bearings FROM other traps to the self trap.  This is intended to align to the wind bearing in the weather dataset, which depicts the direction the weather is coming FROM (http://www.ndbc.noaa.gov/measdes.shtml).

"""

## Checking to see if coordinates of the same trap ID change from year to year.  It appears they do not.
#traps_test = train[['Trap', 'Coordinates', 'Date']]
#traps_test['Year'] = traps_test.Date.map(lambda x : (x.year))
#traps_test.Year = traps_test.Year.astype(str)
#traps_test['Id_test'] = traps_test.Trap + traps_test.Year

           
           
# Creating de-duped df of traps and coordinates.
traps_master = train[['Trap', 'Coordinates']]

'''
two versions of trap T009:
    T009, (41.992478000000006, -87.862994999999998)
    T009, (41.981964000000005, -87.812826999999999)

converting first one to "T0009Alt"
'''

traps_master.loc[traps_master['Coordinates'] == (41.992478000000006, -87.862994999999998), 'Trap'] = 'T009Alt'


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


# Creates df of relative distances.  To be merged with a left join into train df.
dist_df = pd.DataFrame.from_dict(distance_dict, orient='index')
distance_labels = dist_df.index.tolist()
distance_cols = []
for c in distance_labels:
    label = c + '_dist'
    distance_cols.append(label)
dist_df.columns = [distance_cols] 
dist_df['Trap'] = dist_df.index
dist_df.to_csv('../data/relative_locations.csv')


# Creates df of relative bearings.  To be merged with a left join into train df.
bearing_df = pd.DataFrame.from_dict(bearing_dict, orient='index')  
bearing_labels = bearing_df.index.tolist()  
bearing_cols = []
for c in bearing_labels:
    label = c + '_bearing'
    bearing_cols.append(label)
bearing_df.columns = [bearing_cols]
bearing_df['Trap'] = bearing_df.index
bearing_df.to_csv('../data/relative_bearings.csv')


