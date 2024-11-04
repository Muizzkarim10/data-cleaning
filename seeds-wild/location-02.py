import pandas as pd
import openai
import time
import os

# Set up your OpenAI API key (ensure to set it as an environment variable)
openai.api_key = "api-key goes here"

# Function to get region information for a plant name
def get_region_info(plant_name):
    prompt = f"What tropical region does the plant '{plant_name}' belong to?"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.0",  # or "gpt-4" if you have access
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error during API call: {e}")
        return None

# Read plant names from CSV file
plant_names_df = pd.read_csv("names.csv")  # Ensure this file has a "Names" column

# Initialize an empty list to hold plant names with regions
plant_data = []

# Loop through each plant name and get region info
for _, row in plant_names_df.iterrows():
    plant_name = row["Names"]  # Make sure this matches your column name
    print(f"Processing: {plant_name}")  # Debugging line
    
    # Get the region information from ChatGPT
    region_info = get_region_info(plant_name)
    if region_info:
        print(f"Region for {plant_name}: {region_info}")  # Print region information
    else:
        print(f"No region info found for {plant_name}.")
    
    # Append data to list
    plant_data.append({
        "Plant Name": plant_name,
        "Region": region_info,
    })

    # Pause to avoid hitting API rate limits
    time.sleep(1)  # Adjust based on your plan's rate limits

# Convert the collected data to a DataFrame and save as CSV
df = pd.DataFrame(plant_data)
df.to_csv("plant_regions.csv", index=False)
print("Region data collection complete. Saved to plant_regions.csv")
