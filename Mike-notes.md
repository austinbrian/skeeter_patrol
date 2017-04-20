#### Train dataset
- Show individual stations over time?
- Should we convert to epoch time?
    - concern is we don't want spurious correlations between WNV positive mosquitoes in different years
- what do we do with stations and satellites... merge together?


#### Weather dataset
- "CodeSum" values match weather event types; multiple types in many columns
    - need to split out into separate columns
- ResultSpeed is windspeed
- ResultDir is wind direction... but source or where it's headed to?
    - NOAA says it's the direction the wind is coming from in degrees clockwise from true N (http://www.ndbc.noaa.gov/measdes.shtml)
    - **multiply by 10** (it's in the docs, next to category "Wind")
- Calc relative pressure against sea level (<1 is low pressure, >1 high pressure)
- Map out weather codes to individual columns and get dummies


#### Feature engineering, etc.
- Create function to calculate distance between two traps based on their lat/longs
- 




#### General ideas
- Can we organize trap locations by whether they are upwind or downwind on a particular day?


#### Draft Hypotheses
1. The location of a WNV positive result can be predicted based on features of WNV positives in the relatively near past
    - e.g., wind direction, humidity/wetness, relative location to the station where the positive was detected
    - DBSCAN
2. Are there locations that are more likely to have WNV positives generally (regardless of relation to other locations)?  
    - Maybe these areas are likely to have WNV positives...for some reason we don't know...but we spray there anyway...?



#### Research Questions
- How to compare two sets of coordinates and get geographic relation (e.g. distance and direction)
- Wind direction issue (multiply by 10?)



#### Exploratory modeling
- DBSCAN and K-Means -- see if it finds the WNV positives?
