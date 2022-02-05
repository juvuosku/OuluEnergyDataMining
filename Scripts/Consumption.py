from datetime import datetime
from itertools import product
import pandas as pd

hourly_url = "https://api.ouka.fi/v1/properties_consumption_hourly"


class Retrospective():
    def __init__(self, property_ids, start_time, end_time, energy_type=None):
        """
        Create a dataframe containing the energy consumption of properties
        listed by their ids during a precise time interval.
        We can also choose to retrieve only a certain energy type ("Electricity", "Heat" or both).
        """

        self.property_ids = property_ids
        self.start_time = start_time
        self.end_time = end_time
        self.energy_type = energy_type

        start_year = start_time.year
        end_year = end_time.year
        year_difference = end_year - start_year

        years = []
        for y in range(year_difference + 1):
            years.append(start_year + y)

        bas_df = retrievePropertiesConsumptionByYear(property_ids, years)

        replaceTime(bas_df)

        if energy_type:
            if energy_type == "Heat" or energy_type == "heat":
                bas_df = bas_df[bas_df["consumption_measure"] == 'Heat']
            if energy_type == "Electricity" or energy_type == "electricity":
                bas_df = bas_df[bas_df["consumption_measure"] == 'Electricity']
            else:
                print("You type an invalid consumption measure type.")
                #TODO error exception

        self.df = selectTimeObservation(bas_df, start_time, end_time)

    def getMeanEnergy(self):
        heat_df = self.df[self.df["consumption_measure"] == 'Heat']
        elec_df = self.df[self.df["consumption_measure"] == 'Electricity']

        heat_mean = heat_df["consumption"].mean()
        elec_mean = elec_df["consumption"].mean()

        return heat_mean, elec_mean




def retrievePropertiesConsumptionByYear(ids, years):
    """
    Return a dataframe containing the energy consumption of properties listed by their ids during certain years
    """

    def my_query(args):
        """
        Format a query using args: (id, year).
        """
        query = (hourly_url
                 + "?property_id=eq."
                 + str(args[0])
                 + "&year=eq."
                 + str(args[1])
                 )
        return query

    q_args = product(ids, years)
    # form a query per each id+year combination:
    queries = [my_query(p) for p in q_args]
    dfs = [pd.read_json(q) for q in queries]  # fetch data for each query

    return pd.concat(dfs)


def replaceTime(df):
    """
    replace the four columns of time (year, month, day and hour) by only one normalized column using datetime library
    """

    # Saving times
    timeDf = df[["year", "month", "day", "starting_hour"]].values.tolist()

    # COnverting to datetime type
    new_time_list = [datetime(time[0], time[1], time[2], time[3]) for time in timeDf]

    # Deleting obsolete columns
    df.drop("year", axis=1, inplace=True)
    df.drop("month", axis=1, inplace=True)
    df.drop("day", axis=1, inplace=True)
    df.drop("starting_hour", axis=1, inplace=True)

    # Putting the new normalized column to the df
    df["datetime"] = new_time_list
    df.sort_values(by="datetime")


def selectTimeObservation(df, start_time, end_time):
    """
    Returns the dataframe df during a more precise time interval [start_time, end_time],
    with the hour, the day, the month and the year.
    """
    return df.loc[(df['datetime'] >= start_time) & (df['datetime'] < end_time)]


# Test
start_date = datetime(2019, 1, 1, 0)
end_date = datetime(2019, 1, 2, 0)
ids = [657701]

retro = Retrospective(ids, start_date, end_date)

retro.df.info()
print(retro.df.head())
