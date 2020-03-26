#%% [markdown]
# # CSV Consolidation ESP
# Creation date: 2020-03-20

#%% Imports
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import os # To access the OS separator char.
import glob #To be able to dynamically load files matching pattern.

#%% Constants Setup
pathInputFile = "data/processed/esp/"
pathOutputFile = "data/processed/esp/"
metadataFile = "data/raw/esp/tabulaParameters.csv"
datesFile = "data/raw/esp/reportDates.csv"
startFileName = "Actualizacion_"
endFileName = "_COVID-19.csv"

#%% Import metadata to use
dfMetadataAll = pd.read_csv(metadataFile, sep=";", header=0)
dfMetadataAll["ID"] = dfMetadataAll["File"].str.split("_").str[1]
dfMetadataAll["ID"] = dfMetadataAll["ID"].astype('int64')

dfConsolidated = pd.DataFrame()

rawFiles = glob.glob(os.path.join(pathInputFile, startFileName+"*"+endFileName))
for file in rawFiles:
    fileName = file.split(os.sep)[-1]
    print("Processing file: " + fileName)

    # Column Structure will be calculated sequentially based on the previous highest id's date
    fileId = int(fileName.split("_")[1])
    dfMetadataTemp = dfMetadataAll[dfMetadataAll["ID"]<=fileId]
    dfMetadataTemp = dfMetadataTemp[dfMetadataTemp["ID"]==(dfMetadataTemp["ID"].max())].iloc[0]
    fileStructureId = dfMetadataTemp["Structure"]

    # Date will be calculated sequentially based on the previous highest id's date.    
    if dfConsolidated.size == 0:
        # No file loaded yet.
        namesColumns = ["Date","Region","Total confirmed cases","Population Incidence Ratio","Total ICU cases","Total deaths"]
        dfConsolidated = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)

    else:
        if fileStructureId == 3:
            namesColumns = ["Date","Region","Total confirmed cases","Population Incidence Ratio","Total ICU cases","Total deaths"]
        elif fileStructureId == 4:
            namesColumns = ["Date","Region","Total confirmed cases","Population Incidence Ratio", "Total Hospital cases", "Total ICU cases","Total deaths"]
        elif fileStructureId == 5:
            namesColumns = ["Date","Region","Total confirmed cases","Population Incidence Ratio", "Total Hospital cases", "Total ICU cases","Total deaths","Total cured"]
        
        dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)

        dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)
        dfConsolidated.fillna(0, inplace=True)

    print("Total records: " + str(dfConsolidated["Date"].size))

#%% Add Country column.
dfConsolidated.insert(1, "Country", "Spain", allow_duplicates=False) 

dfConsolidated["Date"] = dfConsolidated["Date"].astype(str)
dfConsolidated["Region"] = dfConsolidated["Region"].astype(str)
dfConsolidated["Total confirmed cases"] = dfConsolidated["Total confirmed cases"].astype('int64')
dfConsolidated["Population Incidence Ratio"] = dfConsolidated["Population Incidence Ratio"].astype('float64')
dfConsolidated["Total ICU cases"] = dfConsolidated["Total ICU cases"].astype('int64')
dfConsolidated["Total Hospital cases"] = dfConsolidated["Total Hospital cases"].astype('int64')
dfConsolidated["Total deaths"] = dfConsolidated["Total deaths"].astype('int64')
dfConsolidated["Total cured"] = dfConsolidated["Total cured"].astype('int64')

#%% Write to file consolidated dataframe
dfConsolidated.to_csv(path_or_buf=pathOutputFile+"ESP-COVID19"+".csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")