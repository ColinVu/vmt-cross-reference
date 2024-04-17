import json
import math

# Class representing each station's data
class StationData:
    def __init__(self, id, station_id, longitude, latitude, vmt):
        self.id = id
        self.station_id = station_id
        self.longitude = longitude
        self.latitude = latitude
        self.vmt = vmt

# Opening and Storing the contents of the JSON file
with open('vmt.json', 'r') as file:
    data = json.load(file)

station_data_list = []
for item in data['AADT_STANDARD_DATA_ExportTable']:
    vmt_list = [float(item['VMT2008']), float(item['VMT2009']), float(item['VMT2010']),
                float(item['VMT2011']), float(item['VMT2012']), float(item['VMT2013']),
                float(item['VMT2014']), float(item['VMT2015']), float(item['VMT2016']),
                float(item['VMT2017']), float(item['VMT2018']), float(item['VMT2019']),
                float(item['VMT2020']), float(item['VMT2021']), float(item['VMT2022'])]
    station_data = StationData(
        id=int(item['OBJECTID']),
        station_id=item['Station_ID'],
        longitude=float(item['Lat_Long_X']),
        latitude=float(item['Lat_Long_Y']),
        vmt=vmt_list
    )
    station_data_list.append(station_data)

# Entering information for the new point
new_lat = float(input("Enter latitude coordinate: "))
new_long = float(input("Enter longitude coordinate: "))
radius = float(input("Enter a radius for the VMT effect points (mi): "))
first_date = int(input("Enter begin date: "))
last_date = int(input("Enter last date: "))
weighted_sum_begin = 0.0
weighted_sum_end = 0.0
for item in station_data_list:
    lat_diff = new_lat - item.latitude
    long_diff = new_long - item.longitude
    dist = math.sqrt(pow(lat_diff, 2.) + pow(long_diff, 2.))
    if dist < (0.016992 * radius):
        print("distance: " + str(dist) + ", begin vmt: " + str(item.vmt[first_date-2008]) + ", end vmt: " + str(item.vmt[last_date-2008]))
        distance_weight = 0.5
        count = 0
        last = 0
        while count < 5:
            if (count == 4):
                weighted_sum_begin += 32. * 2. * item.vmt[first_date - 2008]
                weighted_sum_end += 32. * 2. * item.vmt[last_date - 2008]
                print("weight: " + str(32.) + ", weighted add: " + str(
                    32. * 2. * item.vmt[first_date - 2008]) + " " + str(
                    32. * 2. * item.vmt[last_date - 2008]))
                count = 5
                last = 1
            if dist > (0.016992 * distance_weight * radius or last == 0):
                weighted_sum_begin += (1.0/distance_weight) * 2. * item.vmt[first_date - 2008]
                weighted_sum_end += (1.0/distance_weight) * 2. * item.vmt[last_date - 2008]
                print("weight: " + str(1.0/distance_weight) + ", weighted add: " + str(
                    (1.0/distance_weight) * 2. * item.vmt[first_date - 2008]) + " " + str(
                    (1.0/distance_weight) * 2. * item.vmt[last_date - 2008]))
                count = 5
            count += 1
            distance_weight = 0.5 * distance_weight
weighted_sum_change = float(int((weighted_sum_end - weighted_sum_begin) * 100.)) / 100.
change_percent = float(int(((weighted_sum_end - weighted_sum_begin) / weighted_sum_begin) * 10000.)) / 100.
weighted_sum_begin = float(int(weighted_sum_begin * 100.)) / 100.
weighted_sum_end = float(int(weighted_sum_end * 100.)) / 100.
print("The NVMT begins at " + str(weighted_sum_begin) + " and ends at " + str(weighted_sum_end) + ". The change in NVMT is " + str(weighted_sum_change) + ", or " + str(change_percent) + "%.")