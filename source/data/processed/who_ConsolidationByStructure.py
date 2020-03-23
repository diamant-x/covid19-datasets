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
startFileName = "20"
endFileName = "-covid-19.csv"

dfConsolidated = pd.DataFrame()

rawFiles = glob.glob(os.path.join(pathInputFile, startFileName+"*"+endFileName))
for file in rawFiles:
    fileName = file.split(os.sep)[-1]
    print("Processing file: " + fileName)

    # Date will be calculated sequentially based on the previous highest id's date.    
    if dfConsolidated.size == 0:
        # No file loaded yet.
        namesColumns = ["Date","Country","Total confirmed cases","Total deaths"]
        dfConsolidated = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)

    else:
        dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)

        dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)

    print("Total records: " + str(dfConsolidated["Date"].size))

#%% Write to file consolidated dataframe
dfConsolidated.to_csv(path_or_buf=pathOutputFile+"WHO-COVID19"+".csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")