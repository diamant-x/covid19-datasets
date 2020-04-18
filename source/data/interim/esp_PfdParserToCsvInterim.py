#%% [markdown]
# # PDF Parser ESP
# Creation date: 2020-03-20

#%% Imports
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import glob #To be able to dynamically load files matching pattern.
import os # To access the OS separator char.
import tabula # To scan OCR PDFs.
from ast import literal_eval # To evalaute saved text arrays as real arrays.

#%% Constants Setup
pathInputFile = "data/raw/esp/"
pathOutputFile = "data/interim/esp/"
metadataFile = "data/raw/esp/tabulaParameters.csv"

startFileName = "Actualizacion_"
endFileName = "_COVID-19.pdf"

#%% Import metadata to use
dfMetadataAll = pd.read_csv(metadataFile, sep=";", header=0, dtype={"area":str})
dfMetadataAll["CoreFileName"] = dfMetadataAll["File"].str.replace(startFileName,"").str.replace(endFileName,"")
rawFiles = glob.glob(os.path.join(pathInputFile, startFileName+"*"+endFileName))

#%% Process Data Structure
for file in rawFiles:
    fileName = file.split(os.sep)[-1]

    outputFilename = fileName.split(".")[-2] + ".csv"
    if os.path.isfile(pathOutputFile+outputFilename):
        print("Skipping file as it was already processed: " + fileName)
        continue
    else:
        print("Processing file: " + fileName)



    dfMetadata = dfMetadataAll[dfMetadataAll["File"]==fileName]

    if dfMetadata.size == 0:
        #Try to find the previous file metadata identified and apply same settings, if none, then skip file.
        coreFileName = fileName.replace(startFileName,"").replace(endFileName,"")
        if coreFileName < dfMetadataAll["CoreFileName"].min():
            print("Skipping file due to no metadata defined.")
            continue
        else:
            dfMetadata = dfMetadataAll[dfMetadataAll["CoreFileName"]<=coreFileName]
            dfMetadata = dfMetadata[dfMetadata["CoreFileName"]==dfMetadata["CoreFileName"].max()]
            fileMetadata = dfMetadata.iloc[0]
    else:
        fileMetadata = dfMetadata.iloc[0]
    #if fileMetadata["Structure"]==3: @TODO: If required, here we should implement different treatment.
    if pd.isnull(fileMetadata["area"]):
        try:
            parsedFile = tabula.read_pdf(file, lattice = fileMetadata["lattice"], stream=fileMetadata["stream"], multiple_tables=fileMetadata["multiple_tables"], pages=int(fileMetadata["pages"]), silent = True)
        except (ValueError, TypeError):
            parsedFile = tabula.read_pdf(file, lattice = fileMetadata["lattice"], stream=fileMetadata["stream"], multiple_tables=fileMetadata["multiple_tables"], pages=str(fileMetadata["pages"]), silent = True)
    else:
        try:
            parsedFile = tabula.read_pdf(file, lattice = fileMetadata["lattice"], stream=fileMetadata["stream"], relative_area=True, area=literal_eval(fileMetadata["area"]), multiple_tables=fileMetadata["multiple_tables"], pages=int(fileMetadata["pages"]), silent = True)
        except (ValueError, TypeError):
            parsedFile = tabula.read_pdf(file, lattice = fileMetadata["lattice"], stream=fileMetadata["stream"], relative_area=True, area=literal_eval(fileMetadata["area"]), multiple_tables=fileMetadata["multiple_tables"], pages=str(fileMetadata["pages"]), silent = True)
    if len(parsedFile) > 1:
        tableId = 0
        for table in parsedFile:
            #%% Prepare to write the parsing.
            outputFilename = fileName.split(".")[-2] + "-" + str(tableId) + ".csv"
            if os.path.isfile(pathOutputFile+outputFilename):
                print("Skipping file as it was already processed: " + outputFilename)
                tableId = tableId + 1
                continue
            else:
                table.to_csv(pathOutputFile+outputFilename, index=False, sep=";")
                tableId = tableId + 1
    else:
        dfFile = parsedFile[0]
        #%% Prepare to write the parsing.
        outputFilename = fileName.split(".")[-2] + ".csv"
        dfFile.to_csv(pathOutputFile+outputFilename, index=False, sep=";")