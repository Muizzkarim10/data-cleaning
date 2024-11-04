import requests
import pandas as pd
import time

plant_names_df = pd.read_csv("names.csv")
plant_data = []

# GBIF API URL template for querying occurrences
def get_coordinates(plant_name):
    url = f"https://api.gbif.org/v1/occurrence/search?scientificName={plant_name}&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            result = data['results'][0]
            latitude = result.get("decimalLatitude")
            longitude = result.get("decimalLongitude")
            if latitude and longitude:
                return latitude, longitude
    return None, None

for _, row in plant_names_df.iterrows():
    plant_name = row["Names"]
    latitude, longitude = get_coordinates(plant_name)
    
    plant_data.append({
        "Plant Name": plant_name,
        "Latitude": latitude,
        "Longitude": longitude,
    })
    
    # Pause between requests to avoid rate limits
    time.sleep(1)

df = pd.DataFrame(plant_data)
df.to_csv("plant_locations.csv", index=False)
print("Location data collection complete. Saved to plant_locations.csv")
