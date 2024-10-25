import redis
import json

# Connect to Redis
r = redis.Redis(
    host='redis-19489.c275.us-east-1-4.ec2.redns.redis-cloud.com',
    port=19489,
    username='user1',
    password='Coen6313@poc'
)


#Query1 : Get total leaurates by category and year range
def query_total_laureates_by_category_and_year_range(category, start_year, end_year):
    # Create the search query for the category and year range
    query = f'@year:[{start_year} {end_year}] @category:{{{category}}}'

    # Execute the query using FT.SEARCH
    result = r.execute_command('FT.SEARCH', 'prizeIndex', query)

    total_laureates = 0

    # Skip the first element (total count), then alternate between doc ID and data
    for i in range(1, len(result), 2):  # Start from 1, step by 2 to get only the data elements
        prize_data = result[i + 1][1]  # Get the JSON string from the result
        prize_dict = json.loads(prize_data.decode('utf-8'))  # Parse the JSON string

        # Count the number of laureates in this prize
        if 'laureates' in prize_dict:
            total_laureates += len(prize_dict['laureates'])

    return total_laureates

"""
# Call the function with your test parameters for query 1
category = 'economics'  # You can change this to any category like 'medicine', 'physics', etc.
start_year = 2013       # Starting year for the range
end_year = 2023         # Ending year for the range

# Call the function and print the result
total_laureates = query_total_laureates_by_category_and_year_range(category, start_year, end_year)
print(f"Total laureates in category '{category}' between {start_year} and {end_year}: {total_laureates}")
"""

# Query 2: Get total number of laureates by motivation keyword
def query_total_laureates_by_keyword(keyword):
    # Create the search query for the keyword in the motivation field
    query = f'@motivation:{keyword}'  # Search in the motivation field
    
    # Execute the query using FT.SEARCH
    result = r.execute_command('FT.SEARCH', 'prizeIndex', query)
    
    total_laureates = 0

    # Skip the first element (total count), then alternate between doc ID and data
    for i in range(1, len(result), 2):  # Start from 1, step by 2 to get only the data elements
        prize_data = result[i + 1][1]  # Get the JSON string from the result
        prize_dict = json.loads(prize_data.decode('utf-8'))  # Parse the JSON string

        # Count the number of laureates whose motivation contains the keyword
        if 'laureates' in prize_dict:
            for laureate in prize_dict['laureates']:
                if keyword.lower() in laureate.get('motivation', '').lower():
                    total_laureates += 1
    
    return total_laureates
"""
# Call the function with your test parameters for query 2
keyword = "poverty"  # Example keyword to search in the motivation field
total_laureates = query_total_laureates_by_keyword(keyword)
print(f"Total laureates with '{keyword}' in their motivation: {total_laureates}")
"""


# Query 3: Get laureate information by first and last name
def query_laureate_by_name(firstname, lastname):
    # Normalize the search values to handle case sensitivity
    firstname = firstname.lower()
    lastname = lastname.lower()

    # Create the search query to reference the correct field names
    query = f'@firstname:{firstname} @surname:{lastname}'
    
    # Execute the query using FT.SEARCH
    result = r.execute_command('FT.SEARCH', 'prizeIndex', query)
    
    laureates_data = []

    # Skip the first element (total count), then alternate between doc ID and data
    for i in range(1, len(result), 2):  # Start from 1, step by 2 to get only the data elements
        prize_data = result[i + 1][1]  # Get the JSON string from the result
        prize_dict = json.loads(prize_data.decode('utf-8'))  # Parse the JSON string

        # Find the matching laureate
        for laureate in prize_dict.get('laureates', []):
            if laureate.get('firstname', '').lower() == firstname and laureate.get('surname', '').lower() == lastname:
                laureates_data.append({
                    'year': prize_dict['year'],
                    'category': prize_dict['category'],
                    'motivation': laureate['motivation']
                })
    
    return laureates_data

"""
# Example input for Query 3
firstname = 'Jean'
lastname = 'Tirole'

# Call the function and print the result
laureate_info = query_laureate_by_name(firstname, lastname)
print(f"Laureate information for {firstname} {lastname}: {laureate_info}")
"""
