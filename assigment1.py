# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 00:50:49 2023

@author: Nisarg
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




data = pd.read_csv("API_EN.ATM.CO2E.KT_DS2_en_csv_v2_5994970.csv",\
                   skiprows=[0,1,2,3])

years_cols = np.arange(1990,2021).astype(str)
all_cols =  ["Country Name"] + list(years_cols)

#print(data[years_cols])

countries = np.array(["China","United States","India","Russian Federation",\
                      "Germany","Brazil"])

df_selected = data.loc[data["Country Name"].isin(countries),all_cols]
#Transpose
df_t = pd.DataFrame.transpose(df_selected)
df_t.columns = df_t.iloc[0]

df_t = df_t[1:]

plt.figure()

#df_t["Date"] = pd.to_numeric(df_t["Country Name"])
#plt.step(200,2020)

plt.plot(df_t.index, df_t["China"], label="China")
plt.plot(df_t.index, df_t["United States"], label="United States")
plt.plot(df_t.index, df_t["India"], label="India")
plt.plot(df_t.index, df_t["Russian Federation"], label="Russian Federation")
plt.plot(df_t.index, df_t["Germany"], label="Germany")
plt.plot(df_t.index, df_t["Brazil"], label="Brazil")

plt.title("CO2 emmition")
plt.xlabel("Years")
plt.ylabel("CO2(KT)")
plt.xticks(rotation=90, size=8)

plt.legend()
plt.show()