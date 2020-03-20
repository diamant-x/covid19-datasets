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
pathInputFile = "data/processed/who/"
pathOutputFile = "data/processed/who/"
metadataFile = "data/raw/who/tabulaParameters.csv"

#%% Import metadata to use
dfMetadataAll = pd.read_csv(metadataFile, sep=";", header=0)

#%% Process Data Structure N
dfMetadata = dfMetadataAll[dfMetadataAll["Structure"]=="N"]
dfMetadata.drop(["Structure"], axis=1, inplace=True)

dfConsolidated = pd.DataFrame()

for index, file in dfMetadata.iterrows():
    fileName = file["File"].split(".")[-2] + ".csv"
    print("Processing file: " + fileName)

    date = fileName.split("-")[0]

    if dfConsolidated.size == 0:
        # No file loaded yet.
        dfConsolidated = pd.read_csv(pathInputFile+fileName, skipinitialspace=True, encoding='utf-8')
        dfConsolidated.insert(0, "Date", date, allow_duplicates=False) 
    else:
        dfImported = pd.read_csv(pathInputFile+fileName, skipinitialspace=True)
        dfImported.insert(0, "Date", date, allow_duplicates=False) 

        dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True, encoding='utf-8')
    
    #% Adjust column types.
    dfConsolidated["Date"] = dfConsolidated["Date"].astype(str)
    dfConsolidated["Country"] = dfConsolidated["Country"].astype(str)
    dfConsolidated["Total confirmed cases"] = dfConsolidated["Total confirmed cases"].astype('int64')
    dfConsolidated["Total confirmed new cases"] = dfConsolidated["Total confirmed new cases"].astype('int64')
    dfConsolidated["Total deaths"] = dfConsolidated["Total deaths"].astype('int64')
    dfConsolidated["Total new deaths"] = dfConsolidated["Total new deaths"].astype('int64')
    dfConsolidated["Transmission classification"] = dfConsolidated["Transmission classification"].astype(str)
    dfConsolidated["Days since last reported case"] = dfConsolidated["Days since last reported case"].astype('int64')

    print("Total records: " + str(dfConsolidated["Date"].size))

#% Write to file consolidated file
dfConsolidated.to_csv(path_or_buf=pathOutputFile+"WHO-COVID19_StructureN"+".csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")