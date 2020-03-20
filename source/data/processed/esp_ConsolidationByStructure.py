#%% [markdown]
# # CSV Consolidation ESP
# Creation date: 2020-03-20

#%% Imports
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import os # To access the OS separator char.

#%% Constants Setup
pathInputFile = "data/interim/esp/"
pathOutputFile = "data/processed/esp/"
metadataFile = "data/raw/esp/tabulaParameters.csv"

#%% Import metadata to use
dfMetadataAll = pd.read_csv(metadataFile, sep=";", header=0)

#%% Process Data Structure 3
dfMetadata = dfMetadataAll[dfMetadataAll["Structure"]==3]
dfMetadata.drop(["Structure"], axis=1, inplace=True)

dfConsolidated = pd.DataFrame()

for index, file in dfMetadata.iterrows():
    fileName = file["File"].split(".")[-2] + ".csv"
    print("Processing file: " + fileName)

    # Date will be calculated sequentially. First file id 31 is from 2020-02-26.
    firstDateId = 31
    firstDate = pd.to_datetime('2020-02-26')
    dateId = int(fileName.split("_")[1])
    date = firstDate + pd.Timedelta(days=dateId-firstDateId)
    
    if dfConsolidated.size == 0:
        # No file loaded yet.
        namesColumns = ["Region","Total confirmed cases","Population Incidence Ratio","ICU cases","Total deaths"]
        dfConsolidated = pd.read_csv(pathInputFile+fileName, sep=",", skipinitialspace=True, header=0, names=namesColumns, skipfooter=1, encoding='utf-8')
        dfConsolidated.insert(0, "Date", date, allow_duplicates=False) 

        dfConsolidated["Population Incidence Ratio"] = dfConsolidated["Population Incidence Ratio"].str.replace(",",".")
        dfConsolidated.fillna(0, inplace=True)
    else:
        dfImported = pd.read_csv(pathInputFile+fileName, sep=",", skipinitialspace=True, header=0, names=namesColumns, skipfooter=1, encoding='utf-8')
        dfImported.insert(0, "Date", date, allow_duplicates=False) 

        dfImported["Population Incidence Ratio"] = dfImported["Population Incidence Ratio"].str.replace(",",".")
        dfImported.fillna(0, inplace=True)

        dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)
    
    #% Adjust column types.
    dfConsolidated["Date"] = dfConsolidated["Date"].astype(str)
    dfConsolidated["Region"] = dfConsolidated["Region"].astype(str)
    dfConsolidated["Total confirmed cases"] = dfConsolidated["Total confirmed cases"].astype('int64')
    dfConsolidated["Population Incidence Ratio"] = dfConsolidated["Population Incidence Ratio"].astype('float64')
    dfConsolidated["ICU cases"] = dfConsolidated["ICU cases"].astype('int64')
    dfConsolidated["Total deaths"] = dfConsolidated["Total deaths"].astype('int64')

    print("Total records: " + str(dfConsolidated["Date"].size))

#%% Write to file consolidated dataframe
dfConsolidated.to_csv(path_or_buf=pathOutputFile+"ESP-COVID19_Structure3"+".csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")