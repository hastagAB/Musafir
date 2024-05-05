import requests
from attraction.geoID import get_geo_id

def get_top_attractions_by_geocode(geocode, language="en_US", currency="USD"):
    url = "https://tourist-attraction.p.rapidapi.com/search"

    payload = {
        "location_id": geocode,
        "language": language,
        "currency": currency,
        "offset": "0"
    }

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "3df56689e1mshb6954452a2cec15p1e3346jsna689ad4acefd",
        "X-RapidAPI-Host": "tourist-attraction.p.rapidapi.com"
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and "data" in data["results"]:
            attractions = data["results"]["data"]
            top_attractions = []
            for attraction in attractions:
                address = ""
                if attraction.get("address_obj"):
                    address_parts = [
                        attraction["address_obj"].get("street1", ""),
                        attraction["address_obj"].get("city", ""),
                        attraction["address_obj"].get("state", ""),
                        attraction["address_obj"].get("postalcode", ""),
                        attraction["address_obj"].get("country", "")
                    ]
                    address = ", ".join(part for part in address_parts if part)
                else:
                    address = "Address not available"
                
                primary_category = ""
                if "offer_group" in attraction and "offer_list" in attraction["offer_group"]:
                    primary_category = attraction["offer_group"]["offer_list"][0].get("primary_category", "Category not available")
                else:
                    primary_category = "Category not available"
                
                attraction_info = {
                    "name": attraction["name"],
                    "address": address,
                    "primary_category": primary_category,
                    "description": attraction.get("description", "Description not available")
                }
                top_attractions.append(attraction_info)
            
            return top_attractions
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None

# Example usage:
def print_attractions(attractions):
    if attractions:
        print("Top 5 Attractions:")
        for i, attraction in enumerate(attractions[0:5], start=1):
            print(f"{i}. {attraction['name']}")
            print(f"   Address: {attraction['address']}")
            print(f"   Category: {attraction['primary_category']}")
            print(f"   Description: {attraction['description']}")
            print()
    else:
        print("Failed to fetch attractions.")

# Example usage:

def attractions(city:str):
    geo_id = get_geo_id(city)
    attractions = get_top_attractions_by_geocode(geo_id)
    return attractions

