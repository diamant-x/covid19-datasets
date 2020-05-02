#%% [markdown]
# # CSV Consolidation Country Region
# Creation date: 2020-03-23

#%% Imports
import pandas as pd # To work similar to R in Python
import csv #To load the tags metadatas
import os # To access the OS separator char.

#%% Constants Setup
inputFileList = ["data/processed/ita/ITA-COVID19_Regional.csv", "data/processed/deu/DEU-COVID19.csv", "data/processed/esp/ESP-COVID19.csv", "data/processed/fra/FRA-COVID19.csv", "data/processed/gbr/GBR-COVID19.csv"]
pathOutputFile = "data/processed/"

dfConsolidated = pd.DataFrame()

for file in inputFileList:
    fileName = file.split(os.sep)[-1]
    print("Processing file: " + fileName)

    dfImported = pd.read_csv(file, sep=",", skipinitialspace=True, header=0, encoding='utf-8', engine="python", index_col=False, quoting=csv.QUOTE_NONNUMERIC, parse_dates=["Date"], infer_datetime_format=True)
           
    dfImported = dfImported.groupby(["Date","Country","Region"], as_index=False).sum()
    # include the columns you want. Source: https://stackoverflow.com/a/51601986
    dfImported = dfImported[dfImported.columns[dfImported.columns.isin(["Date","Country","Region","Total confirmed cases", "New cases", "Total Hospital cases", "New Hospital cases", "Total ICU cases", "New ICU cases", "Total deaths", "New deaths", "Total cured", "New cured"])]]
   
    if dfConsolidated.size == 0:
        # No file loaded yet.
        dfConsolidated = dfImported
    else:
        dfConsolidated = dfConsolidated.append(dfImported, sort=False, ignore_index=True)

    print("Total records: " + str(dfConsolidated["Date"].size))

#%% Calculate new columns where Na
dfConsolidated["Current Hospital cases"] = 0

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
                dfConsolidated.loc[indexDate,["Current Hospital cases"]] = dfDate["Total Hospital cases"]

                if  (dfConsolidated.loc[indexDate,["New cases"]].all().sum() == 0) or (dfConsolidated.loc[indexDate,["New cases"]].isnull().values.any()):
                    dfConsolidated.loc[indexDate,["New cases"]] = dfConsolidated.loc[indexDate,["New cases"]] = dfDate["Total confirmed cases"]
                if  (dfConsolidated.loc[indexDate,["New Hospital cases"]].all().sum() == 0) or (dfConsolidated.loc[indexDate,["New Hospital cases"]].isnull().values.any()):
                    dfConsolidated.loc[indexDate,["New Hospital cases"]] = dfDate["Total Hospital cases"]
                if  (dfConsolidated.loc[indexDate,["New ICU cases"]].all().sum() == 0) or (dfConsolidated.loc[indexDate,["New ICU cases"]].isnull().values.any()):
                    dfConsolidated.loc[indexDate,["New ICU cases"]] = dfDate["Total ICU cases"]
                if  (dfConsolidated.loc[indexDate,["New deaths"]].all().sum() == 0) or (dfConsolidated.loc[indexDate,["New deaths"]].isnull().values.any()):
                    dfConsolidated.loc[indexDate,["New deaths"]] = dfDate["Total deaths"]
                if  (dfConsolidated.loc[indexDate,["New cured"]].all().sum() == 0) or (dfConsolidated.loc[indexDate,["New cured"]].isnull().values.any()):
                    dfConsolidated.loc[indexDate,["New cured"]] = dfDate["Total cured"]
            else:
                dfConsolidated.loc[indexDate,["Current Hospital cases"]] = dfDate["Total Hospital cases"].values-dfMaxDate["Total deaths"].values-dfMaxDate["Total cured"].values

                if  (dfConsolidated.loc[indexDate,["New cases"]].all().sum() == 0) or (dfConsolidated.loc[indexDate,["New cases"]].isnull().values.any()):
                    dfConsolidated.loc[indexDate,["New cases"]] = dfDate["Total confirmed cases"].values-dfMaxDate["Total confirmed cases"].values
                if  (dfConsolidated.loc[indexDate,["New Hospital cases"]].all().sum() == 0) or (dfConsolidated.loc[indexDate,["New Hospital cases"]].isnull().values.any()):
                    dfConsolidated.loc[indexDate,["New Hospital cases"]] = dfDate["Total Hospital cases"].values-dfMaxDate["Total Hospital cases"].values
                if  (dfConsolidated.loc[indexDate,["New ICU cases"]].all().sum() == 0) or (dfConsolidated.loc[indexDate,["New ICU cases"]].isnull().values.any()):
                    dfConsolidated.loc[indexDate,["New ICU cases"]] = dfDate["Total ICU cases"].values-dfMaxDate["Total ICU cases"].values
                if  (dfConsolidated.loc[indexDate,["New deaths"]].all().sum() == 0) or (dfConsolidated.loc[indexDate,["New deaths"]].isnull().values.any()):
                    dfConsolidated.loc[indexDate,["New deaths"]] = dfDate["Total deaths"].values-dfMaxDate["Total deaths"].values
                if  (dfConsolidated.loc[indexDate,["New cured"]].all().sum() == 0) or (dfConsolidated.loc[indexDate,["New cured"]].isnull().values.any()):
                    dfConsolidated.loc[indexDate,["New cured"]] = dfDate["Total cured"].values-dfMaxDate["Total cured"].values

#%% Fill empty cells with zeros.
dfConsolidated.fillna(0, inplace=True)

#%% Align data types.
# INT fields
intColumns = ["Total confirmed cases", "New cases", "Total Hospital cases", "New Hospital cases", "Current Hospital cases", "Total ICU cases", "New ICU cases", "Total deaths", "New deaths", "Total cured", "New cured"]
for column in intColumns:
    dfConsolidated[column] = dfConsolidated[column].astype('int64')

#%% Write to file consolidated dataframe
dfConsolidated.to_csv(path_or_buf=pathOutputFile+"ALL-COVID19_CountryRegion.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

print("Done.")