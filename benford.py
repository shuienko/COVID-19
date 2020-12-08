#!/usr/bin/env python3

import csv
import datetime
from scipy.stats import chisquare
from os import listdir
from os.path import isfile, join

EXPECTED_FREQ = [0.301, 0.176, 0.125, 0.097, 0.079, 0.067, 0.058, 0.051, 0.046]
REGIONS = [
    'Cherkasy Oblast',
    'Chernihiv Oblast',
    'Chernivtsi Oblast',
    'Crimea Republic*',
    'Dnipropetrovsk Oblast',
    'Donetsk Oblast',
    'Ivano-Frankivsk Oblast',
    'Kharkiv Oblast',
    'Kherson Oblast',
    'Khmelnytskyi Oblast',
    'Kiev',
    'Kiev Oblast',
    'Kirovohrad Oblast',
    'Luhansk Oblast',
    'Lviv Oblast',
    'Mykolaiv Oblast',
    'Odessa Oblast',
    'Poltava Oblast',
    'Rivne Oblast',
    'Sevastopol*',
    'Sumy Oblast',
    'Ternopil Oblast',
    'Vinnytsia Oblast',
    'Volyn Oblast',
    'Zakarpattia Oblast',
    'Zaporizhia Oblast',
    'Zhytomyr Oblast',
]
DATA_PATH = 'csse_covid_19_data/csse_covid_19_daily_reports'
START_DATE = '06-01-2020'
END_DATE = '12-07-2020'


def get_freq(list_of_strings):
    distribution = {str(i): 0 for i in range(1,10)}
    for item in list_of_strings:
        if str(item)[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            distribution[str(item)[0]] += 1

    distribution_normal = [0] * 9
    for i in range(9):
        distribution_normal[i] = float(distribution[str(i+1)])/len(list_of_strings)

    return distribution_normal

start_date_obj = datetime.datetime.strptime(START_DATE, '%m-%d-%Y')
end_date_obj = datetime.datetime.strptime(END_DATE, '%m-%d-%Y')
current_date_obj = start_date_obj

# inti data
data_dict = {}
for region in REGIONS:
    data_dict[region] = []

while current_date_obj <= end_date_obj:
    current_date = current_date_obj.strftime('%m-%d-%Y')
    with open(DATA_PATH + "/" + current_date + ".csv") as current_file:
        reader = csv.DictReader(current_file, delimiter=',')
        for line in reader:
            if line["Province_State"] in REGIONS:
                data_dict[line["Province_State"]] += [line["Confirmed"]]
    current_date_obj += datetime.timedelta(days=1)

data_dict_diff = {}
for region in REGIONS:
    data_dict_diff[region] = []

for region in data_dict:
    for i in range(len(data_dict[region]) - 1):
        data_dict_diff[region] += [int(data_dict[region][i+1]) - int(data_dict[region][i])]

for region in data_dict_diff:
    freq = get_freq(data_dict_diff[region])
    chi2 = chisquare(freq, f_exp=EXPECTED_FREQ)
    print("%25s | p-value = %0.3f" % (region, chi2[1]))
