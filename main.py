import json
import pprint
with open("./sample-weather-history.json","r") as weatherfile:
    weatherdata=json.load(weatherfile)

# print(len(weatherdata))
# pprint.pp(weatherdata[0])


# How many days of data do we have for each year?
years={}
for d in weatherdata:
    key=d["date"][0:4]
    if key in years:
        years[key]+=1
    else:
        years[key]=1
pprint.pp(years,width=5)

# Warmest day
warmday=max(weatherdata,key=lambda x: x["tmax"])
print(f"The warmest day was {warmday['date']} at {warmday['tmax']} degrees")

#Coldest day

coldday=min(weatherdata,key=lambda x: x["tmin"])
print(f"The coldest day was {coldday['date']} at {coldday['tmin']} degrees")

#How many days had snowfall
snowdays=[day for day in weatherdata if day["snow"]>0]
print(f'Snow fell on {len(snowdays)} days')
# pprint.pp(snowdays)

# using   creating a subset of the data for days that had snowfall
snowdays2=list(filter(lambda d:d["snow"]>0.0, weatherdata))
print(len(weatherdata))
print(len(snowdays2))


def is_summer_rain_day(d):
    summer_months=["-07-","-08-"] # cuz date is in the format 2017-01-02
    if any([m in d["date"] for m in summer_months]) and d["prcp"] >=1.0:
        return True
    return False

summer_rain_day=list(filter(is_summer_rain_day,weatherdata))
print(len(summer_rain_day))


#Challenge
def get_cold_windy_rainy_days():
    with open("./sample-weather-history.json","r") as weatherfile:
        weatherdata=json.load(weatherfile)

    def is_cold_windy_day(d):
        avg_temp=(d["tmax"]+d["tmin"])/2
        total_prcp=d["snow"]+d["prcp"]
        if avg_temp<45 and total_prcp>0.7 and d["awnd"]>=10.0:
            return True
        return False