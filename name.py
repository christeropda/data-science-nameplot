import requests
from bs4 import BeautifulSoup
import pandas as pd
from matplotlib import pyplot as plt

# girlname_norway = requests.get('https://www.ssb.no/statbank/table/10467/tableViewLayout1/')

# boysname_norway = requests.get('https://www.ssb.no/statbank/table/10467/tableViewLayout1/')

# denmark_names_2019 = requests.get('https://www.dst.dk/en/Statistik/emner/befolkning-og-valg/navne/navne-til-nyfoedte')


# # Må søke etter navn, kan ikke få en stor fin tabell. 
# sweden_names = requests.get('https://www.statistikdatabasen.scb.se/pxweb/en/ssd/START__BE__BE0001__BE0001D/BE0001Nyfodda/')

# excel file DL Sverige 'https://www.scb.se/en/finding-statistics/statistics-by-subject-area/population/general-statistics/name-statistics/#_Tablesandgraphs'


def read_excel(filename):
    return pd.read_excel(filename, dtype=str)


def get_dataset(url, limiter):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	castlist = []
	for td in soup.findAll('td', class_='character'):
		episode = td.text.split('\n')[2].strip().split(" ")[0]
		if '/ ...' in td.text:
			episode = td.text.split('\n')[3].strip().split(" ")[0]
			
		name = td.text.split('\n')[1]

		if int(episode) < limiter:
			break

		castlist.append(name.strip())

	
	return castlist

def split_and_remove_dup(names, blacklist):
	res = []
	
	for i in names:
		diff = i.split(" ")
		for j in diff:
			if j not in res and j not in blacklist:
				res.append(j)
	
	return res

def find_names_swe(filename, charlist):
	info = []
	
	with open(filename, "r") as f:
		data = f.readline()
		while(data):
			name = data.split(",")[0].strip()
			if name in charlist:
				info.append(data.strip("\n"))

			data = f.readline()

	return info

def find_names_nor(filename, charlist):
	info = []

	with open(filename, "r") as f:
		data = f.readline()
		while(data):
			name = data.split(";")[0].strip('"').strip()
			if name in charlist:
				info.append(data.strip("\n").strip('"').replace(";", ","))

			data = f.readline()
	

	return info

def plot(names, tit, start, fignum):
	years = list(range(1998,2020))
	numbers = []

	plt.figure(fignum)
	for i in names:
		name = i.strip('"').split(",")[0]
		chars = i.strip('"').replace("-", "0").replace(".", "0").split(",")[1:]

		j = 0	
		while j < len(chars):
			if '"' in chars[j]:
				appendthis = chars[j].strip('"') + chars[j+1].strip('"')
				print(appendthis)
				numbers.append(int(appendthis))
				j += 2
				continue

			numbers.append(int(chars[j]))
			j += 1

		plt.plot(years, numbers, label=name.strip('"'))

		numbers.clear()
		
	plt.legend(loc="upper left")
	plt.axvline(x=start)
	plt.title(tit)
	
if __name__ == "__main__":
	no_no_words = ["High", "The", "King", "Night", "Night's", 'Watch', "Officer", "Black", "Septa"]

	castlist_got = get_dataset('https://www.imdb.com/title/tt0944947/fullcredits?ref_=tt_cl_sm#cast', 3)
	castlist_skam = get_dataset('https://www.imdb.com/title/tt5288312/fullcredits?ref_=tt_cl_sm#cast', 20)
	castlist_wallander = get_dataset('https://www.imdb.com/title/tt0907702/fullcredits?ref_=tt_cl_sm#cast', 5)
	
	names_skam = split_and_remove_dup(castlist_skam, no_no_words)
	names_got = split_and_remove_dup(castlist_got, no_no_words)
	names_wallander = split_and_remove_dup(castlist_wallander, no_no_words)

	swe_got_girls = find_names_swe("sweden_girl_names.csv", names_got)
	swe_got_boys = find_names_swe("sweden_boy_names.csv", names_got)

	nor_got_girls = find_names_nor("norway_girl_names.csv", names_got)
	nor_got_boys = find_names_nor("norway_boy_names.csv", names_got)


	swe_skam_girls = find_names_swe("sweden_girl_names.csv", names_skam)
	swe_skam_boys = find_names_swe("sweden_boy_names.csv", names_skam)

	nor_skam_girls = find_names_nor("norway_girl_names.csv", names_skam)
	nor_skam_boys = find_names_nor("norway_boy_names.csv", names_skam)


	swe_wallander_girls = find_names_swe("sweden_girl_names.csv", names_wallander)
	swe_wallander_boys = find_names_swe("sweden_boy_names.csv", names_wallander)

	nor_wallander_girls = find_names_nor("norway_girl_names.csv", names_wallander)
	nor_wallander_boys = find_names_nor("norway_boy_names.csv", names_wallander)


	plot(swe_got_girls, "Game of Thrones, girl baby names in Sweeden born after 1998", 2011, 1)
	plot(swe_got_boys, "Game of Thrones, boy baby names in Sweeden born after 1998", 2011, 2)

	plot(nor_got_girls, "Game of Thrones, girl baby names in Norway born after 1998", 2011, 3)
	plot(nor_got_boys, "Game of Thrones, boy baby names in Norway born after 1998", 2011, 4)

	plot(swe_skam_girls, "Skam, girl baby names in Sweeden born after 1998", 2015, 5)
	plot(swe_skam_boys, "Skam, boy baby names in Sweeden born after 1998", 2015, 6)

	plot(nor_skam_girls, "Skam, girl baby names in Norway born after 1998", 2015, 7)
	plot(nor_skam_boys, "Skam, boy baby names in Norway born after 1998", 2015, 8)


	plot(swe_wallander_girls, "Wallander, girl baby names in Sweeden born after 1998", 2008, 9)
	plot(swe_wallander_boys, "Wallander, boy baby names in Sweeden born after 1998", 2008, 10)

	plot(nor_wallander_girls, "Wallander, girl baby names in Norway born after 1998", 2008, 11)
	plot(nor_wallander_boys, "Wallander, boy baby names in Norway born after 1998", 2008, 12)

	plt.show()
	plt.close()

