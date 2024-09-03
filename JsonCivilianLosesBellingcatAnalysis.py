import pandas as pd 
import geopandas as gpd
import json
import plotly.express as px
import plotly.graph_objects as go
import contextily as cx
import folium
from folium.plugins import HeatMap
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import glob
import openpyxl
import webbrowser


#########################################
#source: https://pancheliuga.com/blog/spatial-data-analysis-of-civilian-harm-in-ukraine/
#########################################

url="https://ukraine.bellingcat.com/"
current_directory = os.getcwd()
extension="json"

folder="json_civilian"
directory_json = os.path.join(current_directory, folder)

if not os.path.exists(directory_json):
	os.makedirs(directory_json)


#for file in glob.glob(os.path.join(directory_json, "*.json")):
    #os.remove(file)
 


chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : directory_json}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)

#ps: de temps en temps les xpath changent 
time.sleep(2.5)

pop_up = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/div[6]/div[2]/div[1]/button")  
pop_up.click()


time.sleep(2.5)

first_button = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/div[1]/div/div[1]/div[2]/ul/div[2]/i")
first_button.click()

time.sleep(2.5)


second_button = driver.find_element(By.XPATH,"/html/body/div/div[1]/div/div[1]/div/div[2]/div[3]/div/div[4]/span[1]/i")
second_button.click()

time.sleep(2)

driver.close()

#print(directory)


files_json = glob.glob(os.path.join(directory_json, "*.json"))  

json_file = max(files_json, key=os.path.getctime)

fichier=json_file


pd.set_option('display.max_columns', None)

with open(fichier, 'r',encoding='utf-8') as file:
     data = json.loads(file.read())

data = pd.json_normalize(data, record_path='filters', meta=['id', 'date', 'latitude', 'longitude', 'location', 'description'])

data[["latitude", "longitude"]] = data[["latitude", "longitude"]].apply(pd.to_numeric)

print(data)

data_by_type = data.groupby('value').size()
data_by_type = data_by_type.to_frame(name="nombre d'incidents").reset_index()
data_by_type=data_by_type.sort_values(by="nombre d'incidents", ascending=False)

print(data_by_type)

data_by_day = data.groupby('date').size().to_frame(name="nombre d'incidents").reset_index()


######
fig = px.pie(data_by_type, values="nombre d'incidents", names='value', title='Civilian harm by type of affected area', 
             hover_data=["nombre d'incidents"])

fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', width=800, height=600)

fig.show()


fig = px.line(data_by_day, x='date', y="nombre d'incidents", title='Number of incidents per day')

fig.show()
######


#############

url="https://data.humdata.org/dataset/cod-ab-ukr?force_layout=desktop"

folder="adm_ukraine"
directory_adm = os.path.join(current_directory, folder)



fichier_adm=directory_adm+"/ukr_admbnda_adm1_sspe_20221005.shp"





geo_data = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['longitude'], data['latitude']), crs="EPSG:4326")
geo_data.to_crs(epsg=3857, inplace=True)
geo=geo_data.plot(figsize=(20,10))
cx.add_basemap(geo)
name_file_map=directory_adm+'\\Graph_civilian_incident.png'
plt.savefig(name_file_map)
os.startfile(name_file_map)


regions = gpd.read_file(fichier_adm)
regions.to_crs(epsg=3857, inplace=True)
#ax = regions.plot(figsize=(20,10))
#cx.add_basemap(ax)
#plt.show()



combined_geo_incidents_df = gpd.sjoin(geo_data, regions[['ADM1_EN', 'geometry']], predicate='within').drop(columns=['index_right'])


m = folium.Map(location=[49.107892273527504, 31.444630060047018], tiles = 'stamentoner', zoom_start=6, control_scale=True)
heat_data = list(zip(combined_geo_incidents_df["latitude"], combined_geo_incidents_df["longitude"]))
HeatMap(heat_data).add_to(m)
name_map="/Heat_map_incident_civil_ukraine.html"
m.save(directory_adm+name_map)
webbrowser.open(directory_adm+name_map)


#######

incidents_by_region = combined_geo_incidents_df.groupby('ADM1_EN').size().to_frame(name="nombre d'incidents").reset_index()


fig = px.pie(incidents_by_region, values="nombre d'incidents", names='ADM1_EN', title='Civilian harm by region', 
             hover_data=["nombre d'incidents"], labels={"nombre d'incidents":"nombre d'incidents", 'ADM1_EN': 'Region'})

fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', width=800, height=600)

fig.show()


############
regions_incidents = pd.merge(regions[['ADM1_EN', 'geometry']], incidents_by_region, how='left', on='ADM1_EN')
regions_incidents["nombre d'incidents"] = regions_incidents["nombre d'incidents"].fillna(0)

regions_incidents['geoid'] = regions_incidents.index.astype(str)

m = folium.Map(location=[49.107892273527504, 31.444630060047018], tiles='cartodbpositron', zoom_start=6, control_scale=True)

folium.Choropleth(geo_data=regions_incidents, 
                  data=regions_incidents,
                  name='Choropleth Map',
                  columns=['geoid',"nombre d'incidents"], 
                  key_on='feature.id',
                  bins=8,
                  fill_color='YlOrRd', 
                  line_color='white',
                  line_weight=0,
                  legend_name='Number of incidents').add_to(m)

folium.features.GeoJson(regions_incidents, name='Labels',
               style_function=lambda x: {'color':'transparent','fillColor':'transparent','weight':0},
                tooltip=folium.features.GeoJsonTooltip(fields=['ADM1_EN', "nombre d'incidents"],
                                              aliases = ['Region', 'Number of incidents'],
                                              labels=True,
                                              sticky=True)).add_to(m)

folium.LayerControl().add_to(m)

name_map="/Number_of_incident_per_region.html"
m.save(directory_adm+name_map)
webbrowser.open(directory_adm+name_map)
