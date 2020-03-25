#%% [markdown]
# # CSV Consolidation ESP
# Creation date: 2020-03-20

#%% Imports
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import os # To access the OS separator char.
import glob #To be able to dynamically load files matching pattern.
import io # To work with files read/write 

#%% Constants Setup
pathInputFile = "data/interim/esp/"
pathOutputFile = "data/processed/esp/"
metadataFile = "data/raw/esp/tabulaParameters.csv"
datesFile = "data/raw/esp/reportDates.csv"

startFileName = "Actualizacion_"
endFileName = "_COVID-19.csv"

namesOfRegions = ["Andalucía","Aragón","Asturias","Baleares","Canarias","Cantabria","Castilla-La Mancha","Castilla La Mancha","Castilla y León","Cataluña","Ceuta","C. Valenciana","Extremadura","Galicia","Madrid","Melilla","Murcia","Navarra","País Vasco","La Rioja"]

#%% Import metadata to use
dfMetadataAll = pd.read_csv(metadataFile, sep=";", header=0)
dfMetadataAll["ID"] = dfMetadataAll["File"].str.split("_").str[1]
dfMetadataAll["ID"] = dfMetadataAll["ID"].astype('int64')

dfDatesAll = pd.read_csv(datesFile, sep=";", header=0, index_col=False, parse_dates=['Date'], infer_datetime_format=True )
dfDatesAll["ID"] = dfDatesAll["File"].str.split("_").str[1]
dfDatesAll["ID"] = dfDatesAll["ID"].astype('int64')

rawFiles = glob.glob(os.path.join(pathInputFile, startFileName+"*"+endFileName))

#%% Iterate through files.
for file in rawFiles:
    fileName = file.split(os.sep)[-1]
    print("Processing file: " + fileName)

    with io.open(pathOutputFile+fileName, mode='w', encoding="utf-8") as outputFileObject:
        with io.open(file, mode='r', encoding="utf-8") as fileObject:
            #fileContents = fileObject.read()
            for line in fileObject:
                if any(region in line for region in namesOfRegions):
                    for region in namesOfRegions:
                        line = line.replace(region, region+",")
                    outputFileObject.write(line)
                else:
                    continue

    # Date will be calculated sequentially based on the previous highest id's date
    dateId = int(fileName.split("_")[1])
    dfDatesTemp = dfDatesAll[dfDatesAll["ID"]<dateId]
    firstDateId = int(dfDatesTemp["ID"].max())
    date = dfDatesTemp["Date"].max() + pd.Timedelta(days=dateId-firstDateId)

    # Column Structure will be calculated sequentially based on the previous highest id's date
    fileId = int(fileName.split("_")[1])
    dfMetadataTemp = dfMetadataAll[dfMetadataAll["ID"]<=fileId]
    dfMetadataTemp = dfMetadataTemp[dfMetadataTemp["ID"]==(dfMetadataTemp["ID"].max())].iloc[0]
    fileStructureId = dfMetadataTemp["Structure"]

    if fileStructureId == 3:
        namesColumns = ["Region","Total confirmed cases","Population Incidence Ratio","ICU cases","Total deaths"]
    elif fileStructureId == 4:
        namesColumns = ["Region","Total confirmed cases","Population Incidence Ratio","Total Hospital cases", "ICU cases","Total deaths","New cases"]
    elif fileStructureId == 5:
        namesColumns = ["Region","Total confirmed cases","Population Incidence Ratio","Total Hospital cases", "ICU cases","Total deaths","Total cured","New cases"]

    dfImported = pd.read_csv(pathOutputFile+fileName, sep=",", skipinitialspace=True, header=None, skipfooter=0, encoding='utf-8', engine="python", index_col=False)

    #%% Data cleaning
    #% Cross-file
    # Find the columns where each value is null. Source: https://www.jitsejan.com/find-and-delete-empty-columns-pandas-dataframe.html
    empty_cols = [col for col in dfImported.columns if dfImported[col].isnull().all()]
    # Drop these columns from the dataframe
    dfImported.drop(empty_cols, axis=1, inplace=True)

    dfImported.rename(columns=dict(zip(dfImported.columns,namesColumns)), inplace=True)

    try:
        dfImported.insert(2, "First", dfImported["Total confirmed cases"].str.split(" ", expand=True)[0], allow_duplicates=False)
        dfImported.insert(3, "Last", dfImported["Total confirmed cases"].str.split(" ", expand=True)[1], allow_duplicates=False)
  
        dfImported.drop("Total confirmed cases", axis=1, inplace=True)

        dfImported.rename(columns=dict(zip(dfImported.columns,namesColumns)), inplace=True)
    except AttributeError:
        pass
  
    dfImported.insert(0, "Date", date.date(), allow_duplicates=False) 
    
    dfImported.fillna(0, inplace=True)

    # Clean points for correct decimal comma.
    for col in namesColumns:
        if col == "Region": continue
        try:
            dfImported[col] = dfImported[col].str.replace(",",".").astype('float64')
        except AttributeError:
            #Column is not a string-type.
            pass

    #% File specific
    if fileStructureId >= 3:
        dfImported["Region"] = dfImported["Region"].str.replace("-"," ").str.replace("C\.","Comunidad")
        dfImported.loc[dfImported["Total confirmed cases"].round() != dfImported["Total confirmed cases"], "Total confirmed cases"] = dfImported["Total confirmed cases"]*1000
        dfImported.loc[dfImported["ICU cases"].round() != dfImported["ICU cases"], "ICU cases"] = dfImported["ICU cases"]*1000
        dfImported.loc[dfImported["Total deaths"].round() != dfImported["Total deaths"], "Total deaths"] = dfImported["Total deaths"]*1000
    if fileStructureId >= 4: 
        dfImported.loc[dfImported["Total Hospital cases"].round() != dfImported["Total Hospital cases"], "Total Hospital cases"] = dfImported["Total Hospital cases"]*1000
        dfImported.loc[dfImported["New cases"].round() != dfImported["New cases"], "New cases"] = dfImported["New cases"]*1000
    if fileStructureId >= 5:
        dfImported.loc[dfImported["Total cured"].round() != dfImported["Total cured"], "Total cured"] = dfImported["Total cured"]*1000

    #%% Type alignment.
    if fileStructureId >= 3:
        dfImported["Date"] = dfImported["Date"].astype(str)
        dfImported["Region"] = dfImported["Region"].astype(str)
        dfImported["Total confirmed cases"] = dfImported["Total confirmed cases"].astype('int64')
        dfImported["Population Incidence Ratio"] = dfImported["Population Incidence Ratio"].astype('float64')
        dfImported["ICU cases"] = dfImported["ICU cases"].astype('int64')
        dfImported["Total deaths"] = dfImported["Total deaths"].astype('int64')
    if fileStructureId >= 4:
        dfImported["Total Hospital cases"] = dfImported["Total Hospital cases"].astype('int64')
        dfImported["New cases"] = dfImported["New cases"].astype('int64')
    if fileStructureId >= 5:
        dfImported["Total cured"] = dfImported["Total cured"].astype('int64')

    #%% Write to file cleaned dataframe
    dfImported.to_csv(path_or_buf=pathOutputFile+fileName, index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")

# %%
