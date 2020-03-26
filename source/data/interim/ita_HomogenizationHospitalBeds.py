#%% [markdown]
# # CSV interim processing ITA Hospital
# Creation date: 2020-03-26

#%% Imports
import pandas as pd # To work similar to R in Python
import csv #To load the tags metadatas
import os # To access the OS separator char.

#%% Constants Setup
pathInputFile = "data/raw/ita/ITA_HospitalPlacesPerRegion.csv"
pathOutputFile = "data/interim/ita/"
outputFile = "ITA_HospitalPlacesPerRegion.csv"


#%% Process Data Structure 1 regional
dfConsolidated = pd.DataFrame()

file = pathInputFile
fileName = file.split(os.sep)[-1]
print("Processing file: " + fileName)

namesOriginals = ["Anno", "Descrizione Regione", "Denominazione struttura", "Comune", "Codice tipo struttura", "Descrizione tipo struttura", "Tipo di Disciplina", "Posti letto degenza ordinaria", "Posti letto degenza a pagamento", "Posti letto Day Hospital", "Posti letto Day Surgery", "Totale posti letto"]
namesColumns = ["Year","Region","Hospital Name","Province","ID Type of Hospital","Description Type of Hospital","Type of beds", "Total Hospital beds standard", "Total Private Hospital beds", "Total Daycare Hospital beds", "Total Surgery Hospital beds", "Total Hospital beds"]
renameDict = dict(zip(namesOriginals, namesColumns))

dfImported = pd.read_csv(file, sep=";", skipinitialspace=True, header=0, usecols=namesOriginals, encoding='utf-8')
dfImported.rename(renameDict,axis='columns',inplace=True)

#%% Clean data.
dfImported["Region"] = dfImported["Region"].str.title()
dfImported["Province"] = dfImported["Province"].str.title().str.strip()
dfImported["Hospital Name"] = dfImported["Hospital Name"].str.title().str.strip()
dfImported["Description Type of Hospital"] = dfImported["Description Type of Hospital"].str.title()
dfImported["Type of beds"] = dfImported["Type of beds"].str.title()
dfImported = dfImported[dfImported["Total Hospital beds"]!="N.D."]

#%% Adjust data types
dfImported["Total Hospital beds standard"] = dfImported["Total Hospital beds standard"].astype('int64')
dfImported["Total Private Hospital beds"] = dfImported["Total Private Hospital beds"].astype('int64')
dfImported["Total Daycare Hospital beds"] = dfImported["Total Daycare Hospital beds"].astype('int64')
dfImported["Total Surgery Hospital beds"] = dfImported["Total Surgery Hospital beds"].astype('int64')
dfImported["Total Hospital beds"] = dfImported["Total Hospital beds"].astype('int64')

#%% Add Country column.
dfImported.insert(1, "Country", "Italy", allow_duplicates=False) 

#%% Write to file consolidated dataframe
dfImported.to_csv(path_or_buf=pathOutputFile+outputFile, index=False, quoting=csv.QUOTE_NONNUMERIC)
print("Total raw records: " + str(dfImported["Hospital Name"].size))

print("Done.")