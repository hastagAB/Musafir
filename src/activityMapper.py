import pandas as pd

# Load the dataset from CSV file
df = pd.read_csv("Dataset/hackupc-travelperk-dataset-extended.csv")

# Split activities into separate rows
df = df.assign(Activities=df['Activities'].str.split(', ')).explode('Activities')

# Group travelers by activity and concatenate Trip IDs
grouped = df.groupby('Activities').agg({'Traveller Name': list, 'Trip ID': lambda x: list(set(x))}).reset_index()

# Export to CSV
grouped.to_csv('activitiesMap.csv', index=False)

print("CSV file has been exported successfully.")
