import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
from itertools import chain
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import sys
from openpyxl.workbook.child import INVALID_TITLE_REGEX
import datetime
from os.path import exists
import openpyxl
import xlsxwriter as xs
import networkx as nx
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
from requests.exceptions import SSLError
from requests.exceptions import ConnectionError
from datetime import datetime, date, timedelta
import os
import glob


#########################################""


def applanir(liste,integer=1):
	i=0
	while i<integer:
		liste=list(chain.from_iterable(liste))
		i=i+1
	return liste

def check_purge (string):
	if "..." in string or "." in string: 
		return False
	return True

def check_TOS (string):
	if "Privacy policy" in string or "Terms of use" in string or "Contact us" in string: 
		return False
	return True

def number_page(liste):
	data=[]
	for i in range(len(liste)):
		liste[i]=list(filter(check_purge,liste[i]))
		data.append(liste[i])
	data=list(filter(None,data))

	for i in range(len(data)):
		data[i]=int("".join(data[i]))
	return max(data)



def parser(url,header,string="",classe="",parser="html.parser"):
	page=r.get(url,headers=header)
	parser=bs(page.content,parser)
	parser.encoding = parser.apparent_encoding
	if string=="" :
		return parser
	else:
		if classe=="":
			sous_section=parser.find_all(str(string))
		else:
			sous_section=parser.find_all(str(string),{"class": classe})
		return sous_section

def parser_all_pages(n,url,header,string="",classe="",pars="html.parser"):
	data=[]
	for i in range(n-1):
		u=url+str(n-i)
		print(u)
		donnée=parser(u,header,string,classe,pars)
		data.append(donnée)
	data=applanir(data)
	return data


def get_specific_data(categorie):

	etat_type=[]
	donnée=[]

	for k in range(1,len(categorie)):
		if not "\n" in categorie[k]:
				etat=categorie[k].get_text()
				etat_all=etat.split("=")
				etat_type.append(etat_all)
	donnée.append(etat_type)

	donnée=applanir(donnée,2)

	return donnée

def texte(parser):
	for i in range(len(parser)):
		parser[i]=parser[i].get_text()
	return parser

def localisation(liste):
	loc_list=[]
	for i in range(len(liste)):
		if "region" in liste[i] or "district" in liste[i] :   #or "Balakliya" in liste[i]
			loc_list.append(liste[i])
	return loc_list

def date(liste):
	date_list=[]
	for i in range(len(liste)):
		if any(s.isdigit() for s in liste[i]) and not any("-" in s for s in liste[i]) : 
			date_list.append(liste[i])
	return date_list

def localisation_and_date(liste):
	loc_list=[]
	date_list=[]
	data=[]

	for i in range(len(liste)):
		if any(s.isdigit() for s in liste[i]) and any(s.isdigit() for s in liste[i-1]) :
			loc_list.append("")		
		if any(s.isdigit() for s in liste[i]) and not any(s.isdigit() for s in liste[i-1]):
			date_list.append(liste[i])
			loc_list.append(liste[i-1])
	data.append(loc_list)
	data.append(date_list)
	return data

def words_counter(liste):
	string=",".join(liste)
	counts = dict()
	words = string.split(",")
	for word in words:
		if word in counts:
			counts[word] += 1
		else:
			counts[word] = 1

	return counts

def graph_split(dataframe,n,name):

	fig, ax = plt.subplots(1, n,figsize=(25, 25))
	plt.xticks(fontsize=10)

	for i in range(n):
		df=np.array_split(occurence_location, n)
		df[i].plot(y=0, kind="bar", ax=ax[i])
	plt.savefig(name+".png")
	os.startfile(name+".png")
	plt.show()



#########################################

#Parser
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}

url_page1="https://ukr.warspotting.net/search/?belligerent=2&page=1"
nombre_pages=parser(url_page1,header,"a","page-link")
nombre_pages=get_specific_data(nombre_pages)
nombre_pages=number_page(nombre_pages)
print(nombre_pages)
'''
url_russie="https://ukr.warspotting.net/search/?belligerent=2&page=321"
test=parser(url_russie,header,"a","link-secondary")
print(test)
'''
url_russie="https://ukr.warspotting.net/search/?belligerent=2&page="
#date_and_location=parser_all_pages(nombre_pages,url_russie,header,"a","link-secondary")

for i in range(5):
	try:
		date_and_location=parser_all_pages(nombre_pages,url_russie,header,"a","link-secondary")
	except (SSLError,ConnectionError) :
		if i < tries - 1: # i is zero indexed
			time.sleep(2)
			continue
		else:
			raise
	break

date_and_location=texte(date_and_location)
#print(date_and_location)
date_location=localisation_and_date(date_and_location)

loc=localisation(date_and_location)
date=date(date_and_location)
#print(date_and_location)
print(date)
#print(loc)

date_df=pd.DataFrame(date)
loc_df=pd.DataFrame(loc)



occurence_location=words_counter(loc)
occurence_location=pd.DataFrame.from_dict(occurence_location,orient='index')
occurence_location.columns = ["nombre_d'occurence"]
print(occurence_location)

occurence_date=words_counter(date)
occurence_date=pd.DataFrame.from_dict(occurence_date,orient='index')
occurence_date.columns = ["nombre_d'occurence"]
print(occurence_date)

####

current_directory = os.getcwd()

folder="warspotting"
directory_warspotting = os.path.join(current_directory, folder)

if not os.path.exists(directory_warspotting):
	os.makedirs(directory_warspotting)

###




occurence_date.plot( y="nombre_d'occurence", kind="bar")
plt.xticks(fontsize=5)
plt.xticks(rotation=45)

file_image=directory_warspotting+'\\nombre_occurence_date.png'
file_image=file_image.replace("\\", "\\\\")

plt.savefig(file_image)
os.startfile(file_image)

occurence_location.plot( y="nombre_d'occurence", kind="bar")
plt.xticks(fontsize=5)
plt.xticks(rotation=45)

file_image=directory_warspotting+'\\nombre_occurence_location.png'
file_image=file_image.replace("\\", "\\\\")

plt.savefig(file_image)
os.startfile(file_image)



#plt.show()

#plt.hist(occurence_date["nombre_d'occurence"])

#plt.show()



'''
n=40
df=np.array_split(occurence_location, n)

graph_split(occurence_date,n,"nombre_occurence_date",)
graph_split(occurence_location,n,"nombre_occurence_location")
'''



file_excel=directory_warspotting+'\\scrapper_WarSpotting.xlsx'

file_excel=file_excel.replace("\\", "\\\\")


if sys.platform == "win32":

	with pd.ExcelWriter(file_excel,engine="openpyxl",mode="w") as writer:
		occurence_location.to_excel(writer, sheet_name='location ')
		occurence_date.to_excel(writer, sheet_name='date ')

	os.system('"'+file_excel+ '"')