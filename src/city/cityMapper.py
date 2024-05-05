import json
import pycountry

def find_country(city_name):
    with open("src/city/countries.json", "r") as file:
        country_city_mapping = json.load(file)
    
    for country, cities in country_city_mapping.items():
        if city_name in cities:
            try:
                country_code = pycountry.countries.lookup(country).alpha_2
            except LookupError:
                country_code = "Unknown"
            return country, country_code
    return "Unknown", "Unknown"

