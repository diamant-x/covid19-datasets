#%% [markdown]
# # CSV interim processing Fra cases
# Creation date: 2020-04-06

#%% Imports
import pandas as pd # To work similar to R in Python
import csv #To load the tags metadatas
import os # To access the OS separator char.

#%% Constants Setup
pathInputFile = "data/raw/fra/fra-covid19-hospitalieres-departement.csv"
pathOutputFile = "data/interim/fra/"
outputFile = "fra-covid19-hospitalieres-departement.csv"

sexIdMapping = {
    0:"Total",
    1:"Male",
    2:"Female"}


#%% Load Province (Departement) and Region metadata.
fileProvinceMetadata = "data/processed/fra/fra-province-metadata.csv"
dfProvince = pd.read_csv(fileProvinceMetadata, sep=",", skipinitialspace=True, header=0, encoding='utf-8', index_col=False)
fileRegionMetadata = "data/processed/fra/fra-region-metadata.csv"
dfRegion = pd.read_csv(fileRegionMetadata, sep=",", skipinitialspace=True, header=0, encoding='utf-8', index_col=False)
dfMetadata = dfProvince.merge(dfRegion, on="Region ID", how="left")
dfMetadata = dfMetadata[["Province ID", "Province", "Region"]]
dfMetadata["Province ID"] = dfMetadata["Province ID"].astype(str)

#%% Process Data Structure 1 regional
file = pathInputFile
fileName = file.split(os.sep)[-1]
print("Processing file: " + fileName)

namesOriginals = ["dep","sexe","jour","hosp","rea","rad","dc"]
namesColumns = ["Province ID","Sex ID", "Date","Current Hospital cases", "Current ICU cases", "Total cured","Total deaths"]
renameDict = dict(zip(namesOriginals, namesColumns))

dfImported = pd.read_csv(file, sep=";", skipinitialspace=True, header=0, usecols=namesOriginals, encoding='utf-8', parse_dates=["jour"], dayfirst=True, index_col=False)
dfImported.rename(renameDict,axis='columns',inplace=True)

#%% Clean data.
dfImported = dfImported.replace({"Sex ID": sexIdMapping})
dfImported.rename({"Sex ID":"Genre"},axis='columns',inplace=True)
dfImported.fillna(0, inplace=True)

dfImported["Province ID"] = dfImported["Province ID"].astype(str)
dfImported = dfImported.merge(dfMetadata, on="Province ID", how="left")

#%% Adjust data types
dfImported["Total cured"] = dfImported["Total cured"].astype('int64')
dfImported["Current Hospital cases"] = dfImported["Current Hospital cases"].astype('int64')
dfImported["Current ICU cases"] = dfImported["Current ICU cases"].astype('int64')
dfImported["Total deaths"] = dfImported["Total deaths"].astype('int64')

#%% Reorder current columns

#%% Add Country column.
dfImported.insert(0, "Country", "France", allow_duplicates=False) 

#%% Write to file consolidated dataframe
dfImported.to_csv(path_or_buf=pathOutputFile+outputFile, index=False, quoting=csv.QUOTE_NONNUMERIC)
print("Total raw records: " + str(dfImported["Date"].size))

print("Done.")