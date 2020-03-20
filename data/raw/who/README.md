# DATA

## RAW Data
PDFs downloaded from https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports

@TODO: Automatic daily download.

### Structure
Given the evolution of the disease different structures of data where used in the PDFs.
We will focus on the countries data to simplify the problem.

#### Set Structure 1
These files show a mix of Countries and regions with the following structure:
Section: I. SURVEILLANCE
| WHO Region  | Country - Region  |  Total number of confirmed cases |
|---|---|---|
| Region 1 |  Abc | #  |
| Region n | Abc  |  # |
| Total cases  |   |  # |

Files with this structue:
 * 20200121-sitrep-1-2019-ncov

#### Set Structure 2
These files show a mix of Countries and regions with the following structure:
Section: I. SURVEILLANCE

| WHO Region  | Country | Region  |  Total number of confirmed cases |
|---|---|---|---|
| Region 1 |  China |  Total | #  |
| Region 1 |  Abc |  Abc | #  |
| Region n | Abc  |  Abc | # |
| Total cases  | Total  |  | # |

Files with this structue:
 * 20200122-sitrep-2-2019-ncov
 * 20200123-sitrep-3-2019-ncov
 * 20200124-sitrep-4-2019-ncov

 #### Set Structure 3
These files show a mix of Countries and regions with the following structure:
Section: I. SURVEILLANCE

| WHO Region  | Country | _Empty Column_  |  Confirmed Cases |
|---|---|---|---|
| Region 1 |  China |  Total | #  |
| Region 1 |  Abc |   | #  |
| Region n | Abc  |   | # |
| Total Confirmed cases  | Total  |  | # |

Files with this structue:
 * 20200125-sitrep-5-2019-ncov

#### Set Structure 4
These files show a mix of Countries and regions with the following structure:

Section: I. SURVEILLANCE

From report 12 onwards, additional table with China's regions only is also included, pushing countries data to be Table 3.

@TODO: Analyse China's regional data.

| WHO Region  | Country |  Confirmed Cases |
|---|---|---|
| Region 1 |  China*  | #  |
| Region 1 |  Abc  | #  |
| Region n | Abc   | # |
| Total Confirmed cases  | Total   | # |

Files with this structue:
 * 20200126-sitrep-6-2019--ncov
 * 20200127-sitrep-7-2019--ncov
 * 20200128-sitrep-8-ncov-cleared
 * 20200129-sitrep-9-ncov-v2
 * 20200130-sitrep-10-ncov
 * 20200131-sitrep-11-ncov
 * 20200201-sitrep-12-ncov
 * 20200202-sitrep-13-ncov-v3

#### Set Structure 5
With the raise of courntries and spread new columns appear detailing how many new cases versus previous report appear.
These files show a mix of Countries and regions with the following structure:

Section: I. SURVEILLANCE - Table 2

@TODO: Table structure, ( 7 columns)

Files with this structue:
 * 20200203-sitrep-14-ncov
 * @TODO: Analyse which files are like this.


 #### Set Structure N-1
Latest structure. Some tables are missing China's data as it is being reported separately with their regions. It should be included by does using this dataset.

Section: I. SURVEILLANCE - Table 2

| WHO Region / Country  | Total confirmed cases (new) | Total deaths (new) | Transmission classification | Days since last reported case |
| --- | --- | --- |  --- | --- |
| WHO Region n |  |  |  |  |
| Country n | # (#) | # (#)  | Abc | # |
| Grand total | # (#) | # (#)  |  |  |

Files with this structue:
 * @TODO: Analyse which files are like this.
 * 20200301-sitrep-41-covid-19


#### Set Structure N
Latest structure. Some tables are missing China's data as it is being reported separately with their regions. It should be included by does using this dataset.

Section: I. SURVEILLANCE - Table 2

| WHO Region / Country  | Total confirmed cases | Total confirmed new cases | Total deaths | Total new deaths | Transmission classification | Days since last reported case |
| --- | --- | --- | --- | --- | --- | --- |
| WHO Region n |  |  |  | |  |  |
| Country n | # | # | # | # | Abc | # |
| Grand total | # | # | # | # |  |  |

Files with this structue:
 * @TODO: Analyse which files are like this.
 * 20200302-sitrep-42-covid-19
 * 20200303-sitrep-43-covid-19
 * 20200304-sitrep-44-covid-19
 * 20200305-sitrep-45-covid-19
 * 20200306-sitrep-46-covid-19
 * 20200307-sitrep-47-covid-19
 * 20200308-sitrep-48-covid-19
 * 20200309-sitrep-49-covid-19
 * 20200310-sitrep-50-covid-19
 * 20200311-sitrep-51-covid-19
 * 20200312-sitrep-52-covid-19
 * 20200313-sitrep-53-covid-19
 * 20200314-sitrep-54-covid-19
 * 20200315-sitrep-55-covid-19
 * 20200316-sitrep-56-covid-19
 * 20200317-sitrep-57-covid-19