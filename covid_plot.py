#!/usr/bin/env python3
import csv
from git import Repo
import matplotlib.pyplot as plt
from argparse import ArgumentParser

git_dir = "COVID-19"
path = "csse_covid_19_data/csse_covid_19_time_series/"
filename = "time_series_19-covid-"

#global vars
data = []
header = []

# PARSE USER INPUT
def parse_user():
        parser = ArgumentParser(description="Plot the latest COVID-19 data based on country and province/state.")

        parser.add_argument("-np", "--no-plot", action='store_true', help="do not plot the data")
        parser.add_argument("-l", "--log", action='store_true', help="plot logarithmic axis")
        parser.add_argument("-f", "--file", help="print data to this file")
        parser.add_argument("-c", "--country", required=True, help="specify country as in data")
        parser.add_argument("-p", "--province", default="", help="specify province in the chosen country")
        parser.add_argument("-cy", "--category", default="confirmed", help="specify a category [confirmed, deaths,recovered]")

        return parser.parse_args()

# INIT ALL AROUND THE DATA REPO GIT AND ALL
def init_repo():
        repo = Repo(".")

        try:
                submodule = Repo(git_dir)
                current = submodule.head.commit
                print("Looking for updates...")
                submodule.remotes.origin.pull() ##Update Submodules
                if current != submodule.head.commit:
                        print("Updated data submodule.")
                else:
                        print("Data is up-to-date.")
        except:
                print("No data found. Initializing...")
                repo.submodule_update()
                print("Successfully initialized submodule.")

# GET ALL THE DATA FROM GIT REPO
def get_data(category, country, province):
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
def print_file(filepath):
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

        #if data[0] == "":
        #        save_file = data[1].replace(" ", "") + "_" + category + ".csv"
        #else:
        #        save_file = data[1].replace(" ", "") + "(" + province + ")" + "_" + category + ".csv"

        save_file = filepath

        with open(save_file, "w", newline="") as sfile:
                writer = csv.writer(sfile)
                writer.writerow(header)
                writer.writerow(data)
                writer.writerow(delta)
                writer.writerow(growth)
        print(f"Successfully wrote data to {save_file}.")

# PLOT ALL THE COVID DATA
def plot_data(plot_log, category):
        print("Preparing plot...")

        i = 4
        plot_data = []
        while i < len(data):
                plot_data += [int(data[i])]
                i += 1

        plt.figure("COVID-19 Plot")
        plt.plot(plot_data)
        if data[0] == "":
                plt.title(f"{category} in {data[1]}")
        else:
                plt.title(f"{category} in {data[0]}, {data[1]}")

        plt.xlabel(f"days since {header[4]} [mm/dd/yy]")
        plt.ylabel("number (cases)")
        if plot_log:
                plt.yscale('log')
        plt.show()
        print("Goodbye.")

def main():
        args = parse_user()
        #print(args.oof)
        
        init_repo()
        get_data(args.category.capitalize(), args.country, args.province)
        if args.file:
                print_file(args.file)
        if not args.no_plot:
                plot_data(args.log, args.category.capitalize())

main() #do stuff
