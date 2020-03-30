#%% [markdown]
# # CSV Downloader Spain
# Creation date: 2020-03-30

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
rootURL = "https://covid19.isciii.es/resources/"

#%% File Name pattern: start+sequentialInteger+end
fileName = "serie_historica_acumulados.csv"

print("Downloading file "+fileName)
# https://stackoverflow.com/a/7244263
with open(pathOutputFiles+fileName, 'wb') as out_file:
     out_file.write(requests.get(rootURL+fileName, verify = False).content)