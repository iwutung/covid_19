import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# load mobility data sets
df_2020 = pd.read_csv(
    'https://github.com/iwutung/covid_19/blob/master/datasets/2020_UG_Region_Mobility_Report.csv')
df_2021 = pd.read_csv(
    'https://github.com/iwutung/covid_19/blob/master/datasets/2021_UG_Region_Mobility_Report.csv')
df_2022 = pd.read_csv(
    'https://github.com/iwutung/covid_19/blob/master/datasets/2022_UG_Region_Mobility_Report.csv')

# join the data sets
mob_df_ug = pd.concat([df_2020, df_2021, df_2022])

# drop unnecessary columns
df_ug = mob_df_ug[
    ['country_region', 'date',
     'retail_and_recreation_percent_change_from_baseline',
     'grocery_and_pharmacy_percent_change_from_baseline',
     'parks_percent_change_from_baseline',
     'transit_stations_percent_change_from_baseline',
     'workplaces_percent_change_from_baseline',
     'residential_percent_change_from_baseline'
     ]
]

# drop na values
df_ug_fill = df_ug.dropna()

# Compute cuntry average
df_ug_wide = df_ug_fill.groupby(['country_region', 'date']).mean().reset_index()

# rename columns appropriately
df_ug_wide.columns = [
    'country_region', 'date', 'retail_and_recreation',
    'grocery_and_pharmacy', 'parks', 'transit_stations',
    'workplaces', 'residential'
]

# convert date to datetime
df_ug_wide['date'] = pd.to_datetime(df_ug_wide['date'], format='%Y-%m-%d')

# convert dataset to long
df_ug_long = pd.melt(
    df_ug_wide, id_vars=['country_region', 'date'],
    value_vars=[
        'retail_and_recreation', 'grocery_and_pharmacy', 'parks',
        'transit_stations', 'workplaces', 'residential'
    ]
)

print('Mobility datasets loaded')

# Load covid ataset
covid_data = pd.read_csv(
    'https://covid.ourworldindata.org/data/owid-covid-data.csv'
)

# Retain columns for analysis
covid_data_red = covid_data[
    ['iso_code', 'continent', 'location', 'date', 'total_cases', 'new_cases',
     'new_cases_smoothed', 'total_deaths', 'new_deaths',
     'new_deaths_smoothed', 'total_cases_per_million',
     'new_cases_per_million', 'new_cases_smoothed_per_million',
     'total_deaths_per_million', 'new_deaths_per_million',
     'new_deaths_smoothed_per_million', 'total_tests', 'new_tests',
     'total_tests_per_thousand', 'new_tests_per_thousand',
     'new_tests_smoothed', 'new_tests_smoothed_per_thousand',
     'positive_rate', 'tests_per_case', 'tests_units', 'total_vaccinations',
     'people_vaccinated', 'people_fully_vaccinated', 'total_boosters',
     'new_vaccinations', 'new_vaccinations_smoothed',
     'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred',
     'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred',
     'new_vaccinations_smoothed_per_million',
     'new_people_vaccinated_smoothed',
     'new_people_vaccinated_smoothed_per_hundred'
     ]
]

# Filter to Uganda data
covid_ug = covid_data_red[covid_data_red.location == 'Uganda']

# Convert date column to datetime
covid_ug['date'] = pd.to_datetime(covid_ug['date'], format='%Y-%m-%d')

# Convert dataset to long format
covid_data_long = pd.melt(
    covid_ug,
    id_vars=['iso_code', 'continent', 'location', 'date'],
    value_vars=[
        'total_cases', 'new_cases', 'new_cases_smoothed', 'total_deaths',
        'new_deaths', 'new_deaths_smoothed', 'total_cases_per_million',
        'new_cases_per_million', 'new_cases_smoothed_per_million',
        'total_deaths_per_million', 'new_deaths_per_million',
        'new_deaths_smoothed_per_million', 'total_tests', 'new_tests',
        'total_tests_per_thousand', 'new_tests_per_thousand',
        'new_tests_smoothed', 'new_tests_smoothed_per_thousand',
        'positive_rate', 'tests_per_case', 'tests_units',
        'total_vaccinations', 'people_vaccinated',
        'people_fully_vaccinated', 'total_boosters', 'new_vaccinations',
        'new_vaccinations_smoothed', 'total_vaccinations_per_hundred',
        'people_vaccinated_per_hundred',
        'people_fully_vaccinated_per_hundred', 'total_boosters_per_hundred',
        'new_vaccinations_smoothed_per_million',
        'new_people_vaccinated_smoothed',
        'new_people_vaccinated_smoothed_per_hundred'
    ]
)

print('Covid data loaded')


def load_mobility_data(category):
    """
    Filters data by place category if applicable.
    Args:
        (str) category - name of the category to analyze
    Returns:
        df_mob - Pandas DataFrame containing the data filtered by category
    """

    # Apply filter if necessary
    if category != 'all':
        df_mob = df_ug_long[
            df_ug_long['variable'] == category
        ].sort_values('date').reset_index()

    else:
        df_mob = df_ug_long.sort_values(['variable', 'date']).reset_index()

    # Return required data
    return df_mob


def load_covid_data(feature):
    """
    Loads data and filters for Uganda specifics.
    Input:
        (Str) feature - covid data to visualize
    Returns:
        df_covid - Pandas DataFrame covid data for Uganda
    """

    # Apply filter if necessary
    if feature != 'all':
        covid_df = covid_data_long[
            covid_data_long['variable'] == feature
        ].sort_values(['variable', 'date']).reset_index()

    else:
        covid_df = covid_data_long.sort_values(
            ['variable', 'date']
        ).reset_index()

    # Return desired data
    return covid_df
