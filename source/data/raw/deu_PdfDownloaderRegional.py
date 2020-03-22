#%% [markdown]
# # PDF Downloader Deutschland
# Source: https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Archiv.html
# RKI is the country's official health and public diseases entity.
# Creation date: 2020-03-21

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
pathOutputFiles = "data/raw/deu/"
rootURL = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/"

#%% File Name pattern: start+sequentialInteger+end
startFileName = ""
endFileName = "-en.pdf?__blob=publicationFile"

firstDate = pd.to_datetime('2020-03-04')
todayDate = pd.to_datetime('today')
numberOfDays = todayDate - firstDate
numberOfDays = numberOfDays.days

countFiles = 0

for dayId in range(numberOfDays):
    date = firstDate + pd.Timedelta(days=dayId)
    #Get official file name to store it.
    downloadName = startFileName+date.strftime("%Y-%m-%d")+endFileName
    fileName = downloadName.split("?")[0]

    if "Diese Seite gibt es nicht." in requests.get(rootURL+downloadName, verify = False).text:
        continue
    else:
        print("Downloading file "+fileName)
        # https://stackoverflow.com/a/7244263
        with open(pathOutputFiles+fileName, 'wb') as out_file:
            out_file.write(requests.get(rootURL+downloadName, verify = False).content)
            
        countFiles = countFiles + 1

print(str(countFiles) + " files downloaded.")