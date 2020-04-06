#%% [markdown]
# # CSV Downloader France
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
pathOutputFiles = "data/raw/fra/"
rootURL = "https://www.data.gouv.fr/fr/datasets/r/"

#%% File Name pattern: start+sequentialInteger+end
startFileName = "fra-covid19-hospitalieres-departement"
endFileName = ".csv"
downloadFileName = "63352e38-d353-4b54-bfd1-f1b3ee1cabd7"

#Get official file name to store it.
#todayDate = pd.to_datetime('today')
fileName = startFileName+endFileName

if "Erreur 404" in requests.get(rootURL+downloadFileName, verify = False).text:
    print("ERROR: FRA raw File not found.")
else:
    print("Downloading file "+rootURL+downloadFileName)
    # https://stackoverflow.com/a/7244263
    with open(pathOutputFiles+fileName, 'wb') as out_file:
        out_file.write(requests.get(rootURL+downloadFileName, verify = False).content)

#%% File Name pattern: start+sequentialInteger+end
startFileName = "fra-covid19-tests-departement"
endFileName = ".csv"
downloadFileName = "b4ea7b4b-b7d1-4885-a099-71852291ff20"

#Get official file name to store it.
#todayDate = pd.to_datetime('today')
fileName = startFileName+endFileName

if "Erreur 404" in requests.get(rootURL+downloadFileName, verify = False).text:
    print("ERROR: FRA raw File not found.")
else:
    print("Downloading file "+rootURL+downloadFileName)
    # https://stackoverflow.com/a/7244263
    with open(pathOutputFiles+fileName, 'wb') as out_file:
        out_file.write(requests.get(rootURL+downloadFileName, verify = False).content)