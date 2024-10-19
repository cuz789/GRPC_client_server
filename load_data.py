import requests
import redis
import json

# Connect to Redis
r = redis.Redis(
    host='redis-19489.c275.us-east-1-4.ec2.redns.redis-cloud.com',
    port=19489,
    username='user1',
    password='Coen6313@poc'
)

# Fetch Nobel Prize data from the API
url = 'https://api.nobelprize.org/v1/prize.json'
response = requests.get(url)

# Check if the data is fetched successfully
if response.status_code == 200:
    data = response.json()
    
    # Filter data for years 2013 to 2023
    filtered_data = [prize for prize in data['prizes'] if 2013 <= int(prize['year']) <= 2023]
    
    # Load each prize into Redis using 'year' and 'category' as part of the key
    for prize in filtered_data:
        year = int(prize['year'])  # Ensure year is numeric
        category = prize['category']
        key = f'prize:{year}:{category}'  # Key format like "prize:2013:economics"
        
        # Convert year to numeric in the JSON object before uploading
        prize['year'] = year
        
        # Store each prize entry as a separate JSON object
        r.execute_command('JSON.SET', key, '.', json.dumps(prize))
        print(f"Loaded prize data for {year} in category {category} into Redis.")
else:
    print(f"Failed to fetch data from the API. Status code: {response.status_code}")
