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
