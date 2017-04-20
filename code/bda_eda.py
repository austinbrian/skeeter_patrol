#!bin/bash/python

import pandas as pd
import numpy as np

weather = pd.read_csv('../data/input/weather.csv')
# Station 1 is O'Hare, Station 2 is Midway

weather_types = {
'\+FC': 'TORNADO/WATERSPOUT',
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
'FG\+': 'HEAVY FOG',
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

for i in weather_types:
    weather[i] = 0
    weather.loc[weather.CodeSum.str.contains(i) == True,i] = 1
