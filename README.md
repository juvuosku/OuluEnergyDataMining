# OuluEnergyDataMining
Master Student Data Mining project to study Oulu's buildings energy consumption


I think using Python is a good idea since it offers a lot of Data Science libraries, especially Pandas, which could be very useful, so let's use it unless someone has a better proposition.
There is a jupyter notebook to show you some ways to play with the data in case you are not familiar with Pandas dataframes.

Ideas to explore

- Create a function that retrieves a set of rows from the JSON file accessible by an URL (see mentor's email about that).
It should at least have the following parameters: a property id (to select a specific property), a starting date (year, month, day, hour), a delta time of observation (year, month, day, hour), and an energy type (heat or electricity).
It should return a dataframe of the consumption (electricity or heat) of a specific property from a precise time to another precise time. Done (Marius)

- Create a function that plots energy consumption from a dataframe.
It should have the following parameters: a dataframe (see function above)
Plot a 2D plot (energy consumption in the function of time, two curves: heat and electricity)

- Create a function to plot some scatterplots to compare total/annual consumption according to the floorcount, area,...
It should have the following parameters: a list of dataframes, a list of metadata parameter
I'm not quite sure of what it should compare but try some things and take some notes if you find interesting results.

- Create a function that translates an entire column of a dataframe
Parameters: a dataframe, a string to indicate which column to translate.

- Find a way to manage missing data, for example, "year_built" which has a lot of 0 instead of the actual year. This task would require some research so try multiple strategies and take some notes.

# Research questions
- How the building type and its characteristics (like the floor count, the year of construction or its intended use) impact its yearly energy consumption and which of these parameters are more impactful?
- How can we cluster different profiles of energy consumption using k-means or other clustering methods?
- How does the energy consumption varies in Oulu on a district or an entire city level through the years? Are some districts consuming more energy? Did major changes occurred at some point?
- How far and how accurately can we forecast single or group of buildings (e.g. by district or by intended use) by using NN or ML models?

Compact research question:

How do the buildings' characteristics impact their yearly energy consumption, which ones are the most impactful and can we cluster some of these consumption profiles?
or

How does the energy consumption varies in Oulu on a district or an entire city level through the years? Are some districts consuming more energy? Did major changes occurred at some point and can we compare them to the city's development?
Can we predict this change using ML models

The second question is probably too ambitious, we will probably miss the needed data since most of it only started after 2016 and ends at the end of 2019. 
So we shouldn't be able to notice that major changes in only a couple of years.

However, we could use some of 2nd question's sub-questions to add some analysis to the first research question.




So the final question could be:

How do the buildings' characteristics (floorcount, year of construction, district), or their location in the city impact their yearly energy consumption, which ones are the most impactful and can we cluster some of these consumption profiles and identify more consumptive districts using k-means or similar methods?

This question would have multiple steps:

Analysing building's charachteristics one by one and look for change in the consumption values according to their values.

The building's district is also a part of these charachteristics but more complex to analyse, so this will need more work.

They will also need the data to be clean as we go, we won't be able to predict every preprocessing steps from the begininng.

Finally, we will have to find a way to use clusterization methods to identify some consumption profiles.