import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
import timezones
import os
import glob
import sys
import numpy
from openpyxl.workbook.child import INVALID_TITLE_REGEX
from os.path import exists
import openpyxl
import xlsxwriter as xs
import re
from threading import Thread
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
from PIL import Image
import requests as r
from io import BytesIO
from itertools import chain
import time
from requests.exceptions import SSLError
from requests.exceptions import ConnectionError
from datetime import datetime, date, timedelta
import nltk
from nltk.corpus import stopwords
import sumy
from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.reduction import ReductionSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import ssl
from docx import Document
from docx.shared import Inches
import text2emotion as te


#nltk.download()

##################################################################################


def applanir(liste,integer=1):
	i=0
	while i<integer:
		liste=list(chain.from_iterable(liste))
		i=i+1
	return liste


def csv_creator(dataframe,sheetname,index=""):
	
	if index!=False:
		dataframe.to_csv(sheetname+".csv")
	else:
		dataframe.to_csv(sheetname+".csv",index=False)

def convert_to_int(liste,integer=1):

	if integer==1:
		liste=[eval(i) if isinstance(i,str)==True else i for i in liste]

	else:
		j=0
		while j<integer:
			liste[j]=[eval(i) if isinstance(i,str)==True else i for i in liste[j]]
			j=j+1

	return liste

def scrapper_user(request,sheetname,number=3200,opencsv="non",image="",allimage=""):
	container=[]
	if image!="yes":
		for i,tweet in enumerate(sntwitter.TwitterSearchScraper(str(request)).get_items()):
			if i>number:
				break
			container.append([tweet.date,tweet.rawContent])
	if image=="yes":
		for i,tweet in enumerate(sntwitter.TwitterSearchScraper(str(request)).get_items()):
			if i>number:
				break
			if allimage=="":
				if tweet.media:
					j=len(tweet.media)-1
					#print(str(j)+" nombre d'image -1 " +str(i))  
					container.append([tweet.date,tweet.media[j].previewUrl])  #liste pas de même taille a la fin
				else:
					pass
			else:
				if tweet.media:
					for item in tweet.media:
						try:
							container.append([tweet.date,item.previewUrl])
						except:
							pass
				else:
					pass
			
				#container.append([tweet.date,tweet.media[0].previewUrl]) #en attendant car ici listes de même taille a la fin 
	tweets_pd=pd.DataFrame(container, columns=["Date Created", "Tweets"])
	tweets_pd["Date Created"]=tweets_pd["Date Created"].astype(str)
	#print(tweets_pd)

	if sys.platform == "win32":
		with pd.ExcelWriter(file_excel,engine="openpyxl",mode="a",if_sheet_exists="replace") as writer:
			tweets_pd.to_excel(writer, sheet_name=sheetname)


	csv_creator(tweets_pd,sheetname)

	if opencsv!="non":
		os.system(sheetname+".csv")
	
def extract_text(dataframe,header,language=""):
	liste=[]
	ntry=5
	for i in range(len(dataframe)):
		url=dataframe.iloc[i]
		#print(i)
		for j in range(ntry):
			try:
				image=r.get(url,headers=header,timeout=25) #instable si pas de headers
				image=Image.open(BytesIO(image.content))
				text=pytesseract.image_to_string(image)
				if language=="":
					liste.append(text)
					print(i)
				break
			except:
				if j == ntry - 1 :
					print("echec récuperation de l'url du tweet avec l'image")
	return liste

def get_texte(liste):
	texte_liste=[]

	for i in range(len(liste)):
		texte=liste[i].split("\n\n")
		texte_liste.append(texte)

	return texte_liste

def get_total(liste):
	total_liste=[]
	total_equipement=[]

	for i in range(len(liste)):
		sous_liste=liste[i]
		for j in range(len(sous_liste)):
			total_equipement=[]
			if any ("total" in s for s in sous_liste): 
				if "total" in sous_liste[j]:           #if not any("(" in s for s in vehicule)
					total = re.findall('[0-9]+', sous_liste[j])
					total_liste.append(total)
			else:
				for k in range(len(sous_liste)):	
				#if "total" not in sous_liste[j]:
					equipement=re.findall(r"\d+x+", sous_liste[k])
					for y in range(len(equipement)):
						data=re.findall('[0-9]+', equipement[y])
						if data:  #see if the list is not empty 
							total_equipement.append(data)
					
		if total_equipement:		#see if the list is not empty 
			total_equipement=applanir(total_equipement)
			total_equipement=convert_to_int(total_equipement)
			total=sum(total_equipement)
			total_liste.append([total])

	total_liste=applanir(total_liste)
	total_liste=convert_to_int(total_liste)			
	#print(len(total_liste))
	return total_liste


