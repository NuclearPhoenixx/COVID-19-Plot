# COVID-19-Plot

This small script automatically downloads all the latest COVID-19 data from the [2019 Novel Coronavirus COVID-19 (2019-nCoV) Data Repository by Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19), lets you choose a country and/or province and plots the data for you. Additionally, you can also save a csv file with the chosen data and some more info (see below).


## Install

You need Python 3 for this to work.

Download script, install all the dependencies via ```pip3 install -r requirements.txt``` and then simply run it with ```python3 covid_plot.py```.

## Config

At the moment the only way to change the config is to edit the file. This will be updated, don't worry.

Head to the ```#### USER INPUT ####``` section and edit the parameters to your wishes. Notes:

- You can choose from 3 categories: Confirmed cases [Confirmed], deaths [Deaths] and recoveries [Recovered].
- Countries and provinces are taken directly from the data csv and in order to get the correct datapoint you have to know the exact country name as in the csv and at least part of the province name (not case sensitive). Example: Looking for `China` will result in an error, instead look for `Mainland China` (again, not case sensitive). Have a look at these files: [COVID-19 time series](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series)
- You can choose to print the data results to a csv file like the original data file. Additionally you will also get the following info:
  - Third line: Day-to-day delta of cases.
  - Fourth line: Ratio of delta(day n)/delta(day n-1)
- You can also choose to plot the data.

## To Do

- Add nice user input arguments
- Remove gitpython and add the data repo as submodule (!)
