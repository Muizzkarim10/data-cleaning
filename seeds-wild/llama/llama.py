import requests
import json

# List of plant names
plant_names = ["sunflower", "tulip",]  # Replace with your actual plant names

url = "http://localhost:11434/api/generate"

for plant_name in plant_names:
    data = {
        "model": "llama3",
        "prompt": f"Provide the following data for {plant_name}: temperature, soil temperature, precipitation, soil moisture, sunshine duration, and humidity. Return data in JSON format.",
        "stream": False
    }

    response = requests.post(url, json=data)

    # Optionally, if you want to parse the JSON response
    try:
        json_response = response.json()
        # Extract the relevant data from the response
        if 'response' in json_response:
            # Try to parse the inner JSON from the response field
            inner_json_str = json_response['response'].split("```")[1].strip()  # Split and get the JSON part
            inner_json = json.loads(inner_json_str)
            print(f"Parsed JSON response for {plant_name}:", inner_json)
        else:
            print(f"No response field in JSON for {plant_name}.")
    except json.JSONDecodeError:
        print(f"Response content for {plant_name} is not valid JSON.")
        