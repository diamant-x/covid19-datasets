#%% [markdown]
# # PDF Parser
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
pathOutputFiles = "data/raw/who/"
rootURL = "https://www.who.int"

#%% Get list of files
requestListOfFiles = requests.get('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports')
webSourceCode = requestListOfFiles.text

#TODO: Refactor code from iterator to parser.
DataRAWString = webSourceCode.partition("""<div class="sf-content-block content-block" >\r\n    <div ><p>""")[2]
DataRAWString = DataRAWString.partition("""21 January 2020</p><p>&nbsp;</p></div>""")[0]

DataRAWString = DataRAWString.partition("href=\"/docs/default-source/coronaviruse")[2]
DataRAWString = "/docs/default-source/coronaviruse"+DataRAWString
(urlFile, separator, DataRAWString) = DataRAWString.partition("\">")
countFiles = 0

while len(DataRAWString) >0:
    #Get official file name to store it.
    fileName = urlFile.split("/")[-1]
    fileName = fileName.split("?")[0]
    print("Downloading file "+fileName)

    # https://stackoverflow.com/a/7244263
    with open(pathOutputFiles+fileName, 'wb') as out_file:
        out_file.write(requests.get(rootURL+urlFile).content)
    countFiles = countFiles + 1

    # Prepare variable for next file.
    DataRAWString = DataRAWString.partition("href=\"/docs/default-source/coronaviruse")[2]
    DataRAWString = "/docs/default-source/coronaviruse"+DataRAWString
    (urlFile, separator, DataRAWString) = DataRAWString.partition("\">")

print(str(countFiles) + " files downloaded. WHO website has duplicated links.")