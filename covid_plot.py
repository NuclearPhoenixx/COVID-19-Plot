#!/usr/bin/env python3
import csv
from git import Repo
import matplotlib.pyplot as plt

git_dir = "COVID-19-DATA"
path = "csse_covid_19_data/csse_covid_19_time_series/"
filename = "time_series_19-covid-"

#### USER INPUT ####
category =	"Confirmed" # [Confirmed, Deaths, Recovered]
country = 	"mainland china" # Choose an available country
province = 	"" # Specify a province or blank to get the whole country
file = 		False #true or false to save all data to a file
plot =		True #true or false to plot the data
#### ---------- ####


#global vars
repo = []
data = []
header = []

# INIT ALL AROUND THE DATA REPO GIT AND ALL
def init_repo():
	global repo
	try:
		repo = Repo(git_dir)
		current = repo.head.commit
		print("Looking for updates...")
		repo.remotes.origin.pull()
		if current != repo.head.commit:
			print("Updated data repo.")
		else:
			print("Data repo is up-to-date.")
	except:
		print("No data repo found, cloning...")
		repo = Repo.clone_from("https://github.com/CSSEGISandData/COVID-19.git", git_dir)
		print("Successfully cloned repo.")

# GET ALL THE DATA FROM GIT REPO
def get_data():
	global data
	global header

	file = git_dir + "/" + path + filename + category + ".csv"
	print("Preparing data...")
	with open(file) as ofile:
		csv_reader = csv.reader(ofile, delimiter=",")
		line_count = 0
		for row in csv_reader:
			if line_count == 0:
				header = row #f"Column names are {', '.join(row)}"
			else:
				if country.lower() == row[1].lower():
					if province.lower() == "":
						if len(data) == 0:
							data = row
							data[0] = ""
						else:
							i = 4
							while i < len(row):
								data[i] = int(data[i]) + int(row[i])
								i += 1
					elif province.lower() in row[0].lower():
						data = row
						#for row_content in row:
						#print(row_content)

			line_count += 1

	if len(data) > 0:
		print("Done grabbing data.")
	else:
		print("Country and/or province not available!")
		quit()

# PRINT ALL (NEW) DATA TO CSV FILE
def print_file():
	print("Preparing file...")
	delta = [] #List with all the changes
	n = 0 #starts really at 3, the first four entries are region, country, lat/longitude; the fith one is just the start, no delta
	while n < len(data):
		if n <= 4:
			delta += [""]
		else:
			dN = int(data[n]) - int(data[n-1])
			delta += [dN]
		n += 1

	growth = []
	n = 0
	while n < len(data):
		if n <= 5 or delta[n-1] == 0:
			growth += [""]
		else:
			exp = int(delta[n]) / int(delta[n-1])
			growth += [exp]
		n += 1

	if data[0] == "":
		save_file = data[1].replace(" ", "") + "_" + category + ".csv"
	else:
		save_file = data[1].replace(" ", "") + "(" + province + ")" + "_" + category + ".csv"

	with open(save_file, "w", newline="") as sfile:
		writer = csv.writer(sfile)
		writer.writerow(header)
		writer.writerow(data)
		writer.writerow(delta)
		writer.writerow(growth)
	print(f"Successfully wrote data to {save_file}.")

# PLOT ALL THE COVID DATA
def plot_data():
	print("Preparing plot...")
	i = 4
	plot_data = []
	while i < len(data):
		plot_data += [int(data[i])]
		i += 1

	plt.plot(plot_data)
	if data[0] == "":
		plt.title(f"{category} in {data[1]}")
	else:
		plt.title(f"{category} in {data[0]}, {data[1]}")
	plt.xlabel(f"days since {header[4]} [mm/dd/yy]")
	plt.ylabel("number (cases)")
	plt.show()
	print("Goodbye.")

def main():
	init_repo()
	get_data()
	if file:
		print_file()
	if plot:
		plot_data()

main() #do stuff
