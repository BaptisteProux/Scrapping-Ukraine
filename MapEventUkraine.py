import pandas as pd 
import geopandas as gpd
import json
import plotly.express as px
import plotly.graph_objects as go
import contextily as cx
import folium
from folium.plugins import HeatMap
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
import kml2geojson
import zipfile


#https://geoconfirmed.azurewebsites.net/


########################################

def convertKMZtoGeoJson(namefile):
    kmz = zipfile.ZipFile(directory_map+"/"+namefile+".kmz", 'r')
    kmz.extractall(folder)
    os.system('k2g '+folder+"/"+namefile+".kml "+folder+"/"+"map_json "+"--style-filename "+namefile+".json")
    #kml2geojson.main.convert(directory_map+"/"+namefile+".kml", "map_event_json") #ne marche pas

def GeoJsonDataFromKMZ(namefile):
    convertKMZtoGeoJson(namefile)

    with open(directory_map_json+"/"+namefile+".json") as f:
        geo_json_data = f.read()
    return geo_json_data

def style_function(feature):
    name = feature['properties']['name']
    color = 'black'
    for nc in names_colors:
        if nc[0] == name:
            color = nc[1]
    return {'fillColor': color, 'color': color, 'weight': 0.5, 'fillOpacity': 0.8}

def create_icon(styleUrl):
    icon_folder = "images/"
    icon_name = styleUrl.replace("#", "")
    icon_path = icon_folder + icon_name
    return folium.features.CustomIcon(icon_path)

#########################################
url="https://geoconfirmed.azurewebsites.net/"

today = date.today()
current_directory = os.getcwd()
folder="map_event"
folder_json="map_json"
directory_map = os.path.join(current_directory, folder)
directory_map_json=os.path.join(directory_map, folder_json)

if not os.path.exists(directory_map):
    os.makedirs(directory_map)

pd.set_option('display.max_columns', None)

chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : directory_map}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)


time.sleep(10)

pop_up = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/main/article/div/div[5]/button[1]")  
pop_up.click()

time.sleep(3)

driver.close()


files_zip = glob.glob(os.path.join(directory_map, "*.zip"))  

zip_file = max(files_zip, key=os.path.getctime)

fichier=zip_file


with zipfile.ZipFile(fichier, "r") as archive:
    archive.extractall("map_event")

#####



geo_json_Last_7_days=GeoJsonDataFromKMZ("C.-Last-7-days")
geo_json_frontline=GeoJsonDataFromKMZ("B.-Estimated-Frontline-by-@DavidBatashvili")

'''with open(directory_map_json+"/"+"C.-Last-7-days"+".json") as f:
    geo_json_Last_7_days = f.read()'''

m = folium.Map()

'''folium.GeoJson(geo_json_Last_7_days, 
                name='geojson',
                style_function=lambda x: {'fillColor':'red' if x['properties']['styleUrl'].startswith('#_CIRCLES_RU') else 'blue'},
                highlight_function=lambda x: {'weight':2, 'fillOpacity':1},
                tooltip=folium.features.GeoJsonTooltip(fields=['name','description'],
                                                        labels=True,
                                                        sticky=False),
                popup=lambda x: folium.Popup('Name: ' + x['properties']['name'] + '<br>'+ 'Description: ' + x['properties']['description'], max_width=250)
              ).add_to(m)'''

geo_json_Last_7_days = json.loads(geo_json_Last_7_days)

#folium.Marker(icon=create_icon(geo_json_Last_7_days['features'][1]['properties']['styleUrl']))

for feature in geo_json_Last_7_days['features']:
    try:
        icon = create_icon(feature['properties']['styleUrl'])
    except:
        icon=folium.Icon()

    folium.Marker([feature['geometry']['coordinates'][1],feature['geometry']['coordinates'][0]],
                  popup=feature['properties']['name'] + '<br>' + feature['properties']['description'],
                  icon=icon).add_to(m)

folium.GeoJson(geo_json_frontline,
                name='geojson2',
                style_function=lambda feature: {'fillColor': '#000000' if feature['properties']['name'] == '28 0000 JAN 2023 Front line' else '#00ff00'},
                tooltip=folium.features.GeoJsonTooltip(fields=['name'],
                                                       labels=True,
                                                       sticky=False),
                popup=lambda feature: folium.Popup('Name: ' + feature['properties']['name'], max_width=250)
              ).add_to(m)

#folium.GeoJson(geo_json_frontline).add_to(m)

m.fit_bounds(m.get_bounds())

name_map="/map_war_ukraine.html"

m.save(directory_map+name_map)
webbrowser.open(directory_map+name_map)

'''m = folium.Map(location=[btg_all_df['lat'].mean(), btg_all_df['lng'].mean()], zoom_start=7)


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
webbrowser.open(directory_mil+name_map)'''
