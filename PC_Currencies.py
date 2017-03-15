__author__ = 'petriau'
import urllib
import json
import datetime
import csv


# case 1
# For fetching fresh currency rates from openexchangerates.org
app_id = "5d0e402206304a3cadc3a6c0cf8926a1"
rawdate = str(datetime.date.today())
today = rawdate[-2:]+"/"+rawdate[-5:-3]+"/"+rawdate[0:4]

def fetchCurrencyData(url):
    url = urllib.urlopen(url)
    result = url.read()
    #print result
    return json.loads(result)

try:
    rawdata = fetchCurrencyData("https://openexchangerates.org/api/latest.json?app_id=%s" % app_id)

# Load from file if there is no internet connection
except:
    f = file("testrates.json")
    rawdata = json.load(f)

# case 2
# Load from the official WaterAid FX rates available from GAS

# Leave out USD since it's the base currency
wateraid_currencies = ['BDT', 'ETB', 'GBP', 'GHS', 'INR', 'LRD', 'LSL', 'MGA', 'MWK', 'MZN', 'NGN', 'NPR', 'PKR','RWF', 'SLL',
                       'SZL','TZS', 'UGX', 'XOF', 'ZAR', 'ZMW', 'KES']

baserates = {}

output = []
# do base currency to all other currencies (USD)
for i in wateraid_currencies:
    baserates[i] = (rawdata['rates'][i])
    print baserates[i]
    print i
    o = '%s, %s, %s, %s, %s' % ('USD', i, baserates[i], today, "Yes")
    output.append(o)

# do remaining currencies between each other, inversions not needed
a = 0
while a < len(wateraid_currencies):
    b = a + 1
    while b < len(wateraid_currencies):
        # find index instead of dict name
        c = baserates[wateraid_currencies[b]] / baserates[wateraid_currencies[a]]
        o = '%s, %s, %s, %s, %s' % (wateraid_currencies[a], wateraid_currencies[b], c, today, "Yes")
        output.append(o)
        b += 1
    a += 1

print output
# print into csv

ofile = file("output.csv", 'w')
for o in output:
    ofile.write(o+"\n")
ofile.close()

