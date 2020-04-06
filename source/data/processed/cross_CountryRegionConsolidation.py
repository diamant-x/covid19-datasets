#%% [markdown]
# # CSV Consolidation Country Region
# Creation date: 2020-03-23

#%% Imports
import pandas as pd # To work similar to R in Python
import csv #To load the tags metadatas
import os # To access the OS separator char.

#%% Constants Setup
inputFileList = ["data/processed/ita/ITA-COVID19_Regional.csv", "data/processed/deu/DEU-COVID19.csv", "data/processed/esp/ESP-COVID19.csv", "data/processed/fra/FRA-COVID19.csv"]
pathOutputFile = "data/processed/"

dfConsolidated = pd.DataFrame()

for file in inputFileList:
    fileName = file.split(os.sep)[-1]
    print("Processing file: " + fileName)

    # Date will be calculated sequentially based on the previous highest id's date.    
    if dfConsolidated.size == 0:
        # No file loaded yet.
        namesColumns = ["Date","Country","Region","Total confirmed cases", "Total Hospital cases", "Total ICU cases", "Total deaths", "Total cured"]
        dfConsolidated = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)
        dfConsolidated = dfConsolidated.groupby(["Date","Country","Region"], as_index=False).sum()

    else:
        try:
            namesColumns = ["Date","Country","Region","Total confirmed cases", "Total Hospital cases", "Total ICU cases", "Total deaths", "Total cured"]
            dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)
            dfImported = dfImported.groupby(["Date","Country","Region"], as_index=False).sum()
        except ValueError:
            namesColumns = ["Date","Country","Region","Total confirmed cases","Total deaths"]
            dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0,usecols=namesColumns, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC)
            dfImported = dfImported.groupby(["Date","Country","Region"], as_index=False).sum()

        dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)

    print("Total records: " + str(dfConsolidated["Date"].size))

#%% Fill empty cells with zeros.
dfConsolidated.fillna(0, inplace=True)

#%% Calculate new cases and new deaths.
dfConsolidated["New confirmed cases"] = 0
dfConsolidated["Current Hospital cases"] = 0
dfConsolidated["New Hospital cases"] = 0
dfConsolidated["New ICU cases"] = 0
dfConsolidated["New deaths"] = 0
dfConsolidated["New cured"] = 0

for country in dfConsolidated["Country"].unique():
    print("Calculating columns for country: " + country)
    dfCountry = dfConsolidated[dfConsolidated["Country"]==country]
    for region in dfCountry["Region"].unique():
        dfRegion = dfCountry[dfCountry["Region"]==region]
        for date in dfRegion["Date"].unique():
            dfDate = dfRegion[dfRegion["Date"]==date]
            dfMaxDate = dfRegion[dfRegion["Date"]<date]
            dfMaxDate = dfMaxDate[dfMaxDate["Date"]==dfMaxDate["Date"].max()]

            indexDate = dfDate.index
            if dfMaxDate.size == 0:
                # First date
                dfConsolidated.loc[indexDate,["New confirmed cases"]] = dfDate["Total confirmed cases"]
                dfConsolidated.loc[indexDate,["New Hospital cases"]] = dfDate["Total Hospital cases"]
                dfConsolidated.loc[indexDate,["Current Hospital cases"]] = dfDate["Total Hospital cases"]
                dfConsolidated.loc[indexDate,["New ICU cases"]] = dfDate["Total ICU cases"]
                dfConsolidated.loc[indexDate,["New deaths"]] = dfDate["Total deaths"]
                dfConsolidated.loc[indexDate,["New cured"]] = dfDate["Total cured"]
            else:
                dfConsolidated.loc[indexDate,["New confirmed cases"]] = dfDate["Total confirmed cases"].values-dfMaxDate["Total confirmed cases"].values
                dfConsolidated.loc[indexDate,["New Hospital cases"]] = dfDate["Total Hospital cases"].values-dfMaxDate["Total Hospital cases"].values
                dfConsolidated.loc[indexDate,["Current Hospital cases"]] = dfDate["Total Hospital cases"].values-dfMaxDate["Total deaths"].values-dfMaxDate["Total cured"].values
                dfConsolidated.loc[indexDate,["New ICU cases"]] = dfDate["Total ICU cases"].values-dfMaxDate["Total ICU cases"].values
                dfConsolidated.loc[indexDate,["New deaths"]] = dfDate["Total deaths"].values-dfMaxDate["Total deaths"].values
                dfConsolidated.loc[indexDate,["New cured"]] = dfDate["Total cured"].values-dfMaxDate["Total cured"].values

#%% Align data types.
dfConsolidated["Total confirmed cases"] = dfConsolidated["Total confirmed cases"].astype('int64')
dfConsolidated["New confirmed cases"] = dfConsolidated["New confirmed cases"].astype('int64')
dfConsolidated["Total Hospital cases"] = dfConsolidated["Total Hospital cases"].astype('int64')
dfConsolidated["New Hospital cases"] = dfConsolidated["New Hospital cases"].astype('int64')
dfConsolidated["Current Hospital cases"] = dfConsolidated["Current Hospital cases"].astype('int64')
dfConsolidated["Total ICU cases"] = dfConsolidated["Total ICU cases"].astype('int64')
dfConsolidated["New ICU cases"] = dfConsolidated["New ICU cases"].astype('int64')
dfConsolidated["Total deaths"] = dfConsolidated["Total deaths"].astype('int64')
dfConsolidated["New deaths"] = dfConsolidated["New deaths"].astype('int64')
dfConsolidated["Total cured"] = dfConsolidated["Total cured"].astype('int64')
dfConsolidated["New cured"] = dfConsolidated["New cured"].astype('int64')


#%% Write to file consolidated dataframe
dfConsolidated.to_csv(path_or_buf=pathOutputFile+"ALL-COVID19_CountryRegion.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")