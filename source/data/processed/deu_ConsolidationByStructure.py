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
pathInputFile = "data/processed/deu/"
pathOutputFile = "data/processed/deu/"
metadataFile = "data/raw/deu/tabulaParameters.csv"
startFileName = ""
endFileName = "-en.csv"

dfConsolidated = pd.DataFrame()

rawFiles = glob.glob(os.path.join(pathInputFile, startFileName+"*"+endFileName))
for file in rawFiles:
    fileName = file.split(os.sep)[-1]
    print("Processing file: " + fileName)

    # Date will be calculated sequentially based on the previous highest id's date.    
    if dfConsolidated.size == 0:
        # No file loaded yet.
        namesColumns = ["Date","Region","Total confirmed cases","New cases", "Population Incidence Ratio","Total deaths"]
        dfConsolidated = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)

    else:
        try:
            namesColumns = ["Date","Region","Total confirmed cases","New cases", "Population Incidence Ratio","Total deaths"]
            dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)
        except ValueError:
            namesColumns = ["Date", "Region", "Total confirmed cases", "Population Incidence Ratio", "Total deaths"]
            dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)

        dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)

    print("Total records: " + str(dfConsolidated["Date"].size))

#%% Add Country column.
dfConsolidated.insert(1, "Country", "Germany", allow_duplicates=False) 

#%% Align data types.
#STR
dfConsolidated["Date"] = dfConsolidated["Date"].astype(str)
dfConsolidated["Region"] = dfConsolidated["Region"].astype(str)
#INT, int does not support NaN in pandas-numpy so if column contains nan we should map to float. Source: https://pandas.pydata.org/pandas-docs/stable/user_guide/gotchas.html#support-for-integer-na
intColumns = ["Total confirmed cases", "New cases", "Total deaths"]
for column in intColumns:
    try:
        dfConsolidated[column] = dfConsolidated[column].astype('int64')
    except ValueError:
        dfConsolidated[column] = dfConsolidated[column].astype('float64')
#FLOAT
floatColumns = ["Population Incidence Ratio"]
for column in floatColumns:
    dfConsolidated[column] = dfConsolidated[column].astype('float64')

#%% Write to file consolidated dataframe
dfConsolidated.to_csv(path_or_buf=pathOutputFile+"DEU-COVID19"+".csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")