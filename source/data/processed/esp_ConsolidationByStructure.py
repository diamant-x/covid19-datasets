#%% [markdown]
# # CSV Consolidation ESP
# Creation date: 2020-03-20

#%% Imports
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import os # To access the OS separator char.

#%% Constants Setup
pathInputFile = "data/interim/esp/"
pathOutputFile = "data/processed/esp/"
metadataFile = "data/raw/esp/tabulaParameters.csv"
datesFile = "data/raw/esp/reportDates.csv"


#%% Import metadata to use
dfMetadataAll = pd.read_csv(metadataFile, sep=";", header=0)
dfDatesAll = pd.read_csv(datesFile, sep=";", header=0, index_col=False, parse_dates=['Date'], infer_datetime_format=True )


#%% Process Data Structure 3
dfMetadata = dfMetadataAll[dfMetadataAll["Structure"]==3]
dfMetadata.drop(["Structure"], axis=1, inplace=True)

dfDates = dfDatesAll[dfDatesAll["Structure"]==3]
dfDates.drop(["Structure"], axis=1, inplace=True)
dfDates["ID"] = dfDates["File"].str.split("_").str[1]
dfDates["ID"] = dfDates["ID"].astype('int64')

dfConsolidated = pd.DataFrame()

for index, file in dfMetadata.iterrows():
    fileName = file["File"].split(".")[-2] + ".csv"
    print("Processing file: " + fileName)

    # Date will be calculated sequentially based on the previous highest id's date
    dateId = int(fileName.split("_")[1])
    dfDatesTemp = dfDates[dfDates["ID"]<dateId]
    firstDateId = int(dfDatesTemp["ID"].max())
    date = dfDatesTemp["Date"].max() + pd.Timedelta(days=dateId-firstDateId)
    
    if dfConsolidated.size == 0:
        # No file loaded yet.
        namesColumns = ["Region","Total confirmed cases","Population Incidence Ratio","ICU cases","Total deaths"]
        dfConsolidated = pd.read_csv(pathInputFile+fileName, sep=",", skipinitialspace=True, header=0, names=namesColumns, skipfooter=1, encoding='utf-8', engine="python", index_col=False)
        dfConsolidated.insert(0, "Date", date.date(), allow_duplicates=False) 

        dfConsolidated["Population Incidence Ratio"] = dfConsolidated["Population Incidence Ratio"].str.replace(",",".")
        dfConsolidated.fillna(0, inplace=True)
        dfConsolidated.loc[dfConsolidated["Total confirmed cases"].round() != dfConsolidated["Total confirmed cases"], "Total confirmed cases"] = dfConsolidated["Total confirmed cases"]*1000
        dfConsolidated["Total confirmed cases"] = dfConsolidated["Total confirmed cases"].astype('int64')
        dfConsolidated.loc[dfConsolidated["ICU cases"].round() != dfConsolidated["ICU cases"], "ICU cases"] = dfConsolidated["ICU cases"]*1000
        dfConsolidated["ICU cases"] = dfConsolidated["ICU cases"].astype('int64')
        dfConsolidated.loc[dfConsolidated["Total deaths"].round() != dfConsolidated["Total deaths"], "Total deaths"] = dfConsolidated["Total deaths"]*1000
        dfConsolidated["Total deaths"] = dfConsolidated["Total deaths"].astype('int64')

    else:
        dfImported = pd.read_csv(pathInputFile+fileName, sep=",", skipinitialspace=True, header=0, names=namesColumns, skipfooter=1, encoding='utf-8', engine="python", index_col=False)
        dfImported.insert(0, "Date", date.date(), allow_duplicates=False) 

        dfImported["Population Incidence Ratio"] = dfImported["Population Incidence Ratio"].str.replace(",",".")
        dfImported.fillna(0, inplace=True)
        dfImported.loc[dfImported["Total confirmed cases"].round() != dfImported["Total confirmed cases"], "Total confirmed cases"] = dfImported["Total confirmed cases"]*1000
        dfImported["Total confirmed cases"] = dfImported["Total confirmed cases"].astype('int64')
        dfImported["ICU cases"] = dfImported["ICU cases"].astype('int64')
        dfImported["Total deaths"] = dfImported["Total deaths"].astype('int64')

        dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)

#%% Process Data Structure 4
dfMetadata = dfMetadataAll[dfMetadataAll["Structure"]==4]
dfMetadata.drop(["Structure"], axis=1, inplace=True)

dfDates = dfDatesAll[dfDatesAll["Structure"]==3]
dfDates.drop(["Structure"], axis=1, inplace=True)
dfDates["ID"] = dfDates["File"].str.split("_").str[1]
dfDates["ID"] = dfDates["ID"].astype('int64')

namesColumns = ["Region","Total confirmed cases","Population Incidence Ratio","ICU cases","Total deaths","New confirmed cases"]

for index, file in dfMetadata.iterrows():
    fileName = file["File"].split(".")[-2] + ".csv"
    print("Processing file: " + fileName)

    # Date will be calculated sequentially based on the previous highest id's date
    dateId = int(fileName.split("_")[1])
    dfDatesTemp = dfDates[dfDates["ID"]<dateId]
    firstDateId = int(dfDatesTemp["ID"].max())
    date = dfDatesTemp["Date"].max() + pd.Timedelta(days=dateId-firstDateId)
    
    dfImported = pd.read_csv(pathInputFile+fileName, sep=",", skipinitialspace=True, header=None, skiprows=3, names=namesColumns, skipfooter=1, encoding='utf-8', engine="python", index_col=False)
    dfImported.insert(0, "Date", date.date(), allow_duplicates=False) 
    dfImported.drop(["New confirmed cases"], axis=1, inplace=True)

    dfImported["Population Incidence Ratio"] = dfImported["Population Incidence Ratio"].str.replace(",",".")
    dfImported.fillna(0, inplace=True)
    dfImported.loc[dfImported["Total confirmed cases"].round() != dfImported["Total confirmed cases"], "Total confirmed cases"] = dfImported["Total confirmed cases"]*1000
    dfImported["Total confirmed cases"] = dfImported["Total confirmed cases"].astype('int64')
    dfImported["ICU cases"] = dfImported["ICU cases"].astype('int64')
    dfImported["Total deaths"] = dfImported["Total deaths"].astype('int64')

    dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)
    
    
#% Adjust column types.
dfConsolidated["Date"] = dfConsolidated["Date"].astype(str)
dfConsolidated["Region"] = dfConsolidated["Region"].astype(str)
dfConsolidated["Total confirmed cases"] = dfConsolidated["Total confirmed cases"].astype('int64')
dfConsolidated["Population Incidence Ratio"] = dfConsolidated["Population Incidence Ratio"].astype('float64')
dfConsolidated["ICU cases"] = dfConsolidated["ICU cases"].astype('int64')
dfConsolidated["Total deaths"] = dfConsolidated["Total deaths"].astype('int64')
print("Total records: " + str(dfConsolidated["Date"].size))

#%% Write to file consolidated dataframe
dfConsolidated.to_csv(path_or_buf=pathOutputFile+"ESP-COVID19_Structure3"+".csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")