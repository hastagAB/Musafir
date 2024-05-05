import json
import pycountry

def find_country(city_name):
    # Load the country-city mapping from JSON file
    with open("src/city/countries.json", "r") as file:
        country_city_mapping = json.load(file)
    
    # Iterate through the mapping to find the country for the given city
    for country, cities in country_city_mapping.items():
        if city_name in cities:
            # Find the country code using pycountry
            try:
                country_code = pycountry.countries.lookup(country).alpha_2
            except LookupError:
                country_code = "Unknown"
            return country, country_code
    return "Unknown", "Unknown"

# Sample usage:
# city_name = "London"  # Replace with the desired city name
# country_name, country_code = find_country(city_name)
# print(f"The country for {city_name} is: {country_name}")
# print(f"The country code for {country_name} is: {country_code}")
