import json
import pprint
import random 

with open("./sample-weather-history.json","r") as weatherfile:
    weatherdata=json.load(weatherfile)

#Generate random floating point
    
# print(random.random())

# #within a range
# print(random.randint(10,20)) #Will include both ends
# print(random.randrange(10,20)) #Excludes both the ends


def is_summerday(d):
    summer_months=["2019-07-","2019-08-"]
    if any([m in d["date"] for m in summer_months]):
        return True
    return False
summer_2019=list(filter(is_summerday, weatherdata))
random.seed(10)
random_days=[]
for _ in range(5):
    random_days.append(summer_2019[random.randrange(len(summer_2019))])

# print(max(random_days,key=lambda d:d["awnd"]))

month_data=weatherdata[0:3]
random.shuffle(month_data)


# rnd_day=random.choice(month_data)
# print(rnd_day)
# print("----------------")
# rnd_days=random.choices(month_data,k=3)
# print(rnd_days)

rnd_days=random.sample(month_data,k=3)
# print(rnd_days)

#Challenge
def select_days(year,month):
    yearmonth=year+"-"+month
    def yearmonthfilter(day):
        if yearmonth in day["date"]:
            return True
        return False
    yearmonthdata=list(filter(yearmonthfilter,weatherdata))
    datalist=random.sample(yearmonthdata,k=5)
    return datalist

# print(select_days("2019","02"))

import statistics
summers=["-06-","-07-","-08-"]
summer_months=[d for d in weatherdata if any([month in d["date"] for month in summers])]
print(f"Data for {len(summer_months)} summer days")

#mean of min and max for summer day

max_temps=[d["tmax"] for d in summer_months]
min_temps=[d["tmin"] for d in summer_months]

print( max_mean:= statistics.mean(max_temps)) ## new to python neednt declare the variable separately (:=) it calculates and assigns the values
print( min_mean:= statistics.mean(min_temps)) 
# print(statistics.median(max_temps))
# print(statistics.median(min_temps))


upper_outlier =max_mean +(statistics.stdev(max_temps)*2)
lower_outlier =min_mean +(statistics.stdev(min_temps)*2)
print(upper_outlier)
print(lower_outlier)

max_outliers= [t for t in max_temps if t>= upper_outlier]
min_outliers= [t for t in min_temps if t<= lower_outlier]

print(max_outliers)
print(min_outliers)

def count_days():
    def avg_temp(days):
        return (days["tmin"] +days["tmax"])/2
    winters=["-12-","-01-","-02-"]
    winter_month=[d for d in weatherdata if any([month in d["date"] for month in winters])]
    avg_temp=[avg_temp(day) for day in winter_month]
    avg_mean=statistics.mean(avg_temp)

    outlier_temp=avg_mean+statistics.stdev(avg_temp)
    outliers=[day for day in winter_month if avg_temp(day)>=outlier_temp]
    return len(outliers)
