import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px


def load_mobility_data(category):
    """
    Loads data and filters by place category if applicable.
    Args:
        (str) category - name of the category to analyze
    Returns:
        df - Pandas DataFrame containing the data filtered by category
    """
    # load data sets
    df_2020 = pd.read_csv(
        'https://github.com/iwutung/covid_19/blob/master/datasets/2020_UG_Region_Mobility_Report.csv')
    df_2021 = pd.read_csv(
        'https://github.com/iwutung/covid_19/blob/master/datasets/2021_UG_Region_Mobility_Report.csv')
    df_2022 = pd.read_csv(
        'https://github.com/iwutung/covid_19/blob/master/datasets/2022_UG_Region_Mobility_Report.csv')

    # join the data sets
    mob_df_ug = pd.concat([df_2020, df_2021, df_2022]).reset_index()

    # drop unnecessary columns
    df_ug = mob_df_ug[[
        'country_region', 'date',
        'retail_and_recreation_percent_change_from_baseline',
        'grocery_and_pharmacy_percent_change_from_baseline',
        'parks_percent_change_from_baseline',
        'transit_stations_percent_change_from_baseline',
        'workplaces_percent_change_from_baseline',
        'residential_percent_change_from_baseline'
    ]
    ]

    # replace na values with previous value
    df_ug_fill = df_ug.fillna(method='ffill')

    # rename columns appropriately
    df_ug_fill.columns = [
        'country_region', 'date', 'retail_and_recreation',
        'grocery_and_pharmacy', 'parks', 'transit_stations',
        'workplaces', 'residential'
    ]

    # convert date to datetime
    df_ug_fill['date'] = pd.to_datetime(df_ug_fill['date'], format='%Y-%m-%d')

    # convert dataset to long
    df_ug_long = pd.melt(
        df_ug_fill, id_vars=['country_region', 'date'],
        value_vars=[
            'retail_and_recreation', 'grocery_and_pharmacy', 'parks',
            'transit_stations', 'workplaces', 'residential'
        ]
    ).reset_index()

    # filter by category if applicabe
    if category != 'all':
        df_mob = df_ug_long[df_ug_long['variable'] == category]

    else:
        df_mob = df_ug_long

    return df_mob
