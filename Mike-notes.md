#### Train dataset
- Show individual stations over time?
- Should we convert to epoch time?
    - concern is we don't want spurious correlations between WNV positive mosquitoes in different years


#### Weather dataset
- "CodeSum" values match weather event types; multiple types in many columns
    - need to split out into separate columns
- ResultSpeed is windspeed
- ResultDir is wind direction... but source or where it's headed to?
    - NOAA says it's the direction the wind is coming from in degrees clockwise from true N (http://www.ndbc.noaa.gov/measdes.shtml)
    - But that doesn't jive with other sources, that say the wind in Chicago in the spring and summer comes from the south (https://www.windfinder.com/windstatistics/chicago_midway)
    - per Jeff..maybe it's a factor of 10?
- Calc relative pressure against sea level (<1 is low pressure, >1 high pressure)
- Map out weather codes to individual columns and get dummies



#### General ideas
- Can we organize trap locations by whether they are upwind or downwind on a particular day?


#### Draft Hypotheses
1. The location of a WNV positive result can be predicted based on features of WNV positives in the relatively near past
    - e.g., wind direction, humidity/wetness, relative location to the station where the positive was detected
2. Are there locations that are more likely to have WNV positives generally (regardless of relation to other locations)?  
    - Maybe these areas are likely to have WNV positives...for some reason we don't know...but we spray there anyway...?
