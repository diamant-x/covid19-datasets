#%% [markdown]
# # PDF Parser
# Creation date: 2020-05-02

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
pathOutputFiles = "data/raw/gbr/"
rootURL = "https://coronavirus.data.gov.uk/downloads/"

#%% Get list of files
requestListOfFiles = requests.get('https://publicdashacc.blob.core.windows.net/downloads?restype=container&comp=list')
webSourceCode = requestListOfFiles.text

#TODO: Refactor code from iterator to parser.
DataRAWString = webSourceCode.partition("<Blob><Name>")[2]
(urlFile, separator, DataRAWString) = DataRAWString.partition("</Name>")
countFiles = 0

while len(DataRAWString) >0:
    #Get official file name to store it.
    fileName = urlFile.split("/")[-1]
    if ".csv" in fileName:
        print("Downloading file "+fileName)
    else:
        # Prepare variable for next file.
        DataRAWString = DataRAWString.partition("<Blob><Name>")[2]
        (urlFile, separator, DataRAWString) = DataRAWString.partition("</Name>")
        continue

    # https://stackoverflow.com/a/7244263
    with open(pathOutputFiles+fileName, 'wb') as out_file:
        out_file.write(requests.get(rootURL+urlFile).content)
    countFiles = countFiles + 1

    # Prepare variable for next file.
    DataRAWString = DataRAWString.partition("<Blob><Name>")[2]
    (urlFile, separator, DataRAWString) = DataRAWString.partition("</Name>")

print(str(countFiles) + " files downloaded.")