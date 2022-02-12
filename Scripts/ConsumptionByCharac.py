from datetime import datetime
import pandas as pd

from Consumption import Retrospective
from MetaData import Characteristics

# Fetch buildings characteristics
metadata = Characteristics()
meta_df = metadata.metadata_df


# -----------------------------------FloorCount-----------------------------------

# The goal here is to study the consumption of buildings by their floorcount
# By look at their consumption average for example

from math import isnan

nbOfPropertyByFloorcount = 10

# Init a floorcount list
floorcounts = [0, 1, 2, 3, 4, 5]  # or using df["floorcount"].value_counts()

# Dicts to observe missing data
missingPropertyDataByFloorcount = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
numberOfPropertyDataByFloorcount = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

# To find the buildings' id for each different floorcount
idsByFloorcount = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

for floorcount in floorcounts:
    # Choosing the first 5 buildings for each different floorcount
    floor_df = meta_df.loc[(meta_df["floorcount"] == floorcount)][0:nbOfPropertyByFloorcount]
    idsByFloorcount[floorcount] = floor_df["property_id"].tolist()

    numberOfPropertyDataByFloorcount[floorcount] = len(floor_df)

print("-----Buildings' id for each different floorcount-----")
print(str(idsByFloorcount))

print()

print("-----Number of buildings for each different floorcount-----")
print(str(numberOfPropertyDataByFloorcount))

print()

# To retrieve the consumption's mean of each building in the dict above
meansByBuildingList = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

# Creating a retrospective of every buildings we have looked for this case
ids = []

for _, property_ids in idsByFloorcount.items():
    for property_id in property_ids:
        ids.append(property_id)

print("---ids:---")
print(str(ids))
print()

start_time = datetime(2019, 1, 1, 0)
end_time = datetime(2020, 1, 1, 0)

retro = Retrospective(ids, start_time, end_time)

for property_id in ids:
    floorcount = meta_df[meta_df["property_id"] == property_id]["floorcount"]
    floorcount = floorcount.iloc[0]

    mean = retro.getMeanEnergyByProperty(property_id)

    # Checking if the consumption value is valid
    if mean[0] != mean[0]:
        missingPropertyDataByFloorcount[floorcount] += 1
        mean[0] = 0
    else:
        mean[0] = round(mean[0])

    if mean[1] != mean[1]:
        mean[1] = 0
    else:
        mean[1] = round(mean[1])

    if mean[0] != 0 and mean[1] != 0:
        meansByBuildingList[floorcount].append(mean)

print("-----Consumptions mean (heat, elec) sorted by floorcount, still separated by building-----")
print(str(meansByBuildingList))
print()

meansByFloorcount = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

for floorcount, means in meansByBuildingList.items():
    final_mean = [0, 0]
    for mean in means:
        final_mean[0] += mean[0]
        final_mean[1] += mean[1]

    if len(means) > 0:
        final_mean[0] = round(final_mean[0] / len(means), 2)
        final_mean[1] = round(final_mean[1] / len(means), 2)

    # numberOfPropertyDataByFloorcount[floorcount]=len(means)

    meansByFloorcount[floorcount] = final_mean

print("-----Consumptions mean (heat, elec) sorted by floorcount, now grouped by floorcount only-----")
print(str(meansByFloorcount))
print()

# -----------------------------------------------------------------------------
