# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 00:50:49 2023

@author: Nisarg
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def read_and_prepare_world_co2_data(countrie_list, start_from_yeart,
                                    end_to_year):
    """
    This function reads csv and processes and prepare the co2 emission data

    Parameters
    ----------
    countrie_list : list
        select countries from dataset.
    start_from_yeart : int
         starting from year.
    end_to_year : int
        end to year .

    Returns
    -------
    pandas dataframe
        return new filtered data.

    """

    # read csv using pandas
    co2_df = pd.read_csv("API_EN.ATM.CO2E.KT_DS2_en_csv_v2_5994970.csv",
                         skiprows=3, iterator=False)

    years_column_list = np.arange(
        start_from_yeart, (end_to_year+1)).astype(str)
    all_cols_list = ["Country Name"] + list(years_column_list)

    # Filter data: select only specific countries and years
    df_selected = co2_df.loc[co2_df["Country Name"].isin(countrie_list),
                             all_cols_list]

    # Transpose
    df_t = pd.DataFrame.transpose(df_selected)
    df_t.columns = df_t.iloc[0]

    # remove first row
    df_t = df_t[1:]
    df_t.index = df_t.index.astype(int)

    # scale data from kiloton to megaton
    for contry in countrie_list:
        df_t[contry + " megaton"] = df_t[contry]/1000

    return df_t


def read_and_prepare_ev_data(region, start_from_yeart, end_to_year):
    """
    This function reads csv and processes and prepare the ev sale data

    Parameters
    ----------
    region : string
        Country name or type world to get global sales data.
    start_from_yeart : int
         starting from year.
    end_to_year : int
        end to year .

    Returns
    -------
    pandas dataframe
        return new filtered data.

    """

    # read csv using pandas
    ev_df = pd.read_csv(
        "IEA-EV-dataEV salesHistoricalCars.csv", iterator=False)

    # filter data and select only required column
    df_selected = ev_df.loc[(ev_df["region"] == region)
                            & (ev_df["category"] == "Historical")
                            & (ev_df["parameter"] == "EV sales")
                            & (ev_df["mode"] == "Cars")
                            & (ev_df["powertrain"].isin(["PHEV", "BEV"]))
                            & (ev_df["unit"] == "Vehicles")
                            & (ev_df["year"] >= start_from_yeart)
                            & (ev_df["year"] <= end_to_year),
                            ["powertrain", "year", "value"]]

    # scale the number of ev sales into millions
    df_selected["value_million"] = df_selected["value"]/1000000

    return df_selected


def create_and_save_line_graph(data, countrie_list):
    """
    This function takes data as an argument and creates a line chart for \
    co2 emission using matplotlib and save png image on disk

    Parameters
    ----------
    data : pandas dataframe
        data for create line chart.
    countrie_list : list
        list of contries to show on graph.

    Returns
    -------
    None.

    """

    # start creating line chart
    plt.figure(figsize=(10, 6))
    for contry in countrie_list:
        plt.plot(data.index, data[contry+" megaton"], label=contry)

    # set label and legend
    plt.title("CO2 emission")
    plt.xlabel("Years")
    plt.ylabel("Megatons")
    plt.xticks(np.arange(min(data.index), max(data.index)+1, 5.0))
    plt.xlim(min(data.index), max(data.index))
    plt.legend()

    # save the graph in disk
    plt.savefig("fig1.png")


def create_and_save_pi_chart(data, countrie_list, year1, year2):
    """
    This function takes data as an argument and creates two pi charts for \
        co2 emission using matplotlib and save png image on disk

    Parameters
    ----------
    data : pandas dataframe
        data for create line chart.
    countrie_list : list
        list of contries to show on graph.
    year1 : int
        select year for left pie chart.
    year2 : int
        select year for right pie chart.

    Returns
    -------
    None.

    """

    # start creating a line chart
    plt.figure(figsize=(10, 6))

    # use a subplot to show two graphs in a single graph
    # create pie chart one
    plt.subplot(1, 2, 1)
    plt.pie(data.loc[data.index == year1, countrie_list].values.flatten()
            .tolist(),
            labels=countrie_list, autopct='%1.0f%%', pctdistance=1.1,
            labeldistance=1.25, textprops={'fontsize': 10}, radius=0.9)
    plt.title(year1)

    # create pie chart two
    plt.subplot(1, 2, 2)
    plt.pie(data.loc[data.index == year2, countrie_list].values.flatten()
            .tolist(),
            labels=countrie_list, autopct='%1.0f%%', pctdistance=1.1,
            labeldistance=1.25, textprops={'fontsize': 10}, radius=0.9)
    plt.title(year2)
    plt.suptitle(' CO2 emission ', fontsize=15)

    # save the graph on disk
    plt.savefig("fig2.png")


def creat_and_save_bar_chart(data):
    """
    This function takes data as an argument and creates a bar chart for \
        ev sale using matplotlib and save png image on disk

    Parameters
    ----------
    data : pandas dataframe
        data for create bar chart.

    Returns
    -------
    None.

    """

    # get unique years for the x-axis
    years = data["year"].unique()
    # prepare y-axis data
    phev_data = data.loc[data["powertrain"] == "PHEV"]
    bev_data = data.loc[data["powertrain"] == "BEV"]

    # start creating a line chart
    plt.figure(figsize=(10, 6))
    plt.bar(years, phev_data["value_million"],
            label="PHEV(plug-in hybrid electric vehicles)")
    plt.bar(years, bev_data["value_million"],
            bottom=phev_data["value_million"],
            label="BEV(battery electric vehicles)")

    # set label and legend
    plt.title("EV sales, World")
    plt.xlabel("Years")
    plt.ylabel("Vehicles(million)")
    plt.legend()

    # save the graph on disk
    plt.savefig("fig3.png")


##################### Main Program ##########################


countries = ["China", "United States", "India", "Russian Federation",
             "Germany", "Brazil"]
# get co2 emission data
co2_data = read_and_prepare_world_co2_data(countries, 1990, 2020)
# create a line graph from co2 emission data
create_and_save_line_graph(co2_data, countries)
# create pie chart to represent  co2 emission in years 1990 and 2020
create_and_save_pi_chart(co2_data, countries, 1990, 2020)

# get ev car sale data
ev_data = read_and_prepare_ev_data("World", 2010, 2022)
# create a bar chart to represent the ev data
creat_and_save_bar_chart(ev_data)

# Display graph
plt.show()
