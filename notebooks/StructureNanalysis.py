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