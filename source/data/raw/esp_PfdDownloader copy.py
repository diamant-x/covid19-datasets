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

countFiles = 0

for fileId in range(360): #We assume 360 reports maximum may be issued.
    #Get official file name to store it.
    fileName = startFileName+str(fileId)+endFileName

    if "Error 404" in requests.get(rootURL+fileName, verify = False).text:
        continue
    else:
        print("Downloading file "+fileName)
        # https://stackoverflow.com/a/7244263
        with open(pathOutputFiles+fileName, 'wb') as out_file:
            out_file.write(requests.get(rootURL+fileName, verify = False).content)
        countFiles = countFiles + 1

print(str(countFiles) + " files downloaded.")