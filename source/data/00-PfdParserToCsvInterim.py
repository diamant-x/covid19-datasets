#%% [markdown]
# # PDF Parser
# Creation date: 2020-03-18

#%% Imports
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import glob #To be able to dynamically load files matching pattern.
import os # To access the OS separator char.
import tabula # To scan OCR PDFs.

#%% Constants Setup
pathInputFile = "data/raw/"
pathOutputFile = "data/interim/"
metadataFile = "data/raw/tabulaParameters.csv"

#%% Import metadata to use
dfMetadataAll = pd.read_csv(metadataFile, sep=";", header=0)

#%% Process Data Structure N
dfMetadata = dfMetadataAll[dfMetadataAll["Structure"]=="N"]
dfMetadata.drop(["Structure"], axis=1, inplace=True)

for index, file in dfMetadata.iterrows():
    print("Processing file: " + file["File"])
    parsedFile = tabula.read_pdf(pathInputFile+file["File"], lattice = file["lattice"], multiple_tables=file["multiple_tables"], pages=file["pages"], silent = True)
    if len(parsedFile) > 1:
        tableId = 0
        for table in parsedFile:
            #%% Prepare to write the parsing.
            outputFilename = file["File"].split(".")[-2] + "-" + str(tableId) + ".csv"
            table.to_csv(pathOutputFile+outputFilename, index=False)
            tableId = tableId + 1
    else:
        dfFile = parsedFile[0]
        #%% Prepare to write the parsing.
        outputFilename = file["File"].split(".")[-2] + ".csv"
        dfFile.to_csv(pathOutputFile+outputFilename, index=False)