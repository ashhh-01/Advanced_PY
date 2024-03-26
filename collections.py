import json
import pprint
from collections import defaultdict

with open("./sample-weather-history.json","r") as weatherfile:
    weatherdata=json.load(weatherfile)

#Provides default value and neednt check keys exist
years=defaultdict(int) #defaut values gonna be integers if they dont exist
for d in weatherdata:
    key=d["date"][0:4]
    years[key]+=1
# pprint.pp(years)

years_months=defaultdict(list)
for d in weatherdata:
    key=d["date"][0:7]
    years_months[key].append(d)
# print(len(years_months))
    
def warmest_day(month):
    wd=max(month,key=lambda d:d["tmax"])
    return (wd["date"],wd["tmax"])
def coldest_day(month):
    cd=min(month,key=lambda d:d["tmin"])
    return (cd["date"],cd["tmin"])

# for year_month, daylist in years_months.items():
#     print(f"Warmest day in {year_month}:{warmest_day(daylist)}")
#     print(f"Coldest day in {year_month}:{coldest_day(daylist)}")


#Reduce fn -> takes call back -> lambda fn and data and inital value
#Take the total dataset and reduce it to a single value

from functools import reduce
#how much total snowfall in total dataset
total_snowfall=reduce(lambda acc, elem: acc+elem["snow"],weatherdata,0) # Initial value of accumulator 
total_prcp=reduce(lambda acc, elem: acc+(elem["snow"]+elem["prcp"]),weatherdata,0)
print(total_prcp)
print(total_snowfall)

#warmest day tmax and snow>0
def warm_snow_day(acc,elem):
    return elem if elem["snow"]>0 and elem["tmax"]> acc ["tmax"] else acc

starting_val={
    "date":"1900-01-01",
    "tmin":0,
    "tmax":0,
    "prcp":0.0,
    "snow":0.0,
    "snwd":0.0,
    "awnd":0.0
}

result =reduce(warm_snow_day,weatherdata,starting_val)
print(f"{result['date']} with temp {result['tmax']} and snow {result['snow']} ")

#Grouping -> Needs sorted data
from itertools import groupby
year=[day for day in weatherdata if "2022" in day ["date"]]
year.sort(key=lambda d:d["prcp"])
datagroup=defaultdict(list)
for d in year:
    datagroup[d["prcp"]].append(d["date"])
# print(f"{len(datagroup)} total precipiation groups")
# pprint.pp(datagroup)


grouped={k: list(v) for k,v in groupby(year,key=lambda d:d["prcp"])}
# print(f"{len(grouped)} total precipitation groups")
# for key,data in grouped.items():
#     print(f"Precip:{key}, #days :{len(data)}, Days:{list(map(lambda d:d['date'],data))}")


#Working with dates
from datetime import date, timedelta

dateobj=date.fromisoformat(weatherdata[0]["date"])
print(dateobj)
print(dateobj.weekday())

def is_weekend_day(d):
    day=date.fromisoformat(d["date"])
    return (day.weekday()==5 or day.weekday()==6)

weekenddays=list(filter(is_weekend_day,weatherdata))
warmest_day=max(weekenddays,key=lambda d:d["tmax"])
# print(weekenddays)
print(date.fromisoformat(warmest_day["date"]).strftime("%a, %d, %b, %Y"))

coldest_day=min(weatherdata,key=lambda d:d["tmin"])
coldest_date=date.fromisoformat(coldest_day["date"])
print(f"The coldest day of the year was {str(coldest_date)} {coldest_day['tmin']}")

avg_temp=0.0
next_date=coldest_date

for _ in range(7):
    next_date+=timedelta(days=1)
    wd=next((day for day in weatherdata if day["date"]==str(next_date)),None)
    avg_temp+=(wd["tmin"]+wd["tmax"])/2

avg_temp=avg_temp/7
print(f"The average temp for the next 7 days was {avg_temp}")


#challenge
def miserable_day():
    result=reduce(day_rank, weatherdata)

def misery_score(day):
    wind=0 if day["awnd"] is None else day["awnd"]
    temp=day["tmax"]*0.8
    rain=day["prcp"]*10

    score=(temp +rain +wind)/3
    return score

def day_rank(acc,elem):
    return acc if misery_score(acc)>=misery_score(elem) else elem
