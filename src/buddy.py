import pandas as pd
import json

def buddyData(trip_id):
    df = pd.read_csv("src/dataset/hackupc-travelperk-dataset-extended.csv")
    trip_data = df[df['Trip ID'] == trip_id]
    
    if trip_data.empty:
        return json.dumps({"error": "Trip ID not found."})
    
    traveler_name = trip_data.iloc[0]['Traveller Name']
    destination = trip_data.iloc[0]['Arrival City']
    departure_date = pd.to_datetime(trip_data.iloc[0]['Departure Date'], format='%d/%m/%Y')
    return_date = pd.to_datetime(trip_data.iloc[0]['Return Date'], format='%d/%m/%Y')
    main_traveler_activities = trip_data.iloc[0]['Activities'].split(', ')
    
    other_travelers = df[(df['Arrival City'] == destination) & 
                         (pd.to_datetime(df['Departure Date'], format='%d/%m/%Y') <= return_date) & 
                         (pd.to_datetime(df['Return Date'], format='%d/%m/%Y') >= departure_date) & 
                         (df['Trip ID'] != trip_id)]
    
    other_travelers_by_date = {}
    
    current_date = departure_date
    while current_date <= return_date:
        current_date_str = str(current_date.date())
        
        matching_travelers = other_travelers[(pd.to_datetime(other_travelers['Departure Date'], format='%d/%m/%Y') <= current_date) & 
                                             (pd.to_datetime(other_travelers['Return Date'], format='%d/%m/%Y') >= current_date) &
                                             (other_travelers['Activities'].apply(lambda x: any(act in x.split(', ') for act in main_traveler_activities)))]
        
        matching_travelers_info = matching_travelers[['Traveller Name', 'Trip ID', 'Activities']].to_dict(orient='records')
        
        other_travelers_by_date[current_date_str] = matching_travelers_info
        
        current_date += pd.Timedelta(days=1)
    
    output = {
        'Traveler Name': traveler_name,
        'Destination': destination,
        'From Date': str(departure_date.date()),
        'To Date': str(return_date.date()),
        'Main Traveler Activities': main_traveler_activities,
        'Other Travelers': other_travelers_by_date
    }
    
    return format_json_output(output)

def format_json_output(output):
    formatted_output = ""
    formatted_output += f"Other Travelers:\n"
    for date, travelers in output['Other Travelers'].items():
        formatted_output += f"\n{date}:\n"
        for traveler in travelers:
            formatted_output += f"  - {traveler['Traveller Name']}:\n"
            activities = traveler['Activities'].split(', ')
            for activity in activities:
                formatted_output += f"      - {activity}\n"
    return formatted_output

