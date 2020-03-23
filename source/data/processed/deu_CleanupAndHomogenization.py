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
pathInputFile = "data/interim/deu/"
pathOutputFile = "data/processed/deu/"
metadataFile = "data/raw/deu/tabulaParameters.csv"

startFileName = ""
endFileName = "-en.csv"

namesOfRegions = ["Baden-Württemberg","Bavaria","Berlin","Brandenburg","Bremen","Hamburg","Hesse","Mecklenburg-Western Pomerania","Lower Saxony","North Rhine-Westphalia","Rhineland-Palatinate","Saarlan","Saxony","Saxony-Anhalt","Schleswig-Holstein","Thuringia"]

#%% Import metadata to use
dfMetadataAll = pd.read_csv(metadataFile, sep=";", header=0, comment="#")
dfMetadataAll["ID"] = dfMetadataAll["File"].str.replace(startFileName,"").str.replace(endFileName.replace("csv","pdf"),"")

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
                    line = line.replace("+", "").replace("  "," ").replace("\"", "")
                    line = re.sub(r'\s([0-9])', r' \1', line)
                    line = "\"" + line
                    line = re.sub(r'([a-zA-Z])\s([0-9])', r'\1" \2', line)
                    line = re.sub(r'([a-zA-Z]);([0-9])', r'\1";\2', line)
                    line = re.sub(r'([a-zA-Z]);(")', r'\1";\2', line)
                    outputFileObject.write(line)
                else:
                    continue
 
    # Date will be extracted from filename
    date = pd.to_datetime(fileName.replace(startFileName,"").replace(endFileName,""))

    # Column Structure will be calculated sequentially based on the previous highest id's date
    fileId = fileName.replace(startFileName,"").replace(endFileName,"")
    dfMetadataTemp = dfMetadataAll[dfMetadataAll["ID"]<=fileId]
    dfMetadataTemp = dfMetadataTemp[dfMetadataTemp["ID"]==(dfMetadataTemp["ID"].max())].iloc[0]
    fileStructureId = dfMetadataTemp["Structure"]

    if fileStructureId == 5:
        namesColumns = ["Region", "Total confirmed cases", "New cases", "Population Incidence Ratio", "Total deaths"]

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

    try:
        dfImported.insert(2, "First", dfImported["New cases"].str.split(" ", expand=True)[0], allow_duplicates=False)
        dfImported.insert(3, "Last", dfImported["New cases"].str.split(" ", expand=True)[1], allow_duplicates=False)
  
        dfImported.drop("New cases", axis=1, inplace=True)
    except AttributeError:
        pass

    dfImported.fillna(0, inplace=True)

    dfImported.rename(columns=dict(zip(dfImported.columns,namesColumns)), inplace=True)

    dfImported.insert(0, "Date", date.date(), allow_duplicates=False) 
    dfImported["Date"] = dfImported["Date"].astype(str)
    dfImported["Region"] = dfImported["Region"].astype(str)
    dfImported["Total confirmed cases"] = dfImported["Total confirmed cases"].astype('int64')
    dfImported["New cases"] = dfImported["New cases"].astype('int64')
    dfImported["Population Incidence Ratio"] = dfImported["Population Incidence Ratio"].astype('float64')
    dfImported["Total deaths"] = dfImported["Total deaths"].astype('int64')

    #%% Write to file cleaned dataframe
    dfImported.to_csv(path_or_buf=pathOutputFile+fileName, index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")


# %%
