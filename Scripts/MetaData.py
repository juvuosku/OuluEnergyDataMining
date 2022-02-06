import pandas as pd

from deep_translator import GoogleTranslator


class Characteristics():
    def __init__(self, csv_file=None):
        self.csv_file = csv_file
        if not csv_file:
            self.metadata_df = pd.read_csv('../ids_properties.csv')
        else:
            self.metadata_df = pd.read_csv(csv_file)
        translateConsumption(self.metadata_df)


def translateConsumption(df):
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
# meta_df = pd.read_csv('../ids_properties.csv')
# translateConsumption(meta_df)

"""print(meta_df.head())

print("The most occurring building intended uses:")
print(meta_df["intended_use"].value_counts(dropna=False)[0:10])"""
