import re 
import requests
import datetime

msg = open("data.txt", "r").read()
lines = msg.splitlines()
datas = []
k = 5 # number of neighbours to check
api_key = "exAhOWAEye9oRcIEn3qX"

##

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def find_nearest(type, score):
    nearest_profile = -1; 
    smallest_difference = 9999999999999

    for i in datas:
        sample_score = i["change"]
        abs_diff = abs(score - sample_score)
        if (abs_diff < smallest_difference and i["type"] == type):
            nearest_profile = i
            smallest_difference = abs_diff


    print(nearest_profile)

    date_object = datetime.datetime.strptime(nearest_profile["date"], "%d/%m/%Y")
    current_date = date_object.strftime("%Y-%m-%d")
    next_date = (date_object + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    url = "https://marketdata.tradermade.com/api/v1/historical?api_key=" + api_key + "&currency=EURUSD&date=" + current_date
    request = requests.get(url).json()
    start_price = request["quotes"][0]["close"]

    url = "https://marketdata.tradermade.com/api/v1/historical?api_key=" + api_key + "&currency=EURUSD&date=" + next_date
    request = requests.get(url).json()
    end_price = request["quotes"][0]["close"]

    return round((end_price - start_price) / start_price, 5)


##

for i in lines:
    split = i.split()

    if (len(split) <= 1 or split[2] != "USD" or split[3] != "H"):
        continue;


    type = split[4] + " " + split[5] 
    index = 5

    for i2 in range(len(split) - 5): 
        if (has_numbers(split[index])):
            break; 


        index += 1 


    if (len(split) < index + 3):
        continue


    actual = float(re.sub('\D', '', split[index]))
    forecast = float(re.sub('\D', '', split[index + 1]))
    previous = float(re.sub('\D', '', split[index + 2]))

    profile = {
        "type": type,
        "date": split[0],
        "time": split[1],
        "actual": actual, 
        "previous": previous, 
        "change": actual - previous
    }

    datas.append(profile)


#

type = "Unemployment Claims"
actual = 231 
predicted = 212 
forecast = find_nearest(type, actual - predicted)

print("Expected change of " + str(-forecast) + "%" + " For the USD")
