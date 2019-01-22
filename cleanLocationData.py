import config
import requests
import json

"""
To clean up user-defined locations collected in fccForum.js, feed locations to MapQuest API to obtain State and 
Country abbreviations, store each entry as a dictionary with the keys Rank, State, and Country.
"""
MAPQUEST_KEY = config.MAPQUEST_KEY_1
base_url = 'https://www.mapquestapi.com/geocoding/v1/address?key='

original_file = open("userData.csv", "r")
original_file.readline()  # Read headers first

all_locations = open("cleanedLocations.csv", "w")
all_locations.write("Rank,State,Country\n")

us_locations = open("US_cleanedLocations.csv", "w")
us_locations.write("Rank,State,Country\n")

for line in original_file:
    split_data = line.split(",", 1)
    user_rank = split_data[0]
    user_location = split_data[1].strip("\n")

    mapquest_call = requests.get(base_url + MAPQUEST_KEY + '&location=' + user_location)
    results = json.loads(mapquest_call.text)['results'][0]['locations'][0]
    state = results['adminArea3']
    country = results['adminArea1']

    all_locations.writelines(user_rank + "," + state + "," + country + "\n")

    if country == 'US':
        us_locations.writelines(user_rank + "," + state + "," + country + "\n")

original_file.close()
all_locations.close()
us_locations.close()

