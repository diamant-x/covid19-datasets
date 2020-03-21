#%% [markdown]
# # PDF Downloader Spain
# Creation date: 2020-03-20

#%% Imports
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import glob #To be able to dynamically load files matching pattern.
import os # To access the OS separator char.
import requests #To issue REST commands
import urllib.request # to get contents web
import shutil # to store to file
import urllib3
urllib3.disable_warnings() #TODO: Fix SSL validation error.


#%% Constants Setup
pathOutputFiles = "data/raw/ita/"
rootURL = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/"

#%% File Name pattern: start+sequentialInteger+end
startFileName = "dpc-covid19-ita-regioni-"
endFileName = ".csv"

firstDate = pd.to_datetime('2020-02-24')
todayDate = pd.to_datetime('today')
numberOfDays = todayDate - firstDate
numberOfDays = numberOfDays.days

countFiles = 0

for dayId in range(numberOfDays): #We assume 360 reports maximum may be issued.
    date = firstDate + pd.Timedelta(days=dayId)
    #Get official file name to store it.
    fileName = startFileName+date.strftime("%Y%m%d")+endFileName

    if "Error 404" in requests.get(rootURL+fileName, verify = False).text:
        continue
    else:
        print("Downloading file "+fileName)
        # https://stackoverflow.com/a/7244263
        with open(pathOutputFiles+fileName, 'wb') as out_file:
            out_file.write(requests.get(rootURL+fileName, verify = False).content)
            
        countFiles = countFiles + 1

print(str(countFiles) + " files downloaded.")