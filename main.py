import csv
import json
import os, sys
from datetime import datetime
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(src_path)

from buddy import buddyData
from event.eventList import get_top_events_for_trip
from flight.flight_details import get_top_3_fastest_flights
from attraction.attraction import attractions
from hotels.hotel import Hotels

def print_itinerary(trip_data, trip_id, content):
    for trip in trip_data:
        if trip['Trip ID'] == str(trip_id):
            content.append(Paragraph(f"<b>Traveller Name:</b> {trip.get('Traveller Name', '')}", styles['Normal']))
            content.append(Paragraph(f"<b>Traveling from:</b> {trip.get('Departure City', '')} to {trip.get('Arrival City', '')}", styles['Normal']))
            content.append(Paragraph(f"<b>Travel Dates:</b> {trip.get('Departure Date', '')} to {trip.get('Return Date', '')}", styles['Normal']))
            print(f"Traveller Name: {trip.get('Traveller Name', '')}")
            print(f"Traveling from: {trip.get('Departure City', '')} to {trip.get('Arrival City', '')}")
            print(f"Travel Dates: {trip.get('Departure Date', '')} to {trip.get('Return Date', '')}")
            break
    else:
        content.append(Paragraph(f"No trip found with Trip ID {trip_id}", styles['Normal']))
        print(f"No trip found with Trip ID {trip_id}")

def buddies(trip_id, content):
    json_data = buddyData(trip_id)
    content.append(Paragraph(f"<b>Buddies for Trip ID {trip_id}:</b>", styles['Heading1']))
    content.append(Paragraph(json_data, styles['Normal']))
    print(f"Buddies for Trip ID {trip_id}:")
    print(json_data)

def events(trip_id, content):
    json_data = get_top_events_for_trip(trip_id)
    content.append(Paragraph(f"<b>Top events for Trip ID {trip_id}:</b>", styles['Heading1']))
    if json_data is not None:  # Check if json_data is not None
        for event in json_data:
            event_str = ""
            if 'name' in event:
                event_str += f"<b>Event Name:</b> {event['name']}<br/>"
            if 'type' in event:
                event_str += f"<b>Location:</b> {event['type']}<br/>"
            if 'Price Range' in event:
                event_str += f"<b>Date:</b> {event['price_ranges']}<br/>"
            if 'URL' in event:
                event_str += f"<b>Description:</b> {event['url']}<br/><br/>"
            content.append(Paragraph(event_str, styles['Normal']))
            print("Top events for Trip ID", trip_id, ":")
            for event in json_data:
                print("Event Name:", event.get('name', 'N/A'))
                print("type:", event.get('type', 'N/A'))
                print("Date:", event.get('price_ranges', 'N/A'))
                print("Description:", event.get('url', 'N/A'))
                print()
    else:
        content.append(Paragraph("No event information available", styles['Normal']))
        print("No event information available")

def flight(trip_id, content):
    top_flights = get_top_3_fastest_flights(trip_id)
    content.append(Paragraph(f"<b>Top 3 fastest flights for Trip ID {trip_id}:</b>", styles['Heading1']))
    if top_flights:
        content.append(Paragraph(str(top_flights), styles['Normal']))
        print(f"Top 3 fastest flights for Trip ID {trip_id}:")
        print(top_flights)
    else:
        content.append(Paragraph("No flight information available", styles['Normal']))
        print(f"No flight information available for Trip ID {trip_id}")

def topAttractions(city:str, content):
    top_attractions = attractions(city)
    content.append(Paragraph(f"<b>Top attractions for destination city {city}:</b>", styles['Heading1']))
    if top_attractions:
        for i, attraction in enumerate(top_attractions[:5], start=1):
            attraction_info = [
                f"{i}. {attraction['name']}",
                f"   Address: {attraction['address']}",
                f"   Category: {attraction['primary_category']}",
                f"   Description: {attraction['description']}"
            ]
            content.append(Paragraph("<br/>".join(attraction_info), styles['Normal']))
            print(f"Top Attraction {i} in {city}:")
            print(f"Name: {attraction.get('name', '')}")
            print(f"Address: {attraction.get('address', '')}")
            print(f"Category: {attraction.get('primary_category', '')}")
            print(f"Description: {attraction.get('description', '')}")
    else:
        content.append(Paragraph("No attraction information available", styles['Normal']))
        print(f"No attraction information available for {city}")

def topHotels(city, checkin_date, checkout_date, content):
    top_5_hotels = Hotels(city, checkin_date, checkout_date)
    content.append(Paragraph(f"<b>Top hotels for destination city {city}:</b>", styles['Heading1']))
    if top_5_hotels:
        for i, hotel in enumerate(top_5_hotels, start=1):
            hotel_info = [
                f"{hotel['title']}",
                f"   Rating: {hotel['rating']}",
                f"   Provider: {hotel['provider']}",
                f"   Price: {hotel['price']}"
            ]
            content.append(Paragraph("<br/>".join(hotel_info), styles['Normal']))
            print(f"Top Hotel {i} in {city}:")
            print(f"Title: {hotel.get('title', '')}")
            print(f"Rating: {hotel.get('rating', '')}")
            print(f"Provider: {hotel.get('provider', '')}")
            print(f"Price: {hotel.get('price', '')}")
    else:
        content.append(Paragraph("No hotel information available", styles['Normal']))
        print(f"No hotel information available for {city}")

if __name__ == "__main__":
    styles = getSampleStyleSheet()
    file_path = "src/dataset/hackupc-travelperk-dataset-extended.csv"
    trip_id = int(input("Enter the Trip ID: "))
    destination_city = None
    trip_data = []
    
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            trip_data.append(row)
            if int(row['Trip ID']) == trip_id:
                destination_city = row['Arrival City']
                checkin_date = row['Departure Date']
                checkout_date = row['Return Date']

    checkin_date = datetime.strptime(checkin_date, "%d/%m/%Y")
    checkin_date = checkin_date.strftime("%Y-%m-%d")
    
    checkout_date = datetime.strptime(checkout_date, "%d/%m/%Y")
    checkout_date = checkout_date.strftime("%Y-%m-%d")

    pdf_file = f"Trip_{trip_id}_Itinerary.pdf"
    doc = SimpleDocTemplate(pdf_file)
    content = []
    
    print_itinerary(trip_data, trip_id, content)
    buddies(trip_id, content)
    topHotels(destination_city, checkin_date, checkout_date, content)
    events(trip_id, content)
    flight(trip_id, content)
    topAttractions(destination_city, content)
    
    doc.build(content)
    print(f"PDF file '{pdf_file}' generated successfully.")
