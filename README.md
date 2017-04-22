# Kaggle competition project
## Skeeter Patrol, LLC
------

The purpose of this project is to determine which of the mosquito traps in the city of Chicago had mosquitos with West Nile virus.

### Global Goal
* Given this trap and this mosquito species on this date, how does weather (and weather for the past week) and whether or not it was sprayed affect the likelihood for a trap/mosquito/date combo to have WNV present?

### Training Data
* Includes 9955 non-WNV observations, and 551 WNV observations
* T009 and T0035 have multiple street locations
  `train[train.Trap =='T035'].Address.value_counts()`
* AddressAccuracy -- {9:premesis, 8:address-level, 5:postcode, 6:street-level, 3:county-municipality}

### Weather Data
* Station 1 is O'Hare, and Station 2 is Midway airport
* Heating and cooling data are a new baseline centered at 65 degrees ... for some reason?
*
