#%% [markdown]
# # CSV Consolidation Country Region
# Creation date: 2020-03-23

#%% Imports
import pandas as pd # To work similar to R in Python
import csv #To load the tags metadatas
import os # To access the OS separator char.

#%% Constants Setup
inputFileList = ["data/processed/deu/DEU-COVID19.csv", "data/processed/esp/ESP-COVID19.csv", "data/processed/ita/ITA-COVID19_Regional.csv"]
pathOutputFile = "data/processed/"

dfConsolidated = pd.DataFrame()

for file in inputFileList:
    fileName = file.split(os.sep)[-1]
    print("Processing file: " + fileName)

    # Date will be calculated sequentially based on the previous highest id's date.    
    if dfConsolidated.size == 0:
        # No file loaded yet.
        namesColumns = ["Date","Country","Region","Total confirmed cases","Total deaths"]
        dfConsolidated = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)

    else:
        dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)

        dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)

    print("Total records: " + str(dfConsolidated["Date"].size))

dfConsolidated["Total confirmed cases"] = dfConsolidated["Total confirmed cases"].astype('int64')
dfConsolidated["Total deaths"] = dfConsolidated["Total deaths"].astype('int64')

#%% Write to file consolidated dataframe
dfConsolidated.to_csv(path_or_buf=pathOutputFile+"ALL-COVID19_CountryRegion.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")