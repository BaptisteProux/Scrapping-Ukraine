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


#########################################

def barplot(datadf,groupBy,columnx,columnny,titregraph,titrex,titrey):
    data = []

    for aid_type, aid_df in datadf.groupby(groupBy):
        trace = go.Bar(x=aid_df[columnx], y=aid_df[columnny], name=aid_type)
        data.append(trace)

    layout = go.Layout(title=titregraph, xaxis={"title":titrex}, yaxis={"title":titrey})

    fig = go.Figure(data=data, layout=layout)

    fig.show()

def pieplot(datadf,value,name,titre,hover):
    fig = px.pie(datadf, values=value, names=name, title=titre, hover_data=[hover])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', width=800, height=600)
    fig.show()


#########################################

pd.set_option('display.max_columns', None)

url="https://www.ifw-kiel.de/publications/data-sets/ukraine-support-tracker-data-17410/"
current_directory = os.getcwd()
extension="xlsx"

folder="excel_supportTracker"
directory_excel = os.path.join(current_directory, folder)

if not os.path.exists(directory_excel):
	os.makedirs(directory_excel)


#for file in glob.glob(os.path.join(directory_json, "*.json")):
    #os.remove(file)
 


chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : directory_excel}
chrome_options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get(url)


time.sleep(4)


pop_up = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/main/article/section/div/div[2]/div[1]/p[4]/a")  
time.sleep(1)

    
tries = 10
for i in range(tries):
    try:
        pop_up.click()
    except  :
        if i < tries - 1: # i is zero indexed
            time.sleep(1)
            continue
        else:
            print("echec telechargement, travail sur fichier archive")
    break

time.sleep(3)


driver.close()

#print(directory)


files_excel = glob.glob(os.path.join(directory_excel, "*.xlsx"))  

excel_file = max(files_excel, key=os.path.getctime)

fichier=excel_file


df_excel_trackeur_bilateral_assistance=pd.read_excel(fichier,engine="openpyxl",sheet_name="Bilateral assistance, MAIN DATA")
df_excel_trackeur_multilateral_assistance=pd.read_excel(fichier,engine="openpyxl",sheet_name="Multilateral assistance")

#print(df_excel_trackeur_bilateral_assistance)
#print(df_excel_trackeur_multilateral_assistance)



df_excel_trackeur_bilateral_assistance['Converted Value in EUR'] = df_excel_trackeur_bilateral_assistance['Converted Value in EUR'].replace(".", "0")
df_excel_trackeur_bilateral_assistance['Converted Value in EUR'] = df_excel_trackeur_bilateral_assistance['Converted Value in EUR'].replace("", "0")
df_excel_trackeur_bilateral_assistance["Converted Value in EUR"] = df_excel_trackeur_bilateral_assistance["Converted Value in EUR"].apply(pd.to_numeric)
df_excel_trackeur_bilateral_assistance['Sub-type of item'] = df_excel_trackeur_bilateral_assistance['Sub-type of item'].replace(".", "")
df_excel_trackeur_bilateral_assistance['Sub-type of item'] = df_excel_trackeur_bilateral_assistance['Sub-type of item'].replace("Equipment and Assistance", "Equipment and assistance")

df_excel_trackeur_bilateral_assistance['No. of Units'] = df_excel_trackeur_bilateral_assistance['No. of Units'].replace(".", "0")
df_excel_trackeur_bilateral_assistance['No. of Units'] = df_excel_trackeur_bilateral_assistance['No. of Units'].replace("undisclosed", "0")
df_excel_trackeur_bilateral_assistance['No. of Units'] = df_excel_trackeur_bilateral_assistance['No. of Units'].replace("Undisclosed", "0")
df_excel_trackeur_bilateral_assistance["No. of Units"] = df_excel_trackeur_bilateral_assistance["No. of Units"].apply(pd.to_numeric)

df_excel_trackeur_bilateral_assistance['Type of Aid Specific'] = df_excel_trackeur_bilateral_assistance['Type of Aid Specific'].replace("Weapons and Equipment", "Weapons and equipment")
df_excel_trackeur_bilateral_assistance['Sub-type of item'] = df_excel_trackeur_bilateral_assistance['Sub-type of item'].replace("Main battle tank (MBT)", "Main Battle Tank (MBT)")


###
data_by_country_sum = df_excel_trackeur_bilateral_assistance.groupby('countries')["Converted Value in EUR"].sum()
data_by_country_sum=data_by_country_sum.to_frame().reset_index()
print(data_by_country_sum)

data_by_country_sum_type_help = df_excel_trackeur_bilateral_assistance.groupby(['countries',"Type of Aid General"])["Converted Value in EUR"].sum()
data_by_country_sum_type_help=data_by_country_sum_type_help.to_frame().reset_index()
print(data_by_country_sum_type_help)


data_by_help_type_specific = df_excel_trackeur_bilateral_assistance.groupby(['Type of Aid General',"Type of Aid Specific"])["Converted Value in EUR"].sum()
data_by_help_type_specific=data_by_help_type_specific.to_frame().reset_index()
print(data_by_help_type_specific)

data_by_military_sum = df_excel_trackeur_bilateral_assistance.groupby('Sub-type of item')["No. of Units"].sum()
data_by_military_sum=data_by_military_sum.to_frame().reset_index()
print(data_by_military_sum)


'''data_by_military_help = df_excel_trackeur_bilateral_assistance.groupby(['countries',"Sub-type of item"])["Converted Value in EUR"].sum()
data_by_military_help=data_by_military_help.to_frame().reset_index()
print(data_by_military_help)'''
###


######

pieplot(data_by_country_sum,"Converted Value in EUR",'countries','Valeur monétaires des aides par pays',"Converted Value in EUR")
barplot(data_by_country_sum_type_help,"Type of Aid General","countries","Converted Value in EUR","Aid by Country and Type of Aid","Country","Total Aid (EUR)")
barplot(data_by_help_type_specific,"Type of Aid Specific","Type of Aid General","Converted Value in EUR","Type of aid","Type of Aid General","Total Aid (EUR)")

fig = go.Figure(data=[go.Bar(
            x=data_by_military_sum["Sub-type of item"], 
            y=data_by_military_sum["No. of Units"]
    )])

fig.update_layout(title='No. of Units by Sub-type of item',
                  xaxis_title='Sub-type of item',
                  yaxis_title='No. of Units (log)')

fig.update_layout(yaxis_type="log")

fig.show()


###

#########################"""
df_excel_trackeur_multilateral_assistance['Converted Value in EUR'] = df_excel_trackeur_multilateral_assistance['Converted Value in EUR'].fillna("0")
df_excel_trackeur_multilateral_assistance['Converted Value in EUR'] = df_excel_trackeur_multilateral_assistance['Converted Value in EUR'].replace(" ", "0")
print(df_excel_trackeur_multilateral_assistance['Converted Value in EUR'])
df_excel_trackeur_multilateral_assistance["Converted Value in EUR"] = df_excel_trackeur_multilateral_assistance["Converted Value in EUR"].apply(pd.to_numeric)


data_by_donor_sum = df_excel_trackeur_multilateral_assistance.groupby('Donor')["Converted Value in EUR"].sum()
data_by_donor_sum=data_by_donor_sum.to_frame().reset_index()
print(data_by_donor_sum)

data_type_aid = df_excel_trackeur_multilateral_assistance.groupby(['Type of Aid General',"Type of Aid Specific"])["Converted Value in EUR"].sum()
data_type_aid=data_type_aid.to_frame().reset_index()
print(data_type_aid)

pieplot(data_by_donor_sum,"Converted Value in EUR",'Donor','Valeur monétaires des aides par doneurs',"Converted Value in EUR")
barplot(data_type_aid,"Type of Aid Specific","Type of Aid General","Converted Value in EUR","Type of aid","Type of Aid General","Total Aid (EUR)")