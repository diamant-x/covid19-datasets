#%% [markdown]
# # CSV interim processing Fra cases
# Creation date: 2020-04-06

#%% Imports
import pandas as pd # To work similar to R in Python
import csv #To load the tags metadatas
import os # To access the OS separator char.

#%% Constants Setup
pathOutputFile = "data/processed/fra/"
outputFile = "FRA-COVID19.csv"

#%% Process Cases data
pathInputFile = "data/interim/fra/fra-covid19-tests-departement.csv"
file = pathInputFile
fileName = file.split(os.sep)[-1]
print("Processing file: " + fileName)
#% Import data.
dfCases = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, encoding='utf-8', parse_dates=["Date"], index_col=False)
#% Clean data.
dfCases = dfCases.loc[dfCases["Age"]=="Total"]

#%% Process Hospital data
pathInputFile = "data/interim/fra/fra-covid19-hospitalieres-departement.csv"
file = pathInputFile
fileName = file.split(os.sep)[-1]
print("Processing file: " + fileName)
#% Import data.
dfHospital = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, encoding='utf-8', parse_dates=["Date"], index_col=False)
#% Clean data.
dfHospital = dfHospital.loc[dfHospital["Genre"]=="Total"]

#%% Join data
dfImported = dfCases.merge(dfHospital, on=["Country", "Province ID", "Date", "Province", "Region"], how="outer")

#%% Clean data.
dfImported.drop(columns=["Province ID","Genre", "Age", "New tests Male", "New cases Male", "New tests Female", "New cases Female"], inplace=True)
dfImported.fillna(0, inplace=True)
dfImported.sort_values(by=["Date", "Country", "Region", "Province"], inplace=True)

#%% Calculate Total cases.
dfImported["Total Hospital cases"] = dfImported["Current Hospital cases"] + dfImported["Total cured"] + dfImported["Total deaths"]
dfImported["Total ICU cases"] = dfImported["Current ICU cases"]
dfImported['Total confirmed cases'] = dfImported.groupby("Province")['New cases'].transform(pd.Series.cumsum)

#for region in dfImported["Region"].unique():
#    dfRegion = dfImported[dfImported["Region"]==region]
#    for province in dfRegion["Province"].unique():
#        dfProvince = dfRegion[dfRegion["Province"]==province]
#        for date in dfProvince["Date"].unique():
#            dfDate = dfProvince[dfProvince["Date"]==date]
#            dfMaxDate = dfProvince[dfProvince["Date"]<date]
#            dfMaxDate = dfMaxDate[dfMaxDate["Date"]==dfMaxDate["Date"].max()]
#            
#            indexDate = dfDate.index
#            if dfMaxDate.size == 0:
#                # First date
#                dfImported.loc[indexDate,["Total confirmed cases"]] = dfDate["New confirmed cases"]
#            else:
#                dfImported.loc[indexDate,["Total confirmed cases"]] = dfDate["New confirmed cases"].values-dfMaxDate["Total confirmed cases"].values

#%% Adjust data types
dfImported[["New tests", "New cases", "Current Hospital cases", "Current ICU cases", "Total cured", "Total deaths", "Total Hospital cases", "Total ICU cases", "Total confirmed cases"]] = dfImported[["New tests", "New cases", "Current Hospital cases", "Current ICU cases", "Total cured", "Total deaths", "Total Hospital cases", "Total ICU cases", "Total confirmed cases"]].astype('int64')

#%% Reorder current columns
dfImported = dfImported[["Date", "Country", "Region", "Province", "New tests", "New cases", "Current Hospital cases", "Current ICU cases", "Total cured", "Total deaths", "Total Hospital cases", "Total ICU cases", "Total confirmed cases"]]

#%% Write to file consolidated dataframe
dfImported.to_csv(path_or_buf=pathOutputFile+outputFile, index=False, quoting=csv.QUOTE_NONNUMERIC)
print("Total raw records: " + str(dfImported["Date"].size))

print("Done.")