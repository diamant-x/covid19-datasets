# DATA

## RAW Data
PDFs downloaded from https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html

### Structure
Given the evolution of the disease different structures of data where used in the PDFs.

#### Set Structure 1
Early files don't have tables and data is provided in free text.

| Federal state | Number of cases | New cases Today |
|---|---|---|
|Abc|#|#|

Files with this structue:
 * 2020-03-04-en
 * 2020-03-05-en

#### Set Structure 2
Similar to 1 but an additional columns

| Federal state | Number of cases | New cases Today | Special areas
|---|---|---|---|
|Abc|#|#|Abc|

Files with this structue:
From:
 * 2020-03-06-en
To:
 * 2020-03-09-en

#### Set Structure 3
Previous samples where manually collected byt he government. Now they request automatical processing.

| Federal state | Number of cases | From which, electronically processed |
|---|---|---|
|Abc|#|#|

Files with this structue:
 * 2020-03-10-en
 * 2020-03-11-en

#### Set Structure 4
Previous samples where manually collected byt he government. Now they request automatical processing.

| Federal state | Number of cases | From which, electronically processed | Population Incidence Ratio |
|---|---|---|---|
|Abc|#|#|#|
|Total|#|#|#|

Files with this structue:
From:
 * 2020-03-12-en
To:
 * 2020-03-16-en

#### Set Structure 5
First reports with detailed deaths reported

| Federal state | Total confirmed cases | New cases | Population Incidence Ratio | Total deaths |
|---|---|---|---|---|
|Abc|#|+#|#|#|
|Total|#|#|#|#|

Files with this structue:
From:
 * 2020-03-17-en
To:
