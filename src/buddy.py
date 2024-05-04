import pandas as pd
import json

# Load the dataset from CSV file
df = pd.read_csv("Dataset/hackupc-travelperk-dataset-extended.csv")


def get_trip_info(trip_id):
    # Filter the dataframe for the specified trip ID
    trip_data = df[df['Trip ID'] == trip_id]
    
    if trip_data.empty:
        return json.dumps({"error": "Trip ID not found."})
    
    # Extract trip details
    traveler_name = trip_data.iloc[0]['Traveller Name']
    destination = trip_data.iloc[0]['Arrival City']
    departure_date = pd.to_datetime(trip_data.iloc[0]['Departure Date'], format='%d/%m/%Y')
    return_date = pd.to_datetime(trip_data.iloc[0]['Return Date'], format='%d/%m/%Y')
    
    # Find other travelers for the same destination and overlapping date range
    other_travelers = df[(df['Arrival City'] == destination) & 
                         (pd.to_datetime(df['Departure Date'], format='%d/%m/%Y') <= return_date) & 
                         (pd.to_datetime(df['Return Date'], format='%d/%m/%Y') >= departure_date) & 
                         (df['Trip ID'] != trip_id)]
    
    # Initialize a dictionary to store other travelers' information by date
    other_travelers_by_date = {}
    
    # Iterate over each day of the main traveler's trip
    current_date = departure_date
    while current_date <= return_date:
        current_date_str = str(current_date.date())
        
        # Filter other travelers who are present on the current date
        current_travelers = other_travelers[(pd.to_datetime(other_travelers['Departure Date'], format='%d/%m/%Y') <= current_date) & 
                                            (pd.to_datetime(other_travelers['Return Date'], format='%d/%m/%Y') >= current_date)]
        
        # Extract traveler names and IDs
        current_travelers_info = current_travelers[['Traveller Name', 'Trip ID']].to_dict(orient='records')
        
        # Store the travelers' information for the current date
        other_travelers_by_date[current_date_str] = current_travelers_info
        
        # Move to the next day
        current_date += pd.Timedelta(days=1)
    
    # Prepare JSON output
    output = {
        'Traveler Name': traveler_name,
        'Destination': destination,
        'From Date': str(departure_date.date()),
        'To Date': str(return_date.date()),
        'Other Travelers': other_travelers_by_date
    }
    
    return json.dumps(output, indent=4)

# Example usage:
trip_id = 1  # Change this to the desired trip ID
trip_info = get_trip_info(trip_id)
print(trip_info)
