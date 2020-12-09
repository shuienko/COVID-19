#!/usr/bin/env python3

import csv
import datetime
from scipy.stats import chisquare,chi2
from os import listdir
from os.path import isfile, join

EXPECTED_FREQ = [0.3010, 0.1761, 0.1249, 0.0969, 0.0792, 0.0669, 0.0580, 0.0512, 0.0458]
# Every chi2 values less than CRITICAL_CHI2_VALUE covers 99% of results with 8 degrees of freedom
# If chi2 is more than CRITICAL_CHI2_VALUE then it is likely a fake
CRITICAL_CHI2_VALUE = chi2.ppf(0.99, 8)
print("CRITICAL_CHI2_VALUE = ", CRITICAL_CHI2_VALUE)

DATA_PATH = 'csse_covid_19_data/csse_covid_19_daily_reports'
START_DATE = '06-01-2020'
END_DATE = '12-07-2020'


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
    'Zhytomyr Oblast'
]

def get_freq(list_of_strings):
    distribution = {str(i): 0 for i in range(1, 10)}
    skipped = 0
    for item in list_of_strings:
        if str(item)[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            distribution[str(item)[0]] += 1
        else:
            skipped += 1

    distribution_normal = [0] * 9
    for i in range(9):
        distribution_normal[i] = float(distribution[str(i+1)])

    return distribution_normal, skipped

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
    freq, skipped = get_freq(data_dict_diff[region])
    freq_str = ["%2.0d" % i for i in freq]
    expected_freq = [i * (len(data_dict_diff[region]) - skipped) for i in EXPECTED_FREQ]
    expected_freq_str = ["%2.0f" % i for i in expected_freq]

    chi2 = chisquare(freq, f_exp=expected_freq)
    print("%25s | %s | chi2 = %0.5f" % (region, freq_str , chi2[0]))
    if chi2[0] > CRITICAL_CHI2_VALUE:
        result = 'Fake'
    else:
        result = 'True'
    print("%82s | result = %s\n" % (expected_freq_str, result) )


