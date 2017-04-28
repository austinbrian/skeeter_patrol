# Report of Findings for Skeeter Patrol, LLC
-----
### Background
West Nile Virus (WNV) is commonly spread when infected mosquitos bite humans. Symptoms of WNV can vary from fever to death in the most extreme cases. The Chicago Department of Public Health (CDPH) has limited resources and would like to better predict when WNV will be present among the local mosquito population. Accurate predictions of WNV will help the CDPH in allocating resources to spray of airborne pesticides to control adult mosquito populations.

### Problem statement
The purpose of this project is to determine which of the mosquito traps in the city of Chicago had mosquitos with West Nile virus for the years of 2008, 2010, 2012, and 2014.

### Information Provided
* The data provided includes the city's survey of odd-numbered years from 2007 to 2013, in which they checked the number of mosquitos at mosquito traps arrayed throughout the city on a weekly basis.
* The locations that had been sprayed by a pesticide in 2007, 2011, and 2013.
* Trap-level observations include:
 * A unique **trap identifier**
 * The **date** the test is performed
 * Street **address and block number** of the trap
 * Measure of the **accuracy of the street address** provided for the trap
 * The **species of mosquito** identified
 * **Latitude and longitude** associated with the trap address
 * The **number of mosquitos** discovered during odd-numbered years
 * Whether the **trap tested positive** for West Nile Virus on a given date
* **Weather data** for the months of May-October from 2007 to 2014, with two observations for each date
* A full list of all the species and traps anticipated to be in the even-year data.

### Data Cleaning
* Two of the traps, T009 and T035, were listed at two locations at various points of both the test and training data. We created named an arbitrarily-chosen one of these traps an "alternate" trap by associating it with the coordinates of its latitude and longitude.
* The capacity of each trap was limited to 50 mosquitos, so where there more more than 50 discovered in a trap on a date, there are multiple entries for the same trap/date/species of mosquito. we solved this issue by combining the observations for a day using a groupby and transform statement. This aggregated the total number of a species found in a trap on a date.
```python
df['Grouped_Mosquitos'] = df.groupby(['Trap','Date','Species'])['NumMosquitos'].transform(sum)
```
* The weather documentation included a column that described all of the type of weather on a given date. We transformed this into a series of columns that counted the number of types a weather type was observed.
* Weather information also included two sets of observations for a given date, labeled as Station 1 and Station 2.
* Where null values in the weather data existed, we imputed these values with the following algorithm: for the missing weather observation, we looked up the average temperature (column *Tavg*) on the same date; we then searched for the average value of the column to be imputed when the weather was at the average temperature for the entire dataset, and used that number as the imputed value.
* Weather information included "M" and "T" in certain columns; we determined that "T" stood for "trace amounts" and replaced it with 0.05 (halfway between the minimum amount of that column and 0). "M" was changed to *NaN* format.

### Hypotheses
* After initial review of the data, our team hypothesized that there were two primary factors driving West Nile Virus: the physical location of traps and the weather in the week prior to a trap's selection.
* While we thought that the location was important, we hypothesized that the actual trap at which a mosquito was found was somewhat arbitrary, since the traps were in relatively close proximity. To incorporate this idea into our modeling, we considered that the locations of *other* traps relative to any given trap was an important component.
* While the team considered that the spray data would have an effect on the population of WNV-infected mosquitos, after reviewing the data, we noticed that there was no spray data for the even-numbered years we were projecting. We hypothesized that spray effectiveness would not be applicable in the following year, so excluded it from our analysis.
 * *Given more time, our team would have developed assumptions about the missing years of spray data to incorporate it into our model.*


### Approach
* Concurrent with our first hypothesis, that the location and weather were the primary factors, we built features in two ways:
 1. For each trap, we calculated the distance from that trap to every other trap in the dataset using latitude/longitude tuples and saved this distance "as the crow flies" as a matrix. We further described this distance by calculating the compass bearing between each two points.
 2. For each dated observation, we determined whether the trap in question was closer to Station 1 or Station 2 (identified as O'Hare Airport and Midway Airport, respectively). Using the closer airport, we pulled in the full depiction of the day's weather for each date observation. We then looked up the date for the prior day's weather and included it as additional observations. We continued this process until we had built in the weather for all days until n-6.

 This resulted in a very long list of features.
 ![](http://g.recordit.co/v4UDa7bDuW.gif)
* Using this long list of features, we attempted to classify each date/trap/species of mosquito combination as likely to have West Nile Virus present or not.
* Each of these features were replicated for the testing set as well, since the weather and location information were both included for the years to be predicted.
* Classification tactics included: logistic regression, random forest classification, k-nearest-neighbors classification, Ada-boosted random forest, XGBoost, and support vector machines.
* Because we had such a high number of dimensions, our team decomposed our training data using principal component analysis, and evaluated each of our classifiers using 30 features, which explained ~85% of the variance in our data.
* We evaluated the performance of our classifier using a test-train split in which 33% of our training data was classified on the fit of a given model, and the area under the Radio Operator Curve was measured.


### Findings
* Our initial modeling tactics demonstrated that the most predictive data points in the model were the points around the number of mosquitos observed in an individual trap. Since this variable was not available in the test data, we resolved to estimate this value using regression.
* Estimating this value with linear regression was somewhat unreliable, and materially
* We attempted to perform a clustering analysis that would mimic the number of mosquitos projected, which we could then use to classify the data in ways that would distinguish between WNV classes. We used a Hierarchical DBSCAN method to classify the data, but found that the 104 clusters did not reliably discriminate between times when WNV was present and when it was not.
