__author__ = 'petriau'
import urllib
import json
import datetime
from Tkinter import Tk, BOTH, Text, Menu, END
from ttk import Frame, Button, Style
import tkFileDialog
import csv

wateraid_currencies = ['BDT', 'ETB', 'GBP', 'GHS', 'INR', 'LRD', 'LSL', 'MGA', 'MWK', 'MZN', 'NGN', 'NPR', 'PKR','RWF', 'SLL',
                       'SZL','TZS', 'UGX', 'XOF', 'ZAR', 'ZMW', 'KES', 'USD']

window_width = 270
window_height = 140
rawdata = []

# TODO READ FILE INTO ARRAY
# TODO METHOD TO FIND LATEST RATES IN ARRAY
# TODO METHOD TO MAP RATES TO NEWDEA FORMAT

class Program(Frame):
    def __init__(self, parent):
        Frame.__init__(self,parent)

        self.parent = parent

        self.initUI()

    def initUI(self):
        self.parent.title("FX rate converter GAS to PC")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        fileButton = Button(self, text="Fetch rates from GAS rates file", command=self.onOpen)
        fileButton.place(x=20, y = 20)

        fetchButton = Button(self, text="Fetch rates from openexchangerates.org")
        fetchButton.place(x=20, y = 60)

        quitButton = Button(self, text="Quit", command=self.quit)
        quitButton.place(x=20, y=100)


    def onOpen(self):

        ftypes = [('CSVs', '*.csv')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        rawdata = self.readCSV(fl)
        a = 1

    def readCSV(self, filename):
        f = open(filename, 'r')
        reader = csv.reader(f)
        for row in reader:
            print row

    def readFile(self, filename):

        f = open(filename, "r")
        text = f.read()
        return text


def main():

    root = Tk()
    geom = str(window_width) + "x" + str(window_height) + "+300+300"
    root.geometry(geom)
    app = Program(root)
    root.mainloop()

if __name__ == '__main__':
    main()

# 1 is fetch from the internet, 2 is use a local file from GAS
case = 0

if case == 1:

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

    # Load from a dummy file if there is no internet connection
    except:
        f = file("testrates.json")
        rawdata = json.load(f)

if case == 2:

    # case 2
    # Load from the official WaterAid FX rates available from GAS

    # look at file, find latest rate
    rawdata = ""


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
    output_filename = "FX_output_to_PC_%s.csv" % datetime.datetime.now().strftime("%Y-%m")
    ofile = file(output_filename, 'w')
    for o in output:
        ofile.write(o+"\n")
    ofile.close()

