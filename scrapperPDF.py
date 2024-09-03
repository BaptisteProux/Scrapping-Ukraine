import requests as r
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
from itertools import chain
import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import os
from os.path import exists
import sys
from datetime import datetime, date, timedelta
import xlsxwriter as xs
from openpyxl.workbook.child import INVALID_TITLE_REGEX
from openpyxl import load_workbook
import time
from requests.exceptions import SSLError
from requests.exceptions import ConnectionError
import PyPDF2
import tempfile
import io
import urllib3
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By




###########################################################################################

def extract_pdf_text_online(url,header):

	
	options = webdriver.ChromeOptions()

	profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": directory_pdf , "download.extensions_to_open": "applications/pdf"}
	options.add_experimental_option("prefs", profile)


	driver = webdriver.Chrome(chrome_options=options)
	driver.get(url)

	driver.implicitly_wait(10)

	pdf = driver.page_source
	driver.close()




	return pdf
###########################################################################################
current_directory = os.getcwd()
parent = os.path.dirname(current_directory)
print(parent)

folder="pdf"
directory_pdf = os.path.join(current_directory, folder)

if not os.path.exists(directory_pdf):
	os.makedirs(directory_pdf)


url="https://crsreports.congress.gov/product/pdf/IF/IF12092"
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}

pdf=extract_pdf_text_online(url,header)
print(pdf)



