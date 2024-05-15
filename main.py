import numpy as np 
import requests
import sys
import time
import math 
import matplotlib.pyplot as plt
from scipy import stats
import torch
import torch.nn as nn

msg = open("data.txt", "r").read()
lines = msg.splitlines()
token = "66420cb84cae85.81165144"

##
# notes: 
# [PPI m/m] <-> [CPI m/m] = 0.7
# [CPI m/m] -> [Core PCE Price Index m/m] = 0.4
# [Non-Farm Employment Change] -> [ADP Non-Farm Employment Change] = 0.9
# [

class LinearRegressionModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(LinearRegressionModel, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)  

    def forward(self, x):
        out = self.linear(x)
        return out


def do_linear_regression(data_a, data_b):
    x_train = np.array(data_a, dtype=np.float32)
    x_train = x_train.reshape(-1, 1)

    y_train = np.array(data_b, dtype=np.float32)
    y_train = y_train.reshape(-1, 1)

    model = LinearRegressionModel(1, 1)
    criterion = nn.MSELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=.01)

    for epoch in range(200):
        epoch += 1

        inputs = torch.from_numpy(x_train).requires_grad_()
        labels = torch.from_numpy(y_train)

        optimizer.zero_grad() 
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()


    input = np.array([0.5], dtype=np.float32)
    input = x_train.reshape(-1, 1)
    predicted = model(torch.from_numpy(input).requires_grad_()).data.numpy()

    return predicted
    

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


def methods(data_a, data_b, r):
    # plt.scatter(data_a, data_b)
    # plt.show()

    long_run_a = data_a 
    long_run_b = data_b 
    
    del data_a[-(len(data_a) - 4):]
    del data_b[-(len(data_b) - 4):]

    short_run_a = data_a 
    short_run_b = data_b 

    sr_lr_a = do_linear_regression(short_run_a, short_run_b)
    sr_lr_b = do_linear_regression(long_run_a, long_run_b)

    print(sr_lr_a, sr_lr_b)


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
        methods(data_a, data_b, r)
    
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

