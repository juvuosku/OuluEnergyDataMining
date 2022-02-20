from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

from Consumption import Retrospective
from MetaData import Characteristics
import numpy as np

# Fetch buildings characteristics
metadata = Characteristics()
meta_df = metadata.metadata_df


def consumptionByDistrict(
    district_key, start_time=datetime(2019, 1, 1, 0),
    end_time=datetime(2020, 1, 1, 0),
    nbOfBuildingByDistricts=2, DistrictRange=6):
    district_list = meta_df["district_key"].value_counts(dropna=False)[
    0:DistrictRange].index.tolist()

    # Missing values
    missingValidPropertyDataByDistrict = {
    "district_key": district_list,
    'Missing Data': [0 for i in range(DistrictRange)],
    'Valid Data': [0 for i in range(DistrictRange)]}

    # To find the buildings' id for each different district
    idsByUse = pd.DataFrame(columns=["district_key", "property_id", "average_heat", "average_electricity"])

    for district in district_list:
        distDF = meta_df.loc[(meta_df["district_key"] == district)][0:nbOfBuildingByDistricts]
        ids = distDF["property_id"].tolist()

        retro = Retrospective(ids, start_time, end_time)
        for building_id in ids:
            mean = retro.getMeanEnergyByProperty(building_id)

            district_index = missingValidPropertyDataByDistrict["district_key"].index(district)
            if mean[0] != mean[0] or mean[1] != mean[1]:
                missingValidPropertyDataByDistrict['Missing Data'][district_index] += 1
                mean[0] = 0
                mean[1] = 0
            else:
                missingValidPropertyDataByDistrict['Valid Data'][district_index] += 1
                mean[0] = round(mean[0], 2)
                mean[1] = round(mean[1], 2)

                dic = {"district_key": district,
                    "property_id": building_id,
                    "average_heat": mean[0],
                    "average_electricity": mean[1]}

                idsByUse = idsByUse.append(dic, ignore_index=True)

    # General means by use
    meanByDistrictDF = idsByUse.groupby(district).mean()
    meanByDistrictDF = meanByDistrictDF.reset_index()

    print(meanByDistrictDF)

    # Graphs --------------------------
    # To plot the number of missing/invalid vs valid values-------------------------

    missingValidDataDF = pd.DataFrame.from_dict(missingValidPropertyDataByDistrict)
    missingValidDataDF = missingValidDataDF.set_index(district)
    meanByDistrictDF = meanByDistrictDF.drop("property_id", axis=1)

    print(missingValidDataDF)

    Ntotal = missingValidDataDF["Valid Data"].sum() + missingValidDataDF["Missing Data"].sum()

    fig = missingValidDataDF[['Missing Data', 'Valid Data']].plot(stacked=True,
                                                                  width=0.7,
                                                                  figsize=(12, 6),
                                                                  kind='bar',
                                                                  xlabel=district,
                                                                  ylabel="Total Number of Buildings sample",
                                                                  rot=0,
                                                                  color=["dodgerblue", "lightgray"],
                                                                  fontsize="large",
                                                                  )
    plt.title("Number of Missing/Invalid & Valid Building samples by " + district + ", N=" + str(
        Ntotal) + "(N: total number of samples)", fontweight="bold",
              fontsize=16)

    fig = fig.get_figure()
    fig.savefig('../Graphs/' + district + '/' + district + 'MissingData.png')

    plt.show()

    # To plot the Proportion of missing/invalid vs valid values-------------------------

    missingValidDataDF_prop = pd.DataFrame(columns=[district, 'Missing Data', 'Valid Data'])
    for district in missingValidDataDF.index.tolist():
        missing_data = missingValidDataDF.loc[district, 'Missing Data']
        valid_data = missingValidDataDF.loc[district, 'Valid Data']

        missing_prop = round((missing_data / (missing_data + valid_data)), 2)
        valid_data = round((valid_data / (missing_data + valid_data)), 2)

        dic = {'District': district,
               'Missing Data': missing_prop,
               'Valid Data': valid_data}

        missingValidDataDF_prop = missingValidDataDF_prop.append(dic, ignore_index=True)

    missingValidDataDF_prop = missingValidDataDF_prop.set_index(district)

    fig = missingValidDataDF_prop[['Missing Data', 'Valid Data']].plot(stacked=True,
                                                                       width=0.7,
                                                                       figsize=(14, 6),
                                                                       kind='bar',
                                                                       xlabel=district,
                                                                       ylabel="Proportion of missing or valid Buildings sample ",
                                                                       rot=0,
                                                                       color=["dodgerblue", "lightgray"],
                                                                       fontsize="large",
                                                                       )
    plt.title("Proportion of Missing/Invalid & Valid Building samples by " + district + ", N=" + str(Ntotal),
              fontweight="bold",
              fontsize=16)

    for n, x in enumerate([missingValidDataDF.index.values]):

        for (proportion, count, y_loc) in zip(missingValidDataDF_prop.loc[x],
                                              missingValidDataDF.loc[x],
                                              missingValidDataDF_prop.loc[x].cumsum()):
            if proportion > 0:
                plt.text(x=n - 0.17,
                         y=(y_loc - proportion) + (proportion / 2),
                         s=f{count}\n({np.round(proportion * 100, 1)}%),
                         color="black",
                         fontsize=12,
                         fontweight="bold")

    fig = fig.get_figure()
    fig.savefig('../Graphs/' + district + '/ ' + district + 'ProportionMissingData.png')

    plt.show()

    # To plot the average energy consumption of by district-------------------------

    Nvalid = missingValidDataDF["Valid Data"].sum()

    fig = meanByDistrictDF.plot.bar(x=district,
                                          rot=0,
                                          width=0.8,
                                          color=["darkorange", "royalblue"],
                                          figsize=(10, 4),
                                          xlabel=district,
                                          ylabel="Average Energy Consumption",
                                          fontsize='large')

    plt.title('Average Energy Consumption by ' + district + ', N=' + str(Nvalid)
              + "(N: number of valid samples)", fontweight="bold", fontsize=16)

    fig = fig.get_figure()
    fig.savefig('../Graphs/' + district + '/averageConsumptionBy' + district + '.png')

    plt.show()



district_ids = ["district_key"]
for district in district_ids:
    nbOfBuildingByDistrict = 30
    DistrictRange = 10
    

    consumptionByDistrict(district, nbOfBuildingByDistrict=nbOfBuildingByDistrict,
                                           DistrictRange=DistrictRange)
