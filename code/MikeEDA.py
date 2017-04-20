#!bin/bash/python

import numpy as np
import pandas as pd


train_set = pd.read_csv('data/input/train.csv')

train_set.columns
train_set.dtypes

train_set.AddressAccuracy.head()
train_set.Date.head()
train_set.Date = pd.to_datetime(train_set.Date)
train_set['epoch_time'] = train_set.Date.astype('int64')//1e9

train_set.Address.head()

train_set.WnvPresent.value_counts()

train_set.groupby([train_set.Date.year, train_set.Date.month]).WnvPresent.value_counts()

WNV_by_month_year = train_set.groupby(by=[train_set.Date.map(lambda x : (x.year, x.month))]).WnvPresent.value_counts()

WNV_by_year = train_set.groupby(by=[train_set.Date.map(lambda x : (x.year))]).WnvPresent.value_counts()





weather = pd.read_csv('data/input/weather.csv')
weather.CodeSum.value_counts()
expanded_codes = weather['CodeSum'].str.split(' ', expand=True)



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


weather_cols = []
for key in weather_types:
    weather_cols.append(weather_types[key])

weather = pd.concat([weather,pd.DataFrame(columns=weather_cols)])
weather.Date = pd.to_datetime(weather.Date)
weather['epoch_time'] = weather.Date.astype('int64')//1e9


spray = pd.read_csv('data/input/spray.csv')
spray['comb_time'] = spray.Date + ' ' + spray.Time
spray.comb_time = pd.to_datetime(spray.comb_time)
spray['epoch_time'] = spray.comb_time.astype('int64')//1e9