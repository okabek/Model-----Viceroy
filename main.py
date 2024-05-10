import re 
import requests
import datetime

msg = open("data.txt", "r").read()
lines = msg.splitlines()
datas = []
k = 5 # number of neighbours to check
api_key = "48df6a4e57bd409e8e4a6b983b8ed9a3"

##

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def find_nearest(score):
    nearest_profile = -1; 
    smallest_difference = 9999999999999

    for i in datas:
        sample_score = i["score"]
        abs_diff = abs(score - sample_score)

        if (abs_diff < smallest_difference):
            nearest_profile = i
            smallest_difference = abs_diff


    print("NEAREST SCORE = " + str(i["score"]))

    date_object = datetime.datetime.strptime(i["date"], "%d/%m/%Y")
    converted_date = date_object.strftime("%Y/%m/%d")
    next_date = (date_object + datetime.timedelta(days=1)).strftime("%Y/%m/%d")

    url = "https://api.twelvedata.com/time_series?start_date=" + converted_date + "&end_date=" + next_date + "&outputsize=96&symbol=EUR/USD&interval=15min&apikey=" + api_key
    request = requests.get(url)
    values = request["values"]

    date_object2 = datetime.datetime.strptime(i["time"], "%H:%M")
    converted_date2 = date_object.strftime("%H/%M")

    start_time = i["time"]
    stop_time = (date_object2 + datetime.timedelta(hours=1)).strftime("%H%M")
    start_price = -1
    end_price = -1 

    for i in values:
        dt = i["datetime"]
        dt2 = datetime.split(":")
        dt_time = dt2[0].split(" ")[1] + ":" + dt2[1]

        close = i["close"]

        if (dt_time == start_time):
            start_price = close

        elif (dt_time == stop_time):
            end_price = close      


    return(end_price - start_price) / start_price


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
        continue;


    actual = float(re.sub('\D', '', split[index]))
    forecast = float(re.sub('\D', '', split[index + 1]))
    previous = float(re.sub('\D', '', split[index + 2]))
    change = actual - previous 
    profile = {
        "date": split[0],
        "time": split[1],
        "actual": actual, 
        "previous": previous, 
        "change": change,
        "score": (actual + previous) * change
    }

    datas.append(profile)


forecast = find_nearest(-500)

print("PRICE MAY CHANGE BY " + str(forecast) + "%")
