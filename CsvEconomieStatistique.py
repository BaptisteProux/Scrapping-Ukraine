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


#https://www.consilium.europa.eu/en/infographics/impact-sanctions-russian-economy/

#########################################

pd.set_option('display.max_columns', None)


current_directory = os.getcwd()


folder="economie_statistique"
directory_economie = os.path.join(current_directory, folder)
directory_gdp_evolution=directory_economie+"/Russia_GDP_Evolution.csv"
directory_inflation_evolution=directory_economie+"/Russia_inflation_evolution.csv"

file_GDP_Evolution=pd.read_csv(directory_gdp_evolution)
file_Inflation_Evolution=pd.read_csv(directory_inflation_evolution)

print(file_GDP_Evolution)
print(file_Inflation_Evolution)

file_GDP_Evolution[['World Bank', 'IMF', 'OECD']] = file_GDP_Evolution[['World Bank', 'IMF', 'OECD']].sub(100)

fig = go.Figure()
fig.add_trace(go.Scatter(x=file_GDP_Evolution['when'], y=file_GDP_Evolution['World Bank'], name="World Bank"))
fig.add_trace(go.Scatter(x=file_GDP_Evolution['when'], y=file_GDP_Evolution['IMF'], name="IMF"))
fig.add_trace(go.Scatter(x=file_GDP_Evolution['when'], y=file_GDP_Evolution['OECD'], name="OECD"))
fig.update_layout(title='World Bank, IMF, OECD',xaxis_title='Year',yaxis_title='GDP evolution %')
fig.show()

fig = go.Figure()
fig.add_trace(go.Scatter(x=file_Inflation_Evolution['Date'], y=file_Inflation_Evolution['World Bank'], name="World Bank"))
fig.add_trace(go.Scatter(x=file_Inflation_Evolution['Date'], y=file_Inflation_Evolution['IMF'], name="IMF"))
fig.add_trace(go.Scatter(x=file_Inflation_Evolution['Date'], y=file_Inflation_Evolution['OECD'], name="OECD"))
fig.update_layout(title='World Bank, IMF, OECD',xaxis_title='Year',yaxis_title='Inflation evolution')
fig.show()


