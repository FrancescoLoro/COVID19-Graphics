# COVID19-Graphics

Simple script to draw a diagram of most notable values about COVID-19 spread in Italy.

#### USAGE: 
- Clone the repository

- Launch `main.sh` to get information about whole Italy 

- Launch `main.sh -r RegionName` to get information about particular region

```
usage: main.sh [-h] [-r REGION]

optional arguments:
  -h, --help            show this help message and exit
  -r REGION, --region REGION
                        Region to be shown. Valid options are: abruzzo,
                        basilicata, calabria, campania, emilia-romagna,
                        friuli_venezia_giulia, lazio, liguria, lombardia,
                        marche, molise, piemonte, puglia, sardegna, sicilia,
                        toscana, umbria, valle_d_aosta, veneto, bolzano_trento
```

#### SYSTEM REQUIREMENTS:
- git
- python3

#### REQUIRED PYTHON PACKAGES: 
- pandas
- numpy
- matplotlib

To install them using `pip`, run:
```
python3 -m pip install -r requirements.txt
```
