import pandas as pd 
import geopandas as gpd
import json
import plotly.express as px
import plotly.graph_objects as go
import contextily as cx
import folium
from folium.plugins import HeatMap
from folium.plugins import TimestampedGeoJson
from plotly.subplots import make_subplots

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import glob
import webbrowser
import plotly.graph_objects as go
import numpy as np
from datetime import date


#https://www.consilium.europa.eu/en/infographics/impact-sanctions-russian-economy/

#########################################
today = date.today()
current_directory = os.getcwd()
folder="military_unit"
directory_mil = os.path.join(current_directory, folder)

if not os.path.exists(directory_mil):
    os.makedirs(directory_mil)

pd.set_option('display.max_columns', None)


url_btg_all = "https://raw.githubusercontent.com/simonhuwiler/uawardata/master/data/csv/btgs_all.csv"
btg_all_df = pd.read_csv(url_btg_all)
print(btg_all_df)

url_units_all = "https://raw.githubusercontent.com/simonhuwiler/uawardata/master/data/csv/units_all.csv"
units_all_df = pd.read_csv(url_units_all)
print(units_all_df)


url_btg_current = "https://raw.githubusercontent.com/simonhuwiler/uawardata/master/data/csv/btgs_current.csv"
btg_current_df = pd.read_csv(url_btg_current)
print(btg_current_df)


url_units_current = "https://raw.githubusercontent.com/simonhuwiler/uawardata/master/data/csv/units_current.csv"
units_current_df = pd.read_csv(url_units_current)
print(units_current_df)

#####
m = folium.Map(location=[btg_all_df['lat'].mean(), btg_all_df['lng'].mean()], zoom_start=7)


color_dict = {'vdv': 'green', 'motor_rifle': 'blue', 'tank': 'red'}

for i, row in btg_all_df.iterrows():
    color = color_dict[row['type_of_btg']]
    folium.Marker(location=[row['lat'], row['lng']], 
                  popup=row['unit']+" "+row['type_of_btg']+" "+row['date'], 
                  icon=folium.Icon(color=color, icon='info-sign')).add_to(m)

name_map="/map_military_BTG_all.html"
m.save(directory_mil+name_map)
webbrowser.open(directory_mil+name_map)


m = folium.Map(location=[btg_current_df['lat'].mean(), btg_current_df['lng'].mean()], zoom_start=7)



for i, row in btg_current_df.iterrows():
    color = color_dict[row['type_of_btg']]
    folium.Marker(location=[row['lat'], row['lng']], 
                  popup=row['unit']+" "+row['type_of_btg'], 
                  icon=folium.Icon(color=color, icon='info-sign')).add_to(m)

name_map="/map_military_BTG_2022-06-13.html" #en attente modification dans github pour rajouter la date 
m.save(directory_mil+name_map)
webbrowser.open(directory_mil+name_map)
#####


m = folium.Map(location=[units_all_df['lat'].mean(), units_all_df['lng'].mean()], zoom_start=7)


color_dict = {'ru': 'red', 'ua': 'blue'}

for i, row in units_all_df.iterrows():
    color = color_dict[row['country']]
    folium.Marker(location=[row['lat'], row['lng']], 
                  popup=row['unit']+" "+row['strength']+" "+row['date'], 
                  icon=folium.Icon(color=color, icon='info-sign')).add_to(m)

name_map="/map_military_unit_all.html"
m.save(directory_mil+name_map)
webbrowser.open(directory_mil+name_map)


m = folium.Map(location=[units_current_df['lat'].mean(), units_current_df['lng'].mean()], zoom_start=7)



for i, row in units_current_df.iterrows():
    color = color_dict[row['country']]
    folium.Marker(location=[row['lat'], row['lng']], 
                  popup=row['unit']+" "+row['strength'], 
                  icon=folium.Icon(color=color, icon='info-sign')).add_to(m)

name_map="/map_military_units_2022-06-13.html" #en attente modification dans github pour rajouter la date
m.save(directory_mil+name_map)
webbrowser.open(directory_mil+name_map)
