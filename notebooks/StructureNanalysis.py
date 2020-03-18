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

pathFile = "data/raw/20200302-sitrep-42-covid-19.pdf"

parsedFile = None
parsedFile = tabula.read_pdf(pathFile, lattice = False, multiple_tables=False, pages=[4,5])

#%%
dfFile = parsedFile[0]

#%% 