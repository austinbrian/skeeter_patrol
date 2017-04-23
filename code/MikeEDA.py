#!bin/bash/python

import numpy as np
import pandas as pd
import datetime

train = pd.read_csv('../data/input/train.csv')
train.Date = pd.to_datetime(train.Date)

train.loc[train['Coordinates'] == (41.992478000000006, -87.862994999999998), 'Trap'] = 'T009Alt'

train_geo_df = pd.merge(train, dist_df, how='left', left_on='Trap', right_on='Trap')
train_geo_df = pd.merge(train_geo_df, bearing_df, how='left', left_on='Trap', right_on='Trap')






weather = pd.read_csv('../data/input/weather.csv')
weather.Date = pd.to_datetime(weather.Date)





train.columns
train.dtypes

train.AddressAccuracy.head()
train.Date.head()
train.Date = pd.to_datetime(train.Date)
#train['epoch_time'] = train_set.Date.astype('int64')//1e9

train.Address.head()

train.WnvPresent.value_counts()

train.groupby([train.Date.year, train.Date.month]).WnvPresent.value_counts()

WNV_by_month_year = train.groupby(by=[train.Date.map(lambda x : (x.year, x.month))]).WnvPresent.value_counts()

WNV_by_year = train.groupby(by=[train.Date.map(lambda x : (x.year))]).WnvPresent.value_counts()

train.Trap.astype(str, inplace=True)

trap_loc_test = train.groupby('Trap').Street.nunique()

t009 = train[train.Trap=='T009']
t009.reindex()
point1 = (t009.loc[50, "Latitude"], t009.loc[50, "Longitude"])
point2 = (t009.loc[3962, "Latitude"], t009.loc[3962, "Longitude"])
higgins_dist = distance(point1, point2)

#spray.Date = pd.to_datetime(spray.Date)
#sprays_by_year = spray.groupby(by=[spray.Date.map(lambda x : (x.year))]).count()


weather = pd.read_csv('data/input/weather.csv')
weather.CodeSum.value_counts()
expanded_codes = weather['CodeSum'].str.split(' ', expand=True)

weather_data_check = weather.groupby(by=[weather.Date.map(lambda x: (x.year, x.month))]).Station.value_counts()
weather = pd.concat([weather,pd.DataFrame(columns=weather_cols)])



weather_types = {
'+FC': 'TORNADO/WATERSPOUT',
'FC': 'FUNNEL CLOUD',
'TS': 'THUNDERSTORM',
'GR': 'HAIL',
'RA': 'RAIN',
'DZ': 'DRIZZLE',
'SN': 'SNOW',
'SG': 'SNOW GRAINS',
'GS': 'SMALL HAIL ANDOR SNOW PELLETS',
'PL': 'ICE PELLETS',
'IC': 'ICE CRYSTALS',
'FG+': 'HEAVY FOG',
'FG': 'FOG',
'BR': 'MIST',
'UP': "UNKNOWN PRECIPITATION",
'HZ': 'HAZE',
'FU': 'SMOKE',
'VA': 'VOLCANIC ASH',
'DU': 'WIDESPREAD DUST',
'DS': 'DUSTSTORM',
'PO': 'SAND_DUST WHIRLS',
'SA': 'SAND',
'SS': 'SANDSTORM',
'PY': 'SPRAY',
'SQ': 'SQUALL',
'DR': 'LOW DRIFTING',
'SH': 'SHOWER',
'FZ': 'FREEZING',
'MI': 'SHALLOW',
'PR': 'PARTIAL',
'BC': 'PATCHES',
'BL': 'BLOWING',
'VC': 'VICINITY'}




#weather['epoch_time'] = weather.Date.astype('int64')//1e9


spray = pd.read_csv('data/input/spray.csv')
spray['comb_time'] = spray.Date + ' ' + spray.Time
spray.comb_time = pd.to_datetime(spray.comb_time)
spray['epoch_time'] = spray.comb_time.astype('int64')//1e9
     
#test = pd.read_csv('data/input/test.csv')     
    
#weather_test = weather.copy()
#weather_test.Tavg.astype(str, inplace=True)
#weather_test.Tavg = weather_test.Tavg.replace('M', np.nan)
#weather_test.Tavg.isnull().sum()
#weather_test.dropna(inplace=True)
#weather_test.Tavg.astype(int, inplace=True)


#weather_test['avg_check'] = ((weather_test.Tmax + weather_test.Tmin) / 2).astype(int)

#assert weather_test.avg_check == weather_test.Tavg