def multiple_try_extract_text(parameter1,parameter2,nt):
	tries = nt
	for i in range(tries):
		try:
			liste_texte=extract_text(parameter1,parameter2)
			return liste_texte
		except (SSLError,ConnectionError) :
			if i < tries - 1: # i is zero indexed
				time.sleep(2)
				continue
			else:
				raise
		break

def convert_StringDatetime_to_StringDate(liste):
	date_liste=[]
	string_liste=[]
	for i in range(len(liste)):
		date=datetime.fromisoformat(liste[i])   #2022-08-08 20:51:56+00:00
		date_liste.append(date)

	for i in range(len(date_liste)):
		string=datetime.strftime(date_liste[i], "%y-%m-%d")
		string_liste.append(string)

	return string_liste

def remove_duplicate(liste1,liste2):

	new_listes=[]
	i=0
	while i<len(liste1)-1:
		if liste2[i]==liste2[i+1]:
			liste2.pop(i)
			liste1.pop(i)
		else:
			i=i+1
		new_listes.append(liste1)
		new_listes.append(liste2)		
		return new_listes


def harmoniser(ListeRusseDate,ListeUkraineDate,ListeTotauxRusse,ListeTotauxUkraine):


	new_listes=remove_duplicate(ListeTotauxRusse,ListeRusseDate)
	ListeTotauxRusse=new_listes[0]
	ListeRusseDate=new_listes[1]
	new_listes=remove_duplicate(ListeTotauxUkraine,ListeUkraineDate)
	ListeTotauxUkraine=new_listes[0]
	ListeUkraineDate=new_listes[1]

	'''
	while i<=len(ListeTotauxRusse):
		if i>0 and ListeRusseDate[i]==ListeRusseDate[i-1]:
			ListeRusseDate.pop(i)
			ListeTotauxRusse.pop(i)
		i=i+1

	while i<=len(ListeTotauxUkraine):
		if i>0 and ListeUkraineDate[i]==ListeUkraineDate[i]:
			ListeUkraineDate.pop(i)
			ListeTotauxUkraine.pop(i)
		i=i+1		
'''

	date_return=[]
	final_harmonisation=[]
	missing_ukraine=list(set(ListeRusseDate)-set(ListeUkraineDate))
	#print(len(missing_ukraine))
	missing_russe=list(set(ListeUkraineDate)-set(ListeRusseDate))
	#print(len(missing_russe))

	if len(missing_ukraine)!=0:
		for i in range(len(ListeTotauxRusse)):
			for j in range(len(missing_ukraine)):
				if ListeRusseDate[i]==missing_ukraine[j]:
					#print("date russe")
					#print(ListeRusseDate[i])
					ListeUkraineDate.insert(i,ListeRusseDate[i])
					ListeTotauxUkraine.insert(i,0)
			
	
	if len(missing_russe)!=0:
		for i in range(len(ListeTotauxUkraine)):
			for j in range(len(missing_russe)):
				if ListeUkraineDate[i]==missing_russe[j]:
					#print("date ukraine")
					#print(ListeUkraineDate[i])
					ListeRusseDate.insert(i,ListeUkraineDate[i])
					ListeTotauxRusse.insert(i,0)
	
	'''
	if ListeUkraineDate==ListeRusseDate:
		print("OKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
	else:
		print("ListeUkraineDate")
		print(len(ListeUkraineDate))
		print(ListeUkraineDate)
		print("ListeRusseDate")
		print(len(ListeRusseDate))
		print(ListeRusseDate)
		diffe=list(set(ListeRusseDate)-set(ListeUkraineDate))
		print("diffe")
		print(diffe)
	'''

	date_return=ListeUkraineDate #peut aussi être ListeRusseDate

	final_harmonisation.append(date_return)
	final_harmonisation.append(ListeTotauxRusse)
	final_harmonisation.append(ListeTotauxUkraine)


	return final_harmonisation




##################################################################################

#pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\Tesseract.exe'

today=datetime.now()
today=str(today)
today = re.sub(INVALID_TITLE_REGEX, '-', today)
print(today)

date_start_war = datetime(2022, 2, 24).date()
string_date_start_war = datetime.strftime(date_start_war, '%d.%m.%Y')



aujour=datetime.now().date()
string_aujour= aujour.strftime('%d.%m.%Y') 


diff=aujour-date_start_war
diff=diff.days


n=25
ntry=50

########

current_directory = os.getcwd()

folder="TwitterUkraine"
directory_TwitterUkraine = os.path.join(current_directory, folder)

if not os.path.exists(directory_TwitterUkraine):
	os.makedirs(directory_TwitterUkraine)


#######

header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}

file_excel=directory_TwitterUkraine+'\\ScrapperTwitterUkraine.xlsx'

file_excel=file_excel.replace("\\", "\\\\")


file_text=directory_TwitterUkraine+'\\Data_TwitterUkraine.txt'

file_text=file_text.replace("\\", "\\\\")


if sys.platform == "win32" and exists(file_excel)!=True:
	excel=xs.Workbook(file_excel)
	excel.close()




#scrapper_user('since:2022-02-24 from:Liveuamap',"Liveuamap",number=n)
#scrapper_user('since:2022-02-24 from:UAWeapons',"UAWeapons",number=n)
try:
	scrapper_user('Russia OR Russian OR Ukraine OR Ukrainian OR Kremlin OR Putin OR Zelensky',"TheStudyofWar",number=n)
	print("updated")
except:
	print("error API twitter ou fichier ouvert: travail sur un sheet TheStudyofWar non mis a jour a la place: upgrade snscrape sur la version la plus récente pour voir si correction ")

try:	
	scrapper_user('Russia OR Russian OR Ukraine OR Ukrainian OR Kremlin OR Putin OR Zelensky since:2022-02-24 from:DefenceU',"DefenceU",number=n)
	print("updated")
except:
	print("error API twitter ou fichier ouvert: travail sur un sheet DefenceU non mis a jour a la place: upgrade snscrape sur la version la plus récente pour voir si correction ")

try:
	scrapper_user('intercepted call since:2022-02-24 from:wartranslated',"wartranslated_intercepted",number=n)
	print("updated")
except:
	print("error API twitter ou fichier ouvert: travail sur un sheet wartranslated_intercepted non mis a jour a la place: upgrade snscrape sur la version la plus récente pour voir si correction ")

try:
	scrapper_user('https://t.me OR telegram OR Girkin OR girkin since:2022-02-24 from:wartranslated',"wartranslated_translated",number=n)
	print("updated")
except:
	print("error API twitter ou fichier ouvert: travail sur un sheet wartranslated_translated non mis a jour a la place: upgrade snscrape sur la version la plus récente pour voir si correction ")

try:
	scrapper_user('since:2022-02-24 from:RALee85',"RobLee",number=n)
	print("updated")
except:
	print("error API twitter ou fichier ouvert: travail sur un sheet RobLee non mis a jour a la place: upgrade snscrape sur la version la plus récente pour voir si correction ")

try:
	scrapper_user('Overview of Russian equipment losses since:2022-02-24 from:Rebel44CZ',"Jakub_Russian",number=diff,image="yes")
	print("updated")
except:
	print("error API twitter ou fichier ouvert: travail sur un sheet Jakub_Russian non mis a jour a la place: upgrade snscrape sur la version la plus récente pour voir si correction ")

try:
	scrapper_user('Overview of Ukrainian equipment losses since:2022-02-24 from:Rebel44CZ',"Jakub_Ukrainian",number=diff,image="yes")
	print("updated")
except:
	print("error API twitter ou fichier ouvert: travail sur un sheet Jakub_Ukrainian non mis a jour a la place: upgrade snscrape sur la version la plus récente pour voir si correction ")

try:
	scrapper_user('https://t.me OR telegram OR Girkin OR girkin OR Wagner OR Russia OR Ukrainian since:2022-02-24 from:wartranslated',"wartranslated_translated_image",number=500,image="yes",allimage="yes")
	print("updated")
except:
	print("error API twitter ou fichier ouvert: travail sur un sheet wartranslated_translated_image non mis a jour a la place: upgrade snscrape sur la version la plus récente pour voir si correction ")
	raise




pd.set_option('display.max_columns', None)

evolution_russie=pd.read_excel(file_excel,sheet_name="Jakub_Russian",usecols=['Date Created', 'Tweets'])
evolution_ukraine=pd.read_excel(file_excel,sheet_name="Jakub_Ukrainian",usecols=['Date Created', 'Tweets'])
telegram_image=pd.read_excel(file_excel,sheet_name="wartranslated_translated_image",usecols=['Date Created', 'Tweets'])
telegram_image = telegram_image.groupby('Date Created')['Tweets'].apply(list)
print(telegram_image)


evolution_russie_date=evolution_russie.iloc[:, 0]
evolution_russie_image=evolution_russie.iloc[:, 1]

evolution_ukraine_date=evolution_ukraine.iloc[:, 0]
evolution_ukraine_image=evolution_ukraine.iloc[:, 1]


liste_texte_russie=multiple_try_extract_text(evolution_russie_image,header,ntry) #car forte chance d'erreur SSL et faible chance d'erreur timeout 
liste_texte_ukraine=multiple_try_extract_text(evolution_ukraine_image,header,ntry) #car forte chance d'erreur SSL et faible chance d'erreur timeout

#multiple try individualisé pour augmenter chance de succès

total_russe=get_texte(liste_texte_russie)
total_russe=get_total(total_russe)
total_russe=total_russe[::-1]
evolution_russie_date=evolution_russie_date.iloc[::-1]
evolution_russie_date=list(evolution_russie_date)



total_ukraine=get_texte(liste_texte_ukraine)
total_ukraine=get_total(total_ukraine)
total_ukraine=total_ukraine[::-1]
evolution_ukraine_date=evolution_ukraine_date.iloc[::-1]
evolution_ukraine_date=list(evolution_ukraine_date)


evolution_russie_date=convert_StringDatetime_to_StringDate(evolution_russie_date)
#print("evolution_russie_date")
#print(evolution_russie_date)
#print(len(evolution_russie_date))
evolution_ukraine_date=convert_StringDatetime_to_StringDate(evolution_ukraine_date)
#print("evolution_ukraine_date")
#print(evolution_ukraine_date)
#print(len(evolution_ukraine_date))

#print("avant harmonisation total russe")
#print(total_russe)

#print("avant harmonisation total ukraine")
#print(total_ukraine)

harmonie=harmoniser(evolution_russie_date,evolution_ukraine_date,total_russe,total_ukraine)
#print("evolution_ukraine_date")
#print(evolution_ukraine_date)
#print(harmonie)

evolution_date=harmonie[0]
#print("evolution_date")
#print(evolution_date)
#print(len(evolution_date))
total_russe=harmonie[1]
#print("total_russe")
#print(total_russe)
#print(len(total_russe))
total_ukraine=harmonie[2]
#print("total_ukraine")
#print(total_ukraine)
#print(len(total_ukraine))



curb_russia=np.cumsum(total_russe)
curb_ukraine=np.cumsum(total_ukraine)


plt.figure(1)


X_axix=np.arange(len(evolution_date))

plt.xticks(fontsize=5, rotation=90)
plt.xticks(X_axix,evolution_date)


plt.plot(X_axix,total_russe,c="red",label="losses russian")
plt.plot(X_axix,total_ukraine,c="blue",label="losses ukrainian")
plt.title("variation des pertes des 2 camps")
plt.xlabel("date")
plt.ylabel("number")



for i,j in zip(X_axix,total_russe):
	plt.annotate(str(j),xy=(i,j),xytext=(5,5),textcoords="offset points",fontweight="bold",color="red",fontsize=5)

for i,j in zip(X_axix,total_ukraine):
	plt.annotate(str(j),xy=(i,j),xytext=(5,5),textcoords="offset points",fontweight="bold",color="blue",fontsize=5)

file_image=directory_TwitterUkraine+'\\variation_perte.png'

file_image=file_image.replace("\\", "\\\\")

plt.savefig(file_image)

os.startfile(file_image)

plt.figure(2)

X_axix=np.arange(len(evolution_date))

plt.xticks(fontsize=5, rotation=90)
plt.xticks(X_axix,evolution_date)


plt.plot(X_axix,curb_russia,c="red",label="losses russian")
plt.plot(X_axix,curb_ukraine,c="blue",label="losses ukrainian")
plt.title("variation des pertes des 2 camps")
plt.xlabel("date")
plt.ylabel("number")


'''
for i,j in zip(X_axix,curb_russia):
	plt.annotate(str(j),xy=(i,j),xytext=(5,5),textcoords="offset points",fontweight="bold",color="red",fontsize=5)

for i,j in zip(X_axix,curb_ukraine):
	plt.annotate(str(j),xy=(i,j),xytext=(5,5),textcoords="offset points",fontweight="bold",color="blue",fontsize=5)
'''


file_image=directory_TwitterUkraine+'\\courbe_perte.png'

file_image=file_image.replace("\\", "\\\\")

plt.savefig(file_image)


os.startfile(file_image)

os.system('"'+file_excel+ '"')



