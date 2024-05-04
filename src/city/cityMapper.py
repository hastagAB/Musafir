import json
import pandas as pd

# Load the dataset from CSV file
df = pd.read_csv("../Dataset/hackupc-travelperk-dataset-extended.csv")

# Load the country-city mapping from JSON file
with open("countries.json", "r") as file:
    country_city_mapping = json.load(file)

# Function to find the country for a given city
def find_country(city):
    for country, cities in country_city_mapping.items():
        if city in cities:
            return country
    return "Unknown"

# Create a new column 'Country Name' in the DataFrame
df['Country Name'] = df['Arrival City'].apply(find_country)

# Export the updated DataFrame to CSV
df.to_csv('dataset_with_countries.csv', index=False)

print("CSV file has been exported successfully.")
