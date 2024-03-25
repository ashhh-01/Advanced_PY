import json
import pprint
import copy # to avoid changing original dataset
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
dataset=list(filter(lambda d:d["snow"]>0.0, weatherdata))
print(len(weatherdata))
print(len(dataset))


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
    
    blustery_day=list(filter(is_cold_windy_day,weatherdata))
    return blustery_day


#sorting (using snowy days data) -> gives a new dataset

sorted_data=sorted(dataset, key=lambda d:d["snow"],reverse=True)
# pprint.pp(sorted_data)

# Modifies the dataset
dataset.sort(key=lambda d:d["snow"],reverse=False)
# pprint.pp(dataset)

#Multiple Fields (Tuple)
sorted_data2=sorted(dataset, key=lambda d:(d["snow"],d["awnd"]))
# pprint.pp(sorted_data2)

#Data Transformation using Map function
def toC(f):
    f=0 if f is None else f
    return (f-32)*5/9
def toMM(i):
    i=0 if i is None else i 
    return i*25.4

def toKPH(s):
    s=0 if s is None else s
    return s*1.60934

def toMetric(wd):
    new_wd = copy.copy(wd)
    new_wd["tmin"]=toC(wd["tmin"])
    new_wd["tmax"]=toC(wd["tmax"])
    new_wd["prcp"]=toMM(wd["prcp"])
    new_wd["snow"]=toMM(wd["snow"])
    new_wd["snwd"]=toMM(wd["snwd"])
    new_wd["tmin"]=toKPH(wd["awnd"])
    return new_wd



#Map iterater
metric_weather=list(map(toMetric,weatherdata))
# pprint.pp(weatherdata[0])
# pprint.pp(metric_weather[0])

#using map to convert objects to tuple
avg_temp=lambda t1,t2:(t1+t2)/2.0
tuple_data=list(map(lambda d:(d["date"],avg_temp(d["tmax"],d["tmin"])),weatherdata))
pprint.pp(tuple_data[0:5])


#challenge
def get_day_temp_descriptions():
    with open("./sample-weather-history.json", "r") as weatherfile:
        weatherdata=json.load(weatherfile)

    def avgerage_temp_to_desc(day_data):
        avg_temp=(day_data["tmin"]+day_data["tmax"])/2
        desc=""
        if avg_temp<=60:
            desc="cold"
        elif avg_temp>60 and avg_temp<80:
            desc="warm"
        else:
            desc="hot"
        return (day_data["date"],desc)
        
    new_data=list(map(avgerage_temp_to_desc,weatherdata))
    return new_data