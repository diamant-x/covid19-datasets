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
import re # To replace using regex rules for complex scenarios
import _csv

#%% Constants Setup
pathInputFile = "data/interim/who/"
pathOutputFile = "data/processed/who/"
metadataFile = "data/raw/who/tabulaParameters.csv"

startFileName = "20"
endFileName = "-covid-19.csv"


namesOfMultilineRegions2 = {"Iran (Islamic,":"Iran (Islamic Republic of),", 
#"Iran (Islamic Republic,":"Iran (Islamic Republic of),", # Conflict iwth file 53
"United Arab,":"United Arab Emirates,", 
"United States Virgin,":"United States Virgin Islands", 
"Democratic Republic,":"Democratic Republic of the Congo", 
"United Republic of,":"United Republic of Tanzania", 
"Central African,":"Central African Republic", 
"Subtotal for all,":"Total", 
"International,,,,,,":"Diamond Princess", 
"Bosnia and,,,":"Bosnia and Herzegovina"}

namesOfMultilineRegions = ["the United,",
"\"Bosnia and", 
"\"Iran (Islamic", 
"\"United Arab", 
"\"Occupied", 
"\"occupied Palestinian", 
"occupied Palestinian,",
"United States of,",
"\"United States of", 
"\"United States Virgin",
"\"Venezuela (Bolivarian", 
"\"United Republic of", 
"\"Bolivia (Plurinational", 
"Bolivia (Plurinational,",
"\"Saint Vincent and the",
"\"Central African",
"\"Democratic Republic",
"Saint Vincent and the," ]

namesOfDroppedRows = ["Total", 
"Unnamed", 
"Country", 
"Territory/Area", 
"confirmed",
"deaths", 
"Western Pacific Region,,,", 
"erritories**,,,", 
"European Region,,,", 
"European Region ^,",
"outh-East Asia Region,,,", 
"Mediterranean Region", 
"egion of the Americas,,,", 
"frican Region,,,", 
"Subtotal", 
"Grand total", 
"regions,,,", 
"conveyance,,", 
"Diamond Princess", 
"Islands,,,", 
"of the Congo,,,", 
"Tanzania,,,", 
"Republic,,,", 
"Republic of),,,", 
"Emirates,,,", 
"regions",
"Herzegovina,,,"]


#%% Import metadata to use
dfMetadataAll = pd.read_csv(metadataFile, sep=";", header=0, comment="#")
dfMetadataAll["ID"] = dfMetadataAll["File"].str.replace(startFileName,"").str.replace(endFileName.replace("csv","pdf"),"")

rawFiles = glob.glob(os.path.join(pathInputFile, startFileName+"*"+endFileName))

#%% Iterate through files.
for file in rawFiles:
    fileName = file.split(os.sep)[-1]
    
    if os.path.isfile(pathOutputFile+fileName):
        print("Skipping file as it was already processed: " + fileName)
        continue
    else:
        print("Processing file: " + fileName)

    with io.open(pathOutputFile+fileName, mode='w', encoding="utf-8") as outputFileObject:
        with io.open(file, mode='r', encoding="utf-8") as fileObject:
            prependNextLine = ""
            for line in fileObject:
                if any(region in line for region in list(namesOfMultilineRegions2)):
                    for key, value in namesOfMultilineRegions2.items():
                        if key in line:
                            prependNextLine = value
                    continue
                elif any(region in line for region in namesOfMultilineRegions):
                    prependNextLine = line.replace(',', '').replace('\n', ' ').replace('\r', '')
                    continue
                elif any(region in line for region in namesOfDroppedRows):
                    continue
                else:
                    if "Total" in prependNextLine:
                        pass
                    else:
                        line = prependNextLine+line.replace("conveyance","").replace("§","").replace(".","").replace("†","").replace("*","").replace("^","").replace("¶","").replace("[1]","").rstrip(',')
                        line = re.sub(r'([a-zA-Z])\s+([0-9])', r'\1,\2', line)
                        line = re.sub(r',,+', r',', line)
                        outputFileObject.write( line )

                    prependNextLine = ""
    
    # Date will be extracted from filename
    date = pd.to_datetime(fileName.split("-")[0])

    # Column Structure will be calculated sequentially based on the previous highest id's date
    fileId = fileName.replace(startFileName,"").replace(endFileName,"")
    dfMetadataTemp = dfMetadataAll[dfMetadataAll["ID"]<=fileId]
    dfMetadataTemp = dfMetadataTemp[dfMetadataTemp["ID"]==(dfMetadataTemp["ID"].max())].iloc[0]
    fileStructureId = dfMetadataTemp["Structure"]

    if fileStructureId == "N":
        namesColumns = ["Country", "Total confirmed cases", "New cases", "Total deaths", "Total new deaths", "Transmission classification", "Days since last reported case"]

    try:
        dfImported = pd.read_csv(pathOutputFile+fileName, skipinitialspace=True, header=None, skipfooter=0, encoding='utf-8', engine="python", index_col=False)
    except:
        try:
            dfImported = pd.read_csv(pathOutputFile+fileName, sep=";", skipinitialspace=True, header=None, skipfooter=0, encoding='utf-8', engine="python", index_col=False)
        except:
            dfImported = pd.read_csv(pathOutputFile+fileName, sep=" ", skipinitialspace=True, header=None, skipfooter=0, encoding='utf-8', engine="python", index_col=False)

    if len(dfImported.columns) == 1:
        dfImported = pd.read_csv(pathOutputFile+fileName, sep=";", skipinitialspace=True, header=None, encoding='utf-8', engine="python", index_col=False)

    # Find the columns where each value is null. Source: https://www.jitsejan.com/find-and-delete-empty-columns-pandas-dataframe.html
    empty_cols = [col for col in dfImported.columns if dfImported[col].isnull().all()]
    # Drop these columns from the dataframe
    dfImported.drop(empty_cols, axis=1, inplace=True)

    dfImported.rename(columns=dict(zip(dfImported.columns,namesColumns)), inplace=True)
    
    try:
        dfImported["Total confirmed cases"] = dfImported["Total confirmed cases"].str.replace(",","").astype('float64')
        dfImported.loc[dfImported["Total confirmed cases"].round() != dfImported["Total confirmed cases"], "Total confirmed cases"] = dfImported["Total confirmed cases"]*1000
    except AttributeError:
        pass

    dfImported.fillna(0, inplace=True)

    dfImported.rename(columns=dict(zip(dfImported.columns,namesColumns)), inplace=True)

    dfImported.insert(0, "Date", date.date(), allow_duplicates=False) 
    dfImported["Date"] = dfImported["Date"].astype(str)
    dfImported["Country"] = dfImported["Country"].astype(str)
    dfImported["Total confirmed cases"] = dfImported["Total confirmed cases"].astype('int64')
    dfImported["New cases"] = dfImported["New cases"].astype('int64')
    dfImported["Total deaths"] = dfImported["Total deaths"].astype('int64')

    #%% Write to file cleaned dataframe
    dfImported.to_csv(path_or_buf=pathOutputFile+fileName, index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")


# %%
