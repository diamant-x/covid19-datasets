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
pathOutputFiles = "data/raw/esp/"
rootURL = "https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/documentos/"

#%% File Name pattern: start+sequentialInteger+end
startFileName = "Actualizacion_"
endFileName = "_COVID-19.pdf"

# By substracting the dates we know the maximum number of reports issued (Assuming one per day).
firstDate = pd.to_datetime('2020-02-26')
todayDate = pd.to_datetime('today')
numberOfDays = todayDate - firstDate
numberOfDays = int(numberOfDays.days)

countFiles = 0

for fileId in range(numberOfDays+1): 
    #Get official file name to store it.
    fileName = startFileName+str(fileId+31)+endFileName

    if "Error 404" in requests.get(rootURL+fileName, verify = False).text:
        print("Error File not Found:\t"+ fileName)
        continue
    else:
        print("Downloading file:\t"+fileName)
        # https://stackoverflow.com/a/7244263
        with open(pathOutputFiles+fileName, 'wb') as out_file:
            out_file.write(requests.get(rootURL+fileName, verify = False).content)
        countFiles = countFiles + 1

print(str(countFiles) + " files downloaded.")