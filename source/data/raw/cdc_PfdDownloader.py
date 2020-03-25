#%% [markdown]
# # eCDC downloader
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


#%% Constants Setup
pathOutputFiles = "data/raw/cdc/"
rootURL = "https://www.ecdc.europa.eu/sites/default/files/documents/"


#%% Download today's file
#Get official file name to store it.
fileName = "COVID-19-geographic-disbtribution-worldwide-"
fileName = fileName + pd.to_datetime('today').strftime("%Y-%m-%d") + ".xlsx"
print("Downloading file "+fileName)

# https://stackoverflow.com/a/7244263
with open(pathOutputFiles+fileName, 'wb') as out_file:
    out_file.write(requests.get(rootURL+fileName).content)

#%% Download yesterday's file in case they published it late.
#Get official file name to store it.
fileName = "COVID-19-geographic-disbtribution-worldwide-"
fileName = fileName + (pd.to_datetime('today') - pd.Timedelta(days=1)).strftime("%Y-%m-%d") + ".xlsx"
print("Downloading file "+fileName)

# https://stackoverflow.com/a/7244263
with open(pathOutputFiles+fileName, 'wb') as out_file:
    out_file.write(requests.get(rootURL+fileName).content)

print("eCDC status file downloaded.")