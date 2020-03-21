#%% [markdown]
# # CSV Consolidation ESP
# Creation date: 2020-03-20

#%% Imports
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import os # To access the OS separator char.
import glob # To be able to use regex in python.


#%% Constants Setup
pathInputFile = "data/raw/ita/"
pathOutputFile = "data/processed/ita/"
outputFile = "ITA-COVID19_Regional.csv"

startFileName = "dpc-covid19-ita-regioni-"
endFileName = ".csv"

rawFiles = glob.glob(os.path.join(pathInputFile, startFileName+"*"+endFileName))

#%% Process Data Structure 1 regional
dfConsolidated = pd.DataFrame()

for file in rawFiles:
    fileName = file.split(os.sep)[-1]
    print("Processing file: " + fileName)

    namesOriginals = ["data","denominazione_regione","totale_casi","deceduti","terapia_intensiva","tamponi"]
    namesColumns = ["Date","Region","Total confirmed cases","Total deaths","ICU cases","Total tests"]
    renameDict = dict(zip(namesOriginals, namesColumns))
   
    if dfConsolidated.size == 0:
        # No file loaded yet.
        
        dfConsolidated = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, usecols=namesOriginals, encoding='utf-8')
        dfConsolidated.rename(renameDict,axis='columns',inplace=True)

    else:
        dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, usecols=namesOriginals, encoding='utf-8')
        dfImported.rename(renameDict,axis='columns',inplace=True)

        dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)
    
    #% Adjust column types.
    # Data source is clean enough.

    print("Total records: " + str(dfConsolidated["Date"].size))

#%% Write to file consolidated dataframe
dfConsolidated.to_csv(path_or_buf=pathOutputFile+outputFile, index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")