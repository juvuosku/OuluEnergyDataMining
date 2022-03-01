#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from Consumption import Retrospective
from MetaData import Characteristics


# In[ ]:
# Fetch buildings characteristics

metadata = Characteristics()
# In[ ]:

meta_df = metadata.metadata_df


# In[ ]:


def consumptionByDistrict(
    district_key, start_time=datetime(2019, 1, 1, 0),
    end_time=datetime(2020, 1, 1, 0),
    nbOfBuildingByDistrict=2, DistrictRange=6):
    district_list = meta_df["district_key"].value_counts(dropna=False)[
    0:DistrictRange].index.tolist()
    district_list.sort()

    # Missing values
    missingValidPropertyDataByDistrict = {
    "district_key": district_list,
    'Missing Data': [0 for i in range(DistrictRange)],
    'Valid Data': [0 for i in range(DistrictRange)]}

    # To find the buildings' id for each different district
    idsByUse = pd.DataFrame(columns=["district_key", "property_id", "average_heat", "average_electricity"])
    for district in district_list:
        print('Processing district %s' % district)
        distDF = meta_df.loc[(meta_df["district_key"] == district)][0:nbOfBuildingByDistrict]
        ids = distDF["property_id"].tolist()
        retro = Retrospective(ids, start_time, end_time)
        for building_id in ids:
            print('  Processing building %s' % building_id)
            mean = retro.getMeanEnergyByProperty(building_id)
            district_index = missingValidPropertyDataByDistrict["district_key"].index(district)
            if mean[0] != mean[0] or mean[1] != mean[1]:
                print('  Missing values')
                missingValidPropertyDataByDistrict['Missing Data'][district_index] += 1
                mean[0] = 0
                mean[1] = 0
            else:
                print('  Mean values: %f %f' % (mean[0], mean[1]))
                missingValidPropertyDataByDistrict['Valid Data'][district_index] += 1
                mean[0] = round(mean[0], 2)
                mean[1] = round(mean[1], 2)
                dic = {"district_key": district,
                    "property_id": building_id,
                    "average_heat": mean[0],
                    "average_electricity": mean[1]}
                idsByUse = idsByUse.append(dic, ignore_index=True)

    # General means by use
    meanByDistrictDF = idsByUse.groupby('district_key').mean()
    meanByDistrictDF = meanByDistrictDF.reset_index()
    print(meanByDistrictDF)
    # Graphs --------------------------
    # To plot the number of missing/invalid vs valid values-------------------------
    missingValidDataDF = pd.DataFrame.from_dict(missingValidPropertyDataByDistrict)
    missingValidDataDF = missingValidDataDF.set_index('district_key')
    try:
        meanByDistrictDF = meanByDistrictDF.drop("property_id", axis=1)
    except:
        print("Error!!!")
    print(missingValidDataDF)
    Ntotal = missingValidDataDF["Valid Data"].sum() + missingValidDataDF["Missing Data"].sum()
    fig = missingValidDataDF[['Missing Data', 'Valid Data']].plot(stacked=True,
                                                              width=0.7,
                                                              figsize=(12, 6),
                                                              kind='bar',
                                                              xlabel='district',
                                                              ylabel="Total Number of Buildings sample",
                                                              rot=0,
                                                              color=["dodgerblue", "lightgray"],
                                                              fontsize="large",
                                                              )
    plt.title("Number of Missing/Invalid & Valid Building samples, N=" + str(
        Ntotal) + "(N: total number of samples)", fontweight="bold",
          fontsize=16)
    fig = fig.get_figure()
    path = '../Graphs/' 
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
    fig.savefig(path +  'MissingData.png')
    #plt.show()

    # To plot the Proportion of missing/invalid vs valid values-------------------------
    """
    missingValidDataDF_prop = pd.DataFrame(columns=['district_key', 'Missing Data', 'Valid Data'])
    for district in missingValidDataDF.index.tolist():
            missing_data = missingValidDataDF.loc[district, 'Missing Data']
            valid_data = missingValidDataDF.loc[district, 'Valid Data']
            missing_prop = round((missing_data / (missing_data + valid_data)), 2)
            valid_data = round((valid_data / (missing_data + valid_data)), 2)
            dic = {'District': district,
                   'Missing Data': missing_prop,
                   'Valid Data': valid_data}
            missingValidDataDF_prop = missingValidDataDF_prop.append(dic, ignore_index=True)
            missingValidDataDF_prop = missingValidDataDF_prop.set_index('district_key')
            fig = missingValidDataDF_prop[['Missing Data', 'Valid Data']].plot(stacked=True,
                                                                           width=0.7,
                                                                           figsize=(14, 6),
                                                                           kind='bar',
                                                                           xlabel='district',
                                                                           ylabel="Proportion of missing or valid Buildings sample ",
                                                                           rot=0,
                                                                           color=["dodgerblue", "lightgray"],
                                                                           fontsize="large",
                                                                           )
            plt.title("Proportion of Missing/Invalid & Valid Building samples by, N=" + str(Ntotal),
                  fontweight="bold",
                  fontsize=16)
            ##print(missingValidDataDF.index.values)
            for n, x in enumerate([missingValidDataDF.index.values]):
                for (proportion, count, y_loc) in zip(missingValidDataDF_prop.loc[x],
                                                  missingValidDataDF.loc[x],
                                                  missingValidDataDF_prop.loc[x].cumsum()):
                    print('Type proportion %s, val %s' % (type(proportion), proportion))
                    if proportion > 0:
                        plt.text(x=n - 0.17,
                             y=(y_loc - proportion) + (proportion / 2),
                             s=f'{count}\n({np.round(proportion * 100, 1)}%)',
                             color="black",
                             fontsize=12,
                             fontweight="bold")
            fig = fig.get_figure()
            fig.savefig('../Graphs/' + district + '/ ' + district + 'ProportionMissingData.png')
            
            #plt.show()
    """
    # To plot the average energy consumption of by district-------------------------
    Nvalid = missingValidDataDF["Valid Data"].sum()
    fig = meanByDistrictDF.plot.bar(  x='district_key',
                                      rot=0,
                                      width=0.8,
                                      color=["darkorange", "royalblue"],
                                      figsize=(10, 4),
                                      xlabel='district',
                                      ylabel="Average Energy Consumption",
                                      fontsize='large')
    plt.title('Average Energy Consumption by district, N=' + str(Nvalid)
          + "(N: number of valid samples)", fontweight="bold", fontsize=16)
    fig = fig.get_figure()
    path = '../Graphs/'
    isExist = os.path.exists(path)
    if not isExist:
        # Create a new directory because it does not exist 
        os.makedirs(path)
    fig.savefig(path + 'averageConsumptionByDistrict.png')
        #plt.show()
# In[ ]:



district_ids = ["district_key"]
for district in district_ids:
    nbOfBuildingByDistrict = 10
    DistrictRange = 27
    
    consumptionByDistrict(district, nbOfBuildingByDistrict=nbOfBuildingByDistrict,
                                           DistrictRange=DistrictRange)

