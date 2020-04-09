#%% [markdown]
# # CSV interim processing ITA Hospital
# Creation date: 2020-03-26

#%% Imports
import pandas as pd # To work similar to R in Python
import csv #To load the tags metadatas
import os # To access the OS separator char.

#%% Constants Setup
pathInputFile = "data/raw/esp/serie_historica_acumulados.csv"
pathOutputFile = "data/interim/esp/"
outputFile = "serie_historica_acumulados.csv"

dictRegionMapping = {
    "AN":"Andalucía",
    "AR":"Aragón",
    "AS":"Asturias",
    "IB":"Baleares",
    "CN":"Canarias",
    "CB":"Cantabria",
    "CM":"Castilla La Mancha",
    "CL":"Castilla y León",
    "CT":"Cataluña",
    "CE":"Ceuta",
    "VC":"Comunidad Valenciana",
    "EX":"Extremadura",
    "GA":"Galicia",
    "MD":"Madrid",
    "ME":"Melilla",
    "MC":"Murcia",
    "NC":"Navarra",
    "PV":"País Vasco",
    "RI":"La Rioja"}

#%% Process Data Structure 1 regional
dfConsolidated = pd.DataFrame()

file = pathInputFile
fileName = file.split(os.sep)[-1]
print("Processing file: " + fileName)

namesOriginals = ["CCAA","FECHA","CASOS ","Hospitalizados","UCI","Fallecidos","Recuperados"]
namesColumns = ["Region","Date","Total confirmed cases", "Total Hospital cases", "Total ICU cases","Total deaths","Total cured"]
renameDict = dict(zip(namesOriginals, namesColumns))

dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, skipfooter=2, usecols=namesOriginals, encoding='latin', engine='python', parse_dates=["Fecha"], dayfirst=True)
dfImported.rename(renameDict,axis='columns',inplace=True)

#%% Clean data.
dfImported = dfImported.replace({"Region": dictRegionMapping})
dfImported.fillna(0, inplace=True)

#%% Adjust data types
dfImported["Total confirmed cases"] = dfImported["Total confirmed cases"].astype('int64')
dfImported["Total Hospital cases"] = dfImported["Total Hospital cases"].astype('int64')
dfImported["Total ICU cases"] = dfImported["Total ICU cases"].astype('int64')
dfImported["Total deaths"] = dfImported["Total deaths"].astype('int64')

#%% Reorder current columns
dfImported = dfImported[["Date","Region","Total confirmed cases", "Total Hospital cases", "Total ICU cases","Total deaths"]]

#%% Add Country column.
dfImported.insert(1, "Country", "Spain", allow_duplicates=False) 

#%% Write to file consolidated dataframe
dfImported.to_csv(path_or_buf=pathOutputFile+outputFile, index=False, quoting=csv.QUOTE_NONNUMERIC)
print("Total raw records: " + str(dfImported["Date"].size))

print("Done.")