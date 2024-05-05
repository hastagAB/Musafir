import pandas as pd
import requests
from datetime import datetime
from tqdm import tqdm

def get_flight_details(departure_date):
    url = "https://sky-scanner3.p.rapidapi.com/flights/search-one-way"

    querystring = {
        "fromEntityId": "eyJlIjoiOTU1NjUwODUiLCJzIjoiQkNOIiwiaCI6IjI3NTQ4MjgzIn0=",
        "toEntityId": "eyJlIjoiOTU2NzM3NDQiLCJzIjoiTlVFIiwiaCI6IjI3NTQ1MTYyIn0=",
        "departDate": departure_date.strftime('%Y-%m-%d')  
    }

    headers = {
        "X-RapidAPI-Key": "160495a7edmshe8043ba129e3fd6p10e807jsn5beeaa98ab4b",
        "X-RapidAPI-Host": "sky-scanner3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    return data

def get_top_3_fastest_flights(trip_id):
    df = pd.read_csv("src/dataset/hackupc-travelperk-dataset-extended.csv")

    trip_row = df[df['Trip ID'] == trip_id]

    if len(trip_row) == 0:
        return "Trip ID not found"

    departure_date_str = trip_row['Departure Date'].values[0]
    departure_date = datetime.strptime(departure_date_str, '%d/%m/%Y')

    flight_details = get_flight_details(departure_date)

    if flight_details['data'] is None:
        return "No flight details available"

    data_list = flight_details['data']['itineraries']

    sorted_flights = sorted(data_list, key=lambda x: x['legs'][0]['durationInMinutes'])

    top_3_flights = []
    for item in sorted_flights[:3]:
        flight_info = {
            "Origin": item['legs'][0]['origin']['name'],
            "Destination": item['legs'][0]['destination']['name'],
            "Flight Name": item['legs'][0]['segments'][0]['marketingCarrier']['name'],
            "Flight Number": item['legs'][0]['segments'][0]['flightNumber'],
            "Time Taken (minutes)": item['legs'][0]['durationInMinutes'],
            "Departure Time": item['legs'][0]['departure'],
            "Arrival Time": item['legs'][0]['arrival'],
            "Price": item['price']['formatted']
        }
        top_3_flights.append(flight_info)

    formatted_output = ""
    for i, flight in enumerate(top_3_flights):
        formatted_output += f"Flight {i+1}:\n"
        for key, value in flight.items():
            formatted_output += f"{key}: {value}\n"
        if i < 2:
            formatted_output += "\n"  
    return formatted_output


