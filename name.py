import requests
from bs4 import BeautifulSoup
import pandas as pd

# girlname_norway = requests.get('https://www.ssb.no/statbank/table/10467/tableViewLayout1/')

# boysname_norway = requests.get('https://www.ssb.no/statbank/table/10467/tableViewLayout1/')

# denmark_names_2019 = requests.get('https://www.dst.dk/en/Statistik/emner/befolkning-og-valg/navne/navne-til-nyfoedte')


# # Må søke etter navn, kan ikke få en stor fin tabell. 
# sweden_names = requests.get('https://www.statistikdatabasen.scb.se/pxweb/en/ssd/START__BE__BE0001__BE0001D/BE0001Nyfodda/')

# excel file DL Sverige 'https://www.scb.se/en/finding-statistics/statistics-by-subject-area/population/general-statistics/name-statistics/#_Tablesandgraphs'


def read_excel(filename):
    return pd.read_excel(filename, dtype=str)


def get_dataset(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	castlist = []
	for td in soup.findAll('td', class_='character'):
		# Splitting on new line, and taking the 2. instance, which is where the names are
		name = td.text.split('\n')[1]
		# Removing the odd episode that comes in, this does not remove any chars
		if 'episode' not in name:
    		# Removing whitespaces, and adding to list	
			castlist.append(name.strip())

	return castlist
if __name__ == "__main__":
	
	pd.set_option('display.max_columns', 1000)
	pd.set_option('display.max_rows', 1000)

	
	castlist = get_dataset('https://www.imdb.com/title/tt0944947/fullcredits?ref_=tt_cl_sm#cast')
	
	sweden_girls = read_excel('sweden_girl_names.xlsx')
	sweden_boys = read_excel('sweden_boy_names.xlsx')

	norway_girls = read_excel('norway_girl_names.xlsx')
	norway_boys = read_excel('norway_boy_names.xlsx')
	print(sweden_girls["Girls' first names 1998-2019"])