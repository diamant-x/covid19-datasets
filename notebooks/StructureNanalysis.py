#%% [markdown]
# Creation date: 2020-03-18
# ## Notebook setup

#%%
import pandas as pd # To work similar to R in Python
import numpy # To access pi number definition.
import csv #To load the tags metadatas
import glob #To be able to dynamically load files matching pattern.
import os # To access the OS separator char.
import tabula # To scan OCR PDFs.

#%%

pathFile = "data/raw/esp/Actualizacion_52_COVID-19.pdf"

parsedFile = None
parsedFile = tabula.read_pdf(pathFile, lattice = False, stream = False, multiple_tables=False, pages=1, relative_area=True, area=[40,0,100,100])

#%%
dfFile = parsedFile[0]
dfFile
#%% 
dfImported = pd.read_csv("data/processed/who/20200305-sitrep-45-covid-19.csv", sep=",", skipinitialspace=True, header=0, encoding='utf-8', engine="python", index_col=False, dtype ={"Date":str,"Country":str,"Total confirmed cases":'int64',"Total deaths":'int64'})
# Date will be extracted from filename
date = pd.to_datetime("20200305-sitrep-45-covid-19.csv".split("-")[0])
dfImported.insert(0, "Date", date.date(), allow_duplicates=False) 
dfImported["Date"] = dfImported["Date"].astype(str)
#Save
dfImported.to_csv("data/processed/who/20200305-sitrep-45-covid-19.csv", index=False, quoting=csv.QUOTE_NONNUMERIC)

# %%
