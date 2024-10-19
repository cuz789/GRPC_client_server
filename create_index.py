import redis

# Connect to Redis
r = redis.Redis(
    host='redis-19489.c275.us-east-1-4.ec2.redns.redis-cloud.com',
    port=19489,
    username='user1',
    password='Coen6313@poc'
)


# Recreate the index with 'year', 'category', 'motivation', 'firstname', and 'surname'
r.execute_command('FT.CREATE', 'prizeIndex', 'ON', 'JSON', 'PREFIX', '1', 'prize:', 
                  'SCHEMA', 
                  '$.year', 'AS', 'year', 'NUMERIC',  # Index 'year' as NUMERIC
                  '$.category', 'AS', 'category', 'TAG',  # Index 'category' as TAG
                  '$.laureates[*].motivation', 'AS', 'motivation', 'TEXT',  # Index 'motivation' as TEXT
                  '$.laureates[*].firstname', 'AS', 'firstname', 'TEXT',  # Index 'firstname' as TEXT
                  '$.laureates[*].surname', 'AS', 'surname', 'TEXT')  # Index 'surname' as TEXT
print("Index recreated successfully with 'firstname', 'surname', and 'motivation'.")


