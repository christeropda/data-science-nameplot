import requests

girlname_norway = requests.get('https://www.ssb.no/statbank/table/10467/tableViewLayout1/')

boysname_norway = requests.get('https://www.ssb.no/statbank/table/10467/tableViewLayout1/')

denmark_names_2019 = requests.get('https://www.dst.dk/en/Statistik/emner/befolkning-og-valg/navne/navne-til-nyfoedte')


# Må søke etter navn, kan ikke få en stor fin tabell. 
sweden_names = requests.get('https://www.statistikdatabasen.scb.se/pxweb/en/ssd/START__BE__BE0001__BE0001D/BE0001Nyfodda/')