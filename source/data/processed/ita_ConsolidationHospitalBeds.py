#%% [markdown]
# # CSV interim processing ITA Hospital
# Creation date: 2020-03-26

#%% Imports
import pandas as pd # To work similar to R in Python
import csv #To load the tags metadatas
import os # To access the OS separator char.

#%% Constants Setup
pathInputFile = "data/interim/ita/ITA_HospitalPlacesPerRegion.csv"
pathOutputFile = "data/processed/ita/"
outputFile = "ITA_HospitalPlacesPerRegion.csv"


#%% Process Data Structure 1 regional
dfConsolidated = pd.DataFrame()

file = pathInputFile
fileName = file.split(os.sep)[-1]
print("Processing file: " + fileName)

namesColumns = ["Year","Country", "Region","Hospital Name","Province","ID Type of Hospital","Description Type of Hospital","Type of beds", "Total Hospital beds standard", "Total Private Hospital beds", "Total Daycare Hospital beds", "Total Surgery Hospital beds", "Total Hospital beds"]

dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)

#%% Filter data.
dfImported = dfImported[dfImported["Year"]==dfImported["Year"].max()]
dfImported = dfImported[dfImported["Type of beds"]=="Acuti"]
dfImported = dfImported[dfImported["ID Type of Hospital"] != 9]

#%% Calculate new columns
dfImported["Hospital ownership"] = dfImported["ID Type of Hospital"].apply(lambda rowValue: 'Private' if rowValue in [2.3, 3.2, 3.3, 5.1, 8] else 'State owned')

#%% Remove unnecessary columns
namesColumnsOutput = ["Year","Country", "Region","Province","Hospital ownership", "Hospital Name", "Total Hospital beds standard", "Total Private Hospital beds", "Total Daycare Hospital beds", "Total Surgery Hospital beds", "Total Hospital beds"]
dfImported = dfImported[namesColumnsOutput]

#%% Adjust data types
dfImported["Year"] = dfImported["Year"].astype('int64')
dfImported["Total Hospital beds standard"] = dfImported["Total Hospital beds standard"].astype('int64')
dfImported["Total Private Hospital beds"] = dfImported["Total Private Hospital beds"].astype('int64')
dfImported["Total Daycare Hospital beds"] = dfImported["Total Daycare Hospital beds"].astype('int64')
dfImported["Total Surgery Hospital beds"] = dfImported["Total Surgery Hospital beds"].astype('int64')
dfImported["Total Hospital beds"] = dfImported["Total Hospital beds"].astype('int64')

#%% Write to file consolidated dataframe
dfImported.to_csv(path_or_buf=pathOutputFile+outputFile, index=False, quoting=csv.QUOTE_NONNUMERIC)
print("Total raw records: " + str(dfImported["Hospital Name"].size))

print("Done.")