import math, csv, datetime

file = open('/Users/karthikj/Documents/CS194/project/seattle/static/police_stations.csv')
crime_file = open('/Users/karthikj/Documents/CS194/project/seattle/static/police_calls_cleaned.csv')
fire_file = open('/Users/karthikj/Documents/CS194/project/seattle/static/fire_calls_cleaned.csv')
neighborhood_map = open('/Users/karthikj/Documents/CS194/project/seattle/static/neighborhood_map.csv')

output_file = open('/Users/karthikj/Documents/CS194/project/seattle/static/crime_counts.csv', 'wb')
fire_output = open('/Users/karthikj/Documents/CS194/project/seattle/static/fire_counts.csv', 'wb')
fire_day_of_week = open('/Users/karthikj/Documents/CS194/project/seattle/static/fire_day.csv', 'wb')
crime_day_of_week = open('/Users/karthikj/Documents/CS194/project/seattle/static/crime_day.csv', 'wb')

#the csv writers that we are outputing too

crimeWriter = csv.writer(output_file, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
crimeWriter.writerow(['location', 'distance', 'crime_count'])

fireWriter = csv.writer(fire_output, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
fireWriter.writerow(['location', 'distance', 'crime_count'])

fireDateWriter = csv.writer(fire_day_of_week, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
fireDateWriter.writerow(['type', 'dayOfWeek', 'distance', 'count'])


crimeDateWriter = csv.writer(crime_day_of_week, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
crimeDateWriter.writerow(['type', 'dayOfWeek', 'distance', 'count'])


crime_locations = []
fire_locations = []
#new_police = []
police_stations = []
fire_stations = []
crime_counts = {}
fire_counts = {}
count = 100


#get the counts for crime rates and fire rate per location (not per day of the week also)
for line in crime_file:
    args = line.split(',')
    crime_loc = args[-1].split()
    if (crime_loc[0] != 'Location'):
        crime_tuple = (float(crime_loc[0]),float(crime_loc[1]))
        crime_locations.append(crime_tuple)

#get the counts for fire rates per location
for line in fire_file:
    args = line.split(',')
    fire_loc = args[-1].split()
    if (len(fire_loc)!= 0 and fire_loc[0] != 'Location'):
	fire_tuple = (float(fire_loc[0]), float(fire_loc[1]))
	fire_locations.append(fire_tuple)

#add to the police stations array each of the locations for the police stations
for line in file:
    args = line.split(',')
    long_lat = args[1].split()
    if (long_lat[0] != 'Location'):
        police_stations.append((float(long_lat[0]), float(long_lat[1])))

#add to the fire stations array each of the locations for the fire stations
for line in neighborhood_map:
    args = line.split(',')
    if (args[0] == "Fire Stations"):
	fire_stations.append((float(args[-1]), float(args[-2])))
    #elif args[0] == "Police Precincts":
    #	new_police.append((float(args[-1]), float(args[-2])))

#figure out distance of crime to nearest police station
distance = 'inf'  
crime_distances = {} 
for crime in crime_locations:
    if crime not in crime_distances:
        for police in police_stations:
            new_dist = math.sqrt((crime[0] - police[0])**2 + (crime[1] - police[1])**2)
            if (new_dist < distance):
                distance = new_dist
        crime_distances[crime] = distance
    distance = 'inf'

#figure out distance of fire to nearest fire station
distance = 'inf'  
fire_distances = {} 
for fire in fire_locations:
    if fire not in fire_distances:
        for police in fire_stations:
            new_dist = math.sqrt((fire[0] - police[0])**2 + (fire[1] - police[1])**2)
            if (new_dist < distance):
                distance = new_dist
        fire_distances[fire] = distance
    distance = 'inf'
crime_file = open('/Users/karthikj/Documents/CS194/project/seattle/static/police_calls_cleaned.csv')

#figure out the day of the week that the crime happened
for line in crime_file:
    args = line.split(',')
    crime_loc = args[-1].split()
    if (crime_loc[0] != 'Location'):
        event_date = args[-2].split('/')
        day = datetime.date(int(event_date[2]), int(event_date[0]), int(event_date[1])).weekday()
        crime_tuple = (float(crime_loc[0]),float(crime_loc[1]))
        distance = crime_distances[crime_tuple]
        uber_crime_tuple = (args[0], day, distance)
        if uber_crime_tuple in crime_counts:
            crime_counts[uber_crime_tuple] = crime_counts[uber_crime_tuple] + 1
        else:
            crime_counts[uber_crime_tuple] = 1

fire_file = open('/Users/karthikj/Documents/CS194/project/seattle/static/fire_calls_cleaned.csv')

#figure out the day of the week the fire happened
for line in fire_file:
    args = line.split(',')
    fire_loc = args[-1].split()
    if (len(fire_loc)!= 0 and fire_loc[0] != 'Location'):
        event_date = args[-2].split('/')
        day = datetime.date(int(event_date[2]), int(event_date[0]), int(event_date[1])).weekday()
	fire_tuple = (float(fire_loc[0]), float(fire_loc[1]))
	distance =fire_distances[fire_tuple]
        uber_fire_tuple = (args[0], day, distance)
        if uber_fire_tuple in fire_counts:
            fire_counts[uber_fire_tuple] = fire_counts[uber_fire_tuple]+1
        else:
            fire_counts[uber_fire_tuple] = 1

for key in crime_counts.iterkeys():
    crimeDateWriter.writerow([key[0], key[1], key[2], crime_counts[key]])
for key in fire_counts.iterkeys():
    fireDateWriter.writerow([key[0], key[1], key[2], fire_counts[key]])
