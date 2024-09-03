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


###########################################################################################

def extract_pdf_text_online(url,header):
	http = urllib3.PoolManager()
	pdf = http.request('GET', url)
	pdf_content = pdf.data
	#pdf=r.get(url,timeout=60,headers=header)
	with tempfile.NamedTemporaryFile() as temp_pdf:
		temp_pdf.write(pdf_content)
		temp_pdf.seek(0)
		#pdf= PyPDF2.PdfReader(temp_pdf)
		#pdf_text=pdf.extractText()
	return pdf_content
###########################################################################################

url="https://crsreports.congress.gov/product/pdf/IF/IF12092"
header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}

pdf=extract_pdf_text_online(url,header)
print(pdf)



