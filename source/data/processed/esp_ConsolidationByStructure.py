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
pathInputFile = "data/processed/esp/"
pathOutputFile = "data/processed/esp/"
metadataFile = "data/raw/esp/tabulaParameters.csv"
datesFile = "data/raw/esp/reportDates.csv"
startFileName = "Actualizacion_"
endFileName = ".csv"

#%% Import metadata to use
dfMetadataAll = pd.read_csv(metadataFile, sep=";", header=0)
dfMetadataAll["ID"] = dfMetadataAll["File"].str.split("_").str[1]
dfMetadataAll["ID"] = dfMetadataAll["ID"].astype('int64')

dfConsolidated = pd.DataFrame()

rawFiles = glob.glob(os.path.join(pathInputFile, startFileName+"*"+endFileName))
for file in rawFiles:
    fileName = file.split(os.sep)[-1]
    print("Processing file: " + fileName)

    # Column Structure will be calculated sequentially based on the previous highest id's date
    fileId = int(fileName.split("_")[1])
    dfMetadataTemp = dfMetadataAll[dfMetadataAll["ID"]<=fileId]
    dfMetadataTemp = dfMetadataTemp[dfMetadataTemp["ID"]==(dfMetadataTemp["ID"].max())].iloc[0]
    fileStructureId = dfMetadataTemp["Structure"]

    # Date will be calculated sequentially based on the previous highest id's date.    
    if dfConsolidated.size == 0:
        # No file loaded yet.
        namesColumns = ["Date","Region","Total confirmed cases","Population Incidence Ratio","Total ICU cases","Total deaths"]
        dfConsolidated = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)

    else:
        if fileStructureId == 3:
            namesColumns = ["Date","Region","Total confirmed cases","Population Incidence Ratio","Total ICU cases","Total deaths"]
            
            dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)
            dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)
        elif fileStructureId == 4:
            namesColumns = ["Date","Region","Total confirmed cases","Population Incidence Ratio", "Total Hospital cases", "Total ICU cases","Total deaths", "New cases"]

            dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)
            dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)
        elif fileStructureId == 5:
            namesColumns = ["Date","Region","Total confirmed cases","Population Incidence Ratio", "Total Hospital cases", "Total ICU cases","Total deaths","Total cured", "New cases"]

            dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)
            dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)
        elif (fileStructureId >= 6) and ("-0" in fileName):
            namesColumns = ["Date", "Region","Total confirmed cases","Population Incidence Ratio", "New cases"]

            dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)
            dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)
        elif (fileStructureId == 6) and ("-1" in fileName):
            namesColumns = ["Date", "Region","Total Hospital cases", "New Hospital cases", "Total ICU cases", "New ICU cases", "Total deaths", "New deaths", "Total cured", "New cured"]

            dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)
            for region in dfImported["Region"].unique():
                for columnName in namesColumns[2:]:
                    dfConsolidated.loc[(dfConsolidated["Date"]==dfImported["Date"][0]) & (dfConsolidated["Region"]==region), columnName] = dfImported.loc[dfImported["Region"]==region][columnName].iloc[0]
        elif (fileStructureId >= 7) and ("-1" in fileName):
            namesColumns = ["Date", "Region","Total Hospital cases", "New Hospital cases", "Total ICU cases", "New ICU cases", "Total deaths", "New deaths"]

            dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)
            for region in dfImported["Region"].unique():
                for columnName in namesColumns[2:]:
                    dfConsolidated.loc[(dfConsolidated["Date"]==dfImported["Date"][0]) & (dfConsolidated["Region"]==region), columnName] = dfImported.loc[dfImported["Region"]==region][columnName].iloc[0]

    print("Total records: " + str(dfConsolidated["Date"].size))

#%% Add Country column.
#dfConsolidated.fillna(0, inplace=True)
dfConsolidated.insert(1, "Country", "Spain", allow_duplicates=False)

#%% Align data types.
#STR
dfConsolidated["Date"] = dfConsolidated["Date"].astype(str)
dfConsolidated["Region"] = dfConsolidated["Region"].astype(str)
#INT, int does not support NaN in pandas-numpy so if column contains nan we should map to float. Source: https://pandas.pydata.org/pandas-docs/stable/user_guide/gotchas.html#support-for-integer-na
intColumns = ["Total confirmed cases", "New cases", "Population Incidence Ratio", "Total ICU cases", "Total Hospital cases", "Total deaths", "Total cured", "New Hospital cases", "New ICU cases", "New deaths", "New cured"]
for column in intColumns:
    try:
        dfConsolidated[column] = dfConsolidated[column].astype('int64')
    except ValueError:
        dfConsolidated[column] = dfConsolidated[column].astype('float64')


#%% Write to file consolidated dataframe
dfConsolidated.to_csv(path_or_buf=pathOutputFile+"ESP-COVID19"+".csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")