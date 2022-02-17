import pandas as pd
import numpy as np
from numpy import asarray
from numpy import savetxt

from deep_translator import GoogleTranslator


class Characteristics():
    def __init__(self, csv_file=None):
        """self.csv_file = csv_file
        if not csv_file:
            self.metadata_df = pd.read_csv('../ids_properties.csv')
        else:
            self.metadata_df = pd.read_csv(csv_file)
        translateIntendedUse(self.metadata_df)"""
        self.metadata_df = pd.read_pickle("../translated_metadata.pkl")


def translateIntendedUse(df):
    # Saving the intended uses
    useDf = df["intended_use"].values.tolist()

    # Translating the sub-dataframe
    new_use_list = []
    i = 0
    for use in useDf:
        if isinstance(use, str):
            new_use_list.append(GoogleTranslator(source='fi', target='en').translate(text=use))
        else:
            new_use_list.append("Error")

    # Deleting obsolete columns
    df.drop("intended_use", axis=1, inplace=True)

    # Putting the new normalized column to the df
    df["intended_use"] = new_use_list


# Test
"""meta_df = pd.read_csv('../ids_properties.csv')
translateConsumption(meta_df)

print(meta_df.head())

print("The most occurring building intended uses:")
print(meta_df["intended_use"].value_counts(dropna=False)[0:10])

print("Properties' id")
unique_ids = asarray([ meta_df["property_id"].unique() ])
savetxt('unique_ids.csv', unique_ids, delimiter=',')"""
