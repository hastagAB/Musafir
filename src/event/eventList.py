import requests

def get_top_events(country_code, api_key, top_n=5):
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?countryCode={country_code}&apikey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Extract top events
        top_events = data['_embedded']['events'][:top_n]
        
        # Extract relevant information for each event
        extracted_events = []
        for event in top_events:
            event_info = {
                'name': event['name'],
                'type': event['type'],
                'price_ranges': event.get('priceRanges', []),
                'url': event['url']
            }
            extracted_events.append(event_info)
        
        return extracted_events
    except Exception as e:
        print("Error occurred:", e)
        return None

# API Key for Ticketmaster
api_key = "6U1eANGQqQlLPnqfDbMG8Ilt6j8Bwlnk"

# Country code for Spain
country_code = "ES"

# Fetch top events happening in Spain
top_events = get_top_events(country_code, api_key)

# Print top events
if top_events:
    print(f"Top Events Happening in {country_code}:")
    for event in top_events:
        print("Name:", event['name'])
        print("Type:", event['type'])
        print("Price Ranges:", event['price_ranges'])
        print("Booking URL:", event['url'])
        print()
else:
    print("Failed to fetch top events.")
