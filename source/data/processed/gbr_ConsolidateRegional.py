#%% [markdown]
# # CSV Consolidation GBR
# Creation date: 2020-05-02

#%% Imports
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import os # To access the OS separator char.
import glob # To be able to use regex in python.


#%% Constants Setup
pathInputFile = "data/interim/gbr/"
pathOutputFile = "data/processed/gbr/"
outputFile = "GBR-COVID19.csv"

startFileName = "coronavirus_latest"
endFileName = ".csv"

rawFiles = glob.glob(os.path.join(pathInputFile, startFileName+"*"+endFileName))

#%% Process Data Structure 1 regional
dfConsolidated = pd.DataFrame()

for file in rawFiles:
    fileName = file.split(os.sep)[-1]
    print("Processing file: " + fileName)

    namesOriginals = ["Date", "Country", "Region", "Total confirmed cases", "New cases", "Total deaths", "New deaths"]

    dfConsolidated = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, usecols=namesOriginals, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
    
    #% Adjust column types.
    # Data source is clean enough.

    print("Total records: " + str(dfConsolidated["Date"].size))

#%% Align data types.
#STR
strColumns = ["Date", "Country", "Region"]
for column in strColumns:
    dfConsolidated[column] = dfConsolidated[column].astype(str)
#INT, int does not support NaN in pandas-numpy so if column contains nan we should map to float. Source: https://pandas.pydata.org/pandas-docs/stable/user_guide/gotchas.html#support-for-integer-na
intColumns = ["Total confirmed cases", "New cases", "Total deaths", "New deaths"]
for column in intColumns:
    try:
        dfConsolidated[column] = dfConsolidated[column].astype('int64')
    except ValueError:
        dfConsolidated[column] = dfConsolidated[column].astype('float64')

#%% Write to file consolidated dataframe
dfConsolidated.to_csv(path_or_buf=pathOutputFile+outputFile, index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")