import pandas as pd

df = pd.read_csv("src//dataset/hackupc-travelperk-dataset-extended.csv")

df = df.assign(Activities=df['Activities'].str.split(', ')).explode('Activities')

grouped = df.groupby('Activities').agg({'Traveller Name': list, 'Trip ID': lambda x: list(set(x))}).reset_index()
grouped.to_csv('activitiesMap.csv', index=False)

print("CSV file has been exported successfully.")
