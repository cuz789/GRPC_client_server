import redis
import json

# Connect to Redis
r = redis.Redis(
    host='redis-19489.c275.us-east-1-4.ec2.redns.redis-cloud.com',
    port=19489,
    username='user1',
    password='Coen6313@poc'
)

'''index_info = r.execute_command('FT.INFO', 'prizeIndex')
print(index_info)  # This will show you if the fields were indexed correctly'''




'''# Query for prizes in the year 2013 and category 'economics'
query = '@year:[2015, 2015] @category:{medicine}'
result = r.execute_command('FT.SEARCH', 'prizeIndex', query)

# Print the results
print(result)'''

'''query = '@motivation:discovery'
result = r.execute_command('FT.SEARCH', 'prizeIndex', query)
print(result)'''

'''# Drop the old index
r.execute_command('FT.DROPINDEX', 'prizeIndex')
print("Old index dropped.")'''














