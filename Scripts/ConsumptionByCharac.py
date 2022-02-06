from datetime import datetime
import pandas as pd

from Consumption import Retrospective
from MetaData import Characteristics

# Fetch buildings characteristics
metadata = Characteristics()
meta_df = metadata.metadata_df

# The goal here is to study the consumption of buildings by their floorcount
# By look at their consumption average for example

# Init a floorcount list
floorcounts = [0, 1, 2, 3, 4, 5]  # or using df["floorcount"].value_counts()

# To find the buildings' id for each different floorcount
idsByFloorcount = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

for floor in floorcounts:
    floor_df = meta_df.loc[(meta_df["floorcount"] == floor)]
    idsByFloorcount[floor] = floor_df["property_id"].tolist()

print("Buildings' id for each different floorcount")
print(floorcounts)

# To retrieve the consumption's mean of each building in the dict above
meansByFloorcount = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

start_time = datetime(2019, 1, 1, 0)
end_time = datetime(2020, 1, 1, 0)
for floor in floorcounts:
    consumption = Retrospective(idsByFloorcount[floor], start_time, end_time)  # heat and electricity
    meansByFloorcount[floor] = consumption.getMeanEnergy()

print("Consumption's mean of each building, sorted as above")
print(meansByFloorcount)

# To get the final means by floorcount
means = []
for k, v in meansByFloorcount.items():
    heat_mean = 0
    elec_mean = 0

    for mean in v:
        heat_mean += mean[0]
        elec_mean += mean[1]

    means.append((heat_mean / len(v), elec_mean / len(v)))

print("Final consumption means by floorcount, (heat, electricity)")
print(meansByFloorcount)
