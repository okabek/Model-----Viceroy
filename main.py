import numpy as np 
import requests
import sys
import time
import math 
from scipy import stats

msg = open("data.txt", "r").read()
lines = msg.splitlines()
token = "66420cb84cae85.81165144"

##
# notes: 
# [PPI m/m] <-> [CPI m/m] = 0.7
# [CPI m/m] -> [Core PCE Price Index m/m] = 0.4
# [Non-Farm Employment Change] -> [ADP Non-Farm Employment Change] = 0.9
# [

def type_write(txt, length):
  txt = txt + "\n"

  for char in txt:
      sys.stdout.write(char)
      sys.stdout.flush()

      time.sleep(length)


def is_number(inputString):
    output = ''.join(c for c in inputString if c.isdigit() or c == '-' or c == '.')
    numeric = False 

    try:
        output = float(output)
        numeric = True 

    except: 
        None 

    
    return numeric


def forecast(name1, name2, r):
    r = 2


def test(name1, name2):
    data_a = []
    data_b = []

    for i in lines:
        split = i.split()

        if (len(split) <= 1 or split[2] != "USD"):
            continue


        type = split[4] 
        index = 5

        for i2 in range(len(split) - 5): 
            data = split[index]

            if (is_number(data) and data != "Composite-20"):
                break


            type = type + " " + split[index]
            index += 1 


        if (len(split) < index + 3):
            continue


        actual = split[index]
        forecast = split[index + 1]
        previous = split[index + 2]

        actual = float(''.join(c for c in actual if c.isdigit() or c == '-' or c == '.'))
        forecast = float(''.join(c for c in forecast if c.isdigit() or c == '-' or c == '.'))
        previous = float(''.join(c for c in previous if c.isdigit() or c == '-' or c == '.'))
  
        if (type == name1 and len(data_a) == len(data_b)):
            data_a.append(actual)

        elif (type == name2 and len(data_a) == len(data_b) + 1):
            data_b.append(actual)


    if (len(data_a) > len(data_b)):
        data_a.pop()

    elif (len(data_b) > len(data_b)):
        data_b.pop()


    print("\nTesting using a 5% significance level...")
    
    r = np.corrcoef(data_a, data_b)[0][1]
    n = len(data_a)
    df = n - 2
    t = r / math.sqrt((1 - r * r) / df)
    p = 1 - stats.t.cdf(t, df)
    
    if (p < 0.05):
        type_write(name1 + " and " + name2 + " are correlated.", .05)
        type_write("r = " + str(r), .05)
        type_write("Running forecast algorithm...", .05)
        forecast(name1, name2, r)
    
    else: 
        type_write("There is no correlation between X and Y", .05)
    
##

art = open("art.txt", 'r').readlines()

for i in art:
    print(i)

    time.sleep(.1)


print("\n\n\n\n")
type_write("MODEL | VICEROY", .05)
type_write("Forecasting the value of indicator [a] based on indicator [b]", .05)
print("\n\n")

##

type = input("Enter the name of the 'to forecast' indicator: ")
type2 = input("Enter the name of the 'to compare' indicator: ")
forecast = test(type2, type)

