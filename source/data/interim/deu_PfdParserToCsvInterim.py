#%% [markdown]
# # PDF Parser DEU
# Creation date: 2020-03-21

#%% Imports
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import glob #To be able to dynamically load files matching pattern.
import os # To access the OS separator char.
import tabula # To scan OCR PDFs.

#%% Constants Setup
pathInputFile = "data/raw/deu"
pathOutputFile = "data/interim/deu/"
metadataFile = "data/raw/deu/tabulaParameters.csv"

startFileName = ""
endFileName = "-en.pdf"

#%% Import metadata to use
dfMetadataAll = pd.read_csv(metadataFile, sep=";", header=0, comment='#')
dfMetadataAll["CoreFileName"] = dfMetadataAll["File"].str.replace(startFileName,"").str.replace(endFileName,"")
rawFiles = glob.glob(os.path.join(pathInputFile, startFileName+"*"+endFileName))

#%% Process Data Structure
for file in rawFiles:
    fileName = file.split(os.sep)[-1]
    print("Processing file: " + fileName)

    dfMetadata = dfMetadataAll[dfMetadataAll["File"]==fileName]

    if dfMetadata.size == 0:
        #Try to find the previous file metadata identified and apply same settings, if none, then skip file.
        coreFileName = fileName.replace(startFileName,"").replace(endFileName,"")
        if coreFileName < dfMetadataAll["CoreFileName"].min():
            print("Skipping file due to no metadata defined.")
            continue
        else:
            dfMetadata = dfMetadataAll[dfMetadataAll["CoreFileName"]<coreFileName]
            dfMetadata = dfMetadata[dfMetadata["CoreFileName"]==dfMetadata["CoreFileName"].max()]
            fileMetadata = dfMetadata.iloc[0]
    else:
        fileMetadata = dfMetadata.iloc[0]

    parsedFile = tabula.read_pdf(file, lattice = fileMetadata["lattice"], multiple_tables = fileMetadata["multiple_tables"], pages = int(fileMetadata["pages"]), silent = False)
    if len(parsedFile) > 1:
        tableId = 0
        for table in parsedFile:
            #%% Prepare to write the parsing.
            outputFilename = fileName.split(".")[-2] + "-" + str(tableId) + ".csv"
            table.to_csv(pathOutputFile+outputFilename, index=False)
            tableId = tableId + 1
    else:
        dfFile = parsedFile[0]
        #%% Prepare to write the parsing.
        outputFilename = fileName.split(".")[-2] + ".csv"
        dfFile.to_csv(pathOutputFile+outputFilename, index=False)