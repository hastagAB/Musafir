import csv
import json
import os, sys
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(src_path)

from buddy import buddyData
from event.eventList import get_top_events_for_trip
from flight.flight_details import get_top_3_fastest_flights
from attraction.attraction import attractions

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
    
def flight(trip_id):
    top_3_flights = get_top_3_fastest_flights(trip_id)
    return top_3_flights

def topAttractions(city:str):
    top_5_places = attractions(city)
    return top_5_places



if __name__ == "__main__":
    file_path = "src/dataset/hackupc-travelperk-dataset-extended.csv"
    trip_id = int(input("Enter the Trip ID: "))
    with open(file_path, 'r') as file:
        for row in csv.DictReader(file):
            if int(row['Trip ID']) == trip_id:
                destination_city = row['Arrival City']
                break
        else:
            destination_city = None
    trip_data = read_trip_data(file_path)
    print_itinerary(trip_data, trip_id)
    # Get and print buddies
    print("Buddies for Trip ID", trip_id, ":")
    buddies(trip_id)
    
    # Get and print top events
    print("Top events for Trip ID", trip_id, ":")
    events(trip_id)
    
    # Get and print top 3 fastest flights
    print("Top 3 fastest flights for Trip ID", trip_id, ":")
    top_flights = flight(trip_id)
    print(top_flights)
    
    # Get and print top attractions
    print("Top attractions for destination city", destination_city, ":")
    topAttractions(destination_city)
    
