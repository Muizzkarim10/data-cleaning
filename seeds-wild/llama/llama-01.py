import requests
import json
import csv
from datetime import datetime

# Input CSV file and output file paths
input_csv_file = 'sample.csv'  # Input file with plant names
output_csv_file = 'plant_data.csv'  # Output file to save the plant data
success_log_file = 'success_log.txt'  # Log file for successful operations
error_log_file = 'error_log.txt'  # Log file for unsuccessful operations

# API endpoint
url = "http://localhost:11434/api/generate"

# Function to fetch data for a given plant name
def fetch_data_for_plant(plant_name):
    data = {
        "model": "llama3",
        "prompt": f"Provide the following data for {plant_name}: temperature, soil temperature, precipitation, soil moisture, sunshine duration, and humidity. Return data in JSON format.",
        "stream": False
    }
    response = requests.post(url, json=data)
    
    try:
        json_response = response.json()
        if 'response' in json_response:
            inner_json_str = json_response['response'].split("```")[1].strip()
            inner_json = json.loads(inner_json_str)
            return inner_json
        else:
            print(f"No response field in JSON for {plant_name}.")
            return None
    except json.JSONDecodeError:
        print(f"Response content for {plant_name} is not valid JSON.")
        return None

# Initialize output CSV with headers if not exists
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as out_csv:
    fieldnames = ['Name', 'Temperature', 'Soil Temperature', 'Precipitation', 'Soil Moisture', 'Sunshine Duration', 'Humidity']
    writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
    writer.writeheader()  # Write headers only once

# Read plant names from input CSV and process in real-time
with open(input_csv_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    # Process each plant name and save data immediately
    for row in reader:
        plant_name = row['Names']  # Adjust column name as necessary
        plant_data = fetch_data_for_plant(plant_name)
        
        if plant_data:
            # Write data to output CSV immediately
            with open(output_csv_file, mode='a', newline='', encoding='utf-8') as out_csv:
                writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
                writer.writerow({
                    'Name': plant_name,
                    'Temperature': plant_data.get('temperature'),
                    'Soil Temperature': plant_data.get('soil_temperature'),
                    'Precipitation': plant_data.get('precipitation'),
                    'Soil Moisture': plant_data.get('soil_moisture'),
                    'Sunshine Duration': plant_data.get('sunshine_duration'),
                    'Humidity': plant_data.get('humidity')
                })
            
            # Log the successful operation immediately
            with open(success_log_file, mode='a', encoding='utf-8') as success_log:
                success_log.write(f"{datetime.now()} - Retrieved data for {plant_name} and saved to CSV\n")
            
            print(f"Data for {plant_name} retrieved and saved.")
        else:
            # Log the error if data could not be retrieved
            with open(error_log_file, mode='a', encoding='utf-8') as error_log:
                error_log.write(f"{datetime.now()} - Data for {plant_name} could not be retrieved.\n")
            
            print(f"Data for {plant_name} could not be retrieved.")
