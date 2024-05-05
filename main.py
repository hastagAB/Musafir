import csv
import json
import os, sys
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(src_path)

from buddy import buddyData
from event.eventList import get_top_events_for_trip

def print_itinerary(trip_data, trip_id):
    for trip in trip_data:
        if trip['Trip ID'] == str(trip_id):
            print(f"Traveller Name: {trip['Traveller Name']}")
            print(f"Traveling from {trip['Departure City']} to {trip['Arrival City']}")
            print(f"Travel Dates: {trip['Departure Date']} to {trip['Return Date']}")
            break
    else:
        print(f"No trip found with Trip ID {trip_id}")

def read_trip_data(file_path):
    trip_data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            trip_data.append(row)
    return trip_data

def buddies(trip_id):
    json_data = buddyData(trip_id)
    return print(json_data)

def events(trip_id):
    json_data = get_top_events_for_trip(trip_id)
    return json_data
    


if __name__ == "__main__":
    file_path = "src/Dataset/hackupc-travelperk-dataset-extended.csv"
    trip_id = int(input("Enter the Trip ID: "))
    trip_data = read_trip_data(file_path)
    print_itinerary(trip_data, trip_id)
    buddies(trip_id)
    events(trip_id)
    
