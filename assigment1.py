# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 00:50:49 2023

@author: Nisarg
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



def read_and_prepare_world_co2_data():
    """ this function reads csv and processes the data and return new \
        filtered dataframe """
    
    #read csv using pandas
    data = pd.read_csv("API_EN.ATM.CO2E.KT_DS2_en_csv_v2_5994970.csv", \
                   skiprows=[0, 1, 2, 3])

    years_column_list  = np.arange(1990, 2021).astype(str)
    all_cols_list = ["Country Name"] + list(years_column_list)

    countries = ["China", "United States", "India", "Russian Federation", \
             "Germany", "Brazil"]

    #Filter data: select only specific countries and years
    df_selected = data.loc[data["Country Name"].isin(countries), \
                           all_cols_list]
   
    # Transpose
    df_t = pd.DataFrame.transpose(df_selected)
    df_t.columns = df_t.iloc[0]

    #remove first row
    df_t = df_t[1:]
    df_t.index = df_t.index.astype(int)

    # convert data from kiloton to megaton
    df_t["China megaton"] = df_t["China"]/1000
    df_t["United States megaton"] = df_t["United States"]/1000
    df_t["India megaton"] = df_t["India"]/1000
    df_t["Russian Federation megaton"] = df_t["Russian Federation"]/1000
    df_t["Germany megaton"] = df_t["Germany"]/1000
    df_t["Brazil megaton"] = df_t["Brazil"]/1000
    
    return df_t

def create_and_save_line_graph(data):
    """ create line chart and save as image on disk """
    
    #start creating line chart
    plt.figure()
    plt.plot(data.index, data["China megaton"], label="China")
    plt.plot(data.index, data["United States megaton"], label="United States")
    plt.plot(data.index, data["India megaton"], label="India")
    plt.plot(data.index, data["Russian Federation megaton"],
                                                 label="Russian Federation")
    plt.plot(data.index, data["Germany megaton"], label="Germany")
    plt.plot(data.index, data["Brazil megaton"], label="Brazil")

    #set label and legend
    plt.title("CO2 emmition")
    plt.xlabel("Years")
    plt.ylabel("Megatons")
    plt.xticks(np.arange(min(data.index), max(data.index)+1, 5.0))
    plt.xlim(min(data.index), max(data.index))
    plt.legend()
    
    #save the graph in disk
    plt.savefig("fig1.png")

def create_and_save_pi_chart(data):
    
    countries = ["China", "United States", "India", "Russian Federation", \
                 "Germany", "Brazil"]
    #start creating line chart
    plt.figure()

    #use subplot to show two graph in single graph
    plt.subplot(1, 2, 1)
    plt.pie((data.loc[data.index==1990, countries].values[0]), labels=countries)
    plt.title("1990")

    plt.subplot(1, 2, 2)
    plt.pie(data.loc[data.index==2020, countries].values[0], labels=countries)
    plt.title("2020")
    
    #save the graph in disk
    plt.savefig("fig2.png")
    

#Main Program
data = read_and_prepare_world_co2_data();
create_and_save_line_graph(data)
create_and_save_pi_chart(data)




#Display graph
plt.show()
