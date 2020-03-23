#!/usr/bin/env python3
import csv
from git import Repo
import matplotlib.pyplot as plt
from argparse import ArgumentParser

git_dir = "COVID-19"
path = "csse_covid_19_data/csse_covid_19_time_series/"
filename = "time_series_19-covid-"

#global vars
data = {}
header = []

# PARSE USER INPUT
def parse_user():
        parser = ArgumentParser(description="Plot the latest COVID-19 data based on country and province/state.")

        parser.add_argument("-np", "--no-plot", action='store_true', help="do not plot the data")
        parser.add_argument("-l", "--log", action='store_true', help="plot logarithmic axis")
        parser.add_argument("-f", "--file", help="print data to this file")
        parser.add_argument("-c", "--country", required=True, action="append", help="specify country as in data. If you provide multiple country flags this will go into comparison mode.")
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
                                header = row
                        else:
                                for c in country:
                                        if c in data:
                                                data_buffer = data[c]
                                        else:        
                                                data_buffer = []
                                        
                                        if c.lower() == row[1].lower():
                                                if province == "":
                                                        if len(data_buffer) == 0:
                                                                data_buffer = row
                                                                data_buffer[0] = ""
                                                        else:
                                                                i = 4
                                                                while i < len(row):
                                                                        data_buffer[i] = int(data_buffer[i]) + int(row[i])
                                                                        i += 1
                                                elif province.lower() in row[0].lower():
                                                        data_buffer = row

                                                data[c.lower()] = data_buffer

                        line_count += 1

        if len(data) > 0:
                print("Done grabbing data.")
        else:
                print("Country and/or province not available!")
                quit()

# PRINT ALL (NEW) DATA TO CSV FILE
def print_file(filepath):
        print("Preparing file...")

        delta = {}
        growth = {}

        for key in data:
                delta[key] = [] #List with all the changes
                n = 0 #starts really at 3, the first four entries are region, country, lat/longitude; the fith one is just the start, no delta
                while n < len(data[key]):
                        if n <= 4:
                                delta[key] += [""]
                        else:
                                dN = int(data[key][n]) - int(data[key][n-1])
                                delta[key] += [dN]
                        n += 1

                growth[key] = []
                n = 0
                while n < len(data[key]):
                        if n <= 5 or delta[key][n-1] == 0:
                                growth[key] += [""]
                        else:
                                exp = int(delta[key][n]) / int(delta[key][n-1])
                                growth[key] += [exp]
                        n += 1

        #if data[0] == "":
        #        save_file = data[1].replace(" ", "") + "_" + category + ".csv"
        #else:
        #        save_file = data[1].replace(" ", "") + "(" + province + ")" + "_" + category + ".csv"

        save_file = filepath

        with open(save_file, "w", newline="") as sfile:
                writer = csv.writer(sfile)
                writer.writerow(header)
                for key in data:
                        writer.writerow(data[key])
                        writer.writerow(delta[key])
                        writer.writerow(growth[key])
        print(f"Successfully wrote data to {save_file}.")

# PLOT ALL THE COVID DATA
def plot_data(plot_log, category):
        print("Preparing plot...")

        plt.figure("COVID-19 Plot")

        for key in data:
                i = 4
                plot_data = []
                while i < len(data[key]):
                        plot_data += [int(data[key][i])]
                        i += 1

                plt.plot(plot_data, label=f"{key.capitalize()}")

        i = 0
        string = f"{category} in "
        for key in data:
                if i > 0:
                        string += " vs "

                if data[key][0] == "":
                        string += f"{key.capitalize()}"
                else:
                        string += f"{data[key][0]}, {key.capitalize()}"
                i += 1

        plt.title(string)

        plt.legend()
        plt.xlabel(f"days since {header[4]} [mm/dd/yy]")
        plt.ylabel("number (cases)")
        if plot_log:
                plt.yscale('log')
        plt.show()
        
        print("Goodbye.")

def main():
        args = parse_user()

        if len(args.country) > 1 and not args.province == "":
                print("Comparing countries ONLY. Please delete province input.")
                return
        
        init_repo()
        get_data(args.category.capitalize(), args.country, args.province)
        if args.file:
                print_file(args.file)
        if not args.no_plot:
                plot_data(args.log, args.category.capitalize())

main() #do stuff
