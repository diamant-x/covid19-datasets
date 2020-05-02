#%% [markdown]
# # CSV Combination and Homogenization GBR/UK
# Creation date: 2020-05-02

#%% Imports
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import os # To access the OS separator char.
import glob # To be able to use regex in python.


#%% Constants Setup
pathInputFile = "data/raw/gbr/"
pathOutputFile = "data/interim/gbr/"

startFileName = "coronavirus-cases_"
endFileName = ".csv"

rawFiles = glob.glob(os.path.join(pathInputFile, startFileName+"*"+endFileName))

#%% Process Data Structure 1 regional
dfConsolidated = pd.DataFrame()

for file in rawFiles:
    fileName = file.split(os.sep)[-1]
    print("Processing file:\t" + fileName)

    namesOriginals = ["Area name","Area type","Specimen date","Daily lab-confirmed cases","Cumulative lab-confirmed cases"]
    namesColumns = ["Region","Area type", "Date", "New cases", "Total confirmed cases"]
    renameDict = dict(zip(namesOriginals, namesColumns))
   
    dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, usecols=namesOriginals, encoding='utf-8')
    dfImported.rename(renameDict,axis='columns',inplace=True)

    dfImported = dfImported.loc[dfImported["Area type"] == "Nation"] # At the time of this source, only England data was both available from cases and deaths...
    dfImported = dfImported[["Date", "Region", "Total confirmed cases", "New cases"]]


    #%% Now we need to import and join the deaths.
    file = file.replace("-cases_", "-deaths_")
    if os.path.exists(file):
        fileName = file.split(os.sep)[-1]
        print("Processing file:\t" + fileName)
    else:
        print("Warning:\tNo companion deaths file found.")
        continue
    
    namesOriginals = ["Area name","Area type","Reporting date","Daily change in deaths","Cumulative deaths"]
    namesColumns = ["Region","Area type", "Date", "New deaths", "Total deaths"]
    renameDict = dict(zip(namesOriginals, namesColumns))
    try:
        dfImportedDeaths = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, usecols=namesOriginals, encoding='utf-8')
    except ValueError:
        namesOriginals = ["Area name","Area type","Reporting date","Daily hospital deaths","Cumulative hospital deaths"]
        renameDict = dict(zip(namesOriginals, namesColumns))
        dfImportedDeaths = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, usecols=namesOriginals, encoding='utf-8')

    dfImportedDeaths.rename(renameDict,axis='columns',inplace=True)

    dfImportedDeaths = dfImportedDeaths.loc[dfImportedDeaths["Area type"] == "Nation"]
    dfImportedDeaths = dfImportedDeaths[["Date", "Region", "Total deaths", "New deaths"]]

    dfConsolidated = pd.merge(dfImported, dfImportedDeaths, on=["Date", "Region"], how='left')
    
    #%% Add Country column.
    dfConsolidated.insert(1, "Country", "United Kingdom", allow_duplicates=False) 

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
    outputFile = fileName.replace("-deaths_", "_")
    dfConsolidated.to_csv(path_or_buf=pathOutputFile+outputFile, index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")