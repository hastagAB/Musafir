import requests
import pandas as pd
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

from city.cityMapper import find_country  

def get_top_events_for_trip(trip_id, top_n=5):
    api_key = "6U1eANGQqQlLPnqfDbMG8Ilt6j8Bwlnk"
    dataset_path = "src/dataset/hackupc-travelperk-dataset-extended.csv"
    
    try:
        df = pd.read_csv(dataset_path)

        trip_data = df[df['Trip ID'] == trip_id]

        if not trip_data.empty:
            arrival_city = trip_data.iloc[0]['Arrival City']
            
            country_name, country_code = find_country(arrival_city)
            
            url = f"https://app.ticketmaster.com/discovery/v2/events.json?countryCode={country_code}&apikey={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if '_embedded' in data:
                top_events_data = data['_embedded'].get('events', [])[:top_n]
                
                extracted_events = []
                for event in top_events_data:
                    event_info = {
                        'name': event['name'],
                        'type': event['type'],
                        'price_ranges': event.get('priceRanges', []),
                        'url': event['url']
                    }
                    extracted_events.append(event_info)
                
                return extracted_events
            else:
                print("No '_embedded' key found in data.")
                return None
        else:
            print("Trip ID not found in the dataset.")
            return None
    except Exception as e:
        print("Error occurred:", e)
        return None

