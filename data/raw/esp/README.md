# DATA

## RAW Data
PDFs downloaded from https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm

*Missing reports from weekend days 14-15th March.*

### Structure
Given the evolution of the disease different structures of data where used in the PDFs.

#### Set Structure 1
Early files don't have tables and data is provided in free text.

Files with this structue:
 * Actualizacion_31_COVID-19
 * Actualizacion_32_COVID-19
 * Actualizacion_33_COVID-19
 * Actualizacion_34_COVID-19


#### Set Structure 2
These files show the following structure:
Tabla 2. Casos COVID-19 e incidencia acumulada por Comunidades autónomas en España.

| CCAA  | Total casos | Casos/Poblacion (100.000h) 
|---|---|---|
| Region n  | # | # |
| Total     | # | # |

Files with this structue:
 * Actualizacion_35_COVID-19

#### Set Structure 3
These files show the following structure:
Tabla 1. Casos COVID-19 e incidencia acumulada por Comunidades autónomas en España, 04.03.2020.

| CCAA  | Total casos | Casos/Poblacion (100.000h) | Ingresos en UCI | Fallecidos
|---|---|---|---|---|
| Region n  | # | # | # | # |
| Total     | # | # | # | # |

Files with this structue:
 * Actualizacion_36_COVID-19
 * Actualizacion_37_COVID-19
 * Actualizacion_38_COVID-19
 * Actualizacion_39_COVID-19
 * Actualizacion_40_COVID-19
 * Actualizacion_41_COVID-19 * A partir de aquí Casos/Poblacion de los ultimos 14 dias solo.
 * Actualizacion_42_COVID-19
 * Actualizacion_43_COVID-19
 * Actualizacion_46_COVID-19
 * Actualizacion_47_COVID-19
 * Actualizacion_48_COVID-19
 * Actualizacion_49_COVID-19
 * Actualizacion_50_COVID-19

 #### Set Structure 4
These files show the following structure:
Tabla 1. Casos COVID-19 e incidencia acumulada por Comunidades autónomas en España, 04.03.2020.

| CCAA  | Total casos | Casos/Poblacion (100.000h) | Hospitalizados | Ingresos en UCI | Fallecidos | Nuevos
|---|---|---|---|---|---|---|
| Region n  | # | # | # | # | # | # |
| Total     | # | # | # | # | # | # |

Files with this structue:
From:
 * Actualizacion_51_COVID-19
To:
 * Actualizacion_52_COVID-19

#### Set Structure 5
These files show the following structure:
Tabla 1. Casos COVID-19 e incidencia acumulada por Comunidades autónomas en España, 04.03.2020.

| CCAA  | Total casos | Casos/Poblacion (100.000h) | Hospitalizados | Ingresos en UCI | Fallecidos | Curados | Nuevos
|---|---|---|---|---|---|---|---|
| Region n  | # | # | # | # | # | # | # |
| Total     | # | # | # | # | # | # | # |

Files with this structue:
From:
 * Actualizacion_53_COVID-19
To: