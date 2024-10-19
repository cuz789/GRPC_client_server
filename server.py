import grpc
from concurrent import futures
import redis
import json
import protobuf_queries_pb2_grpc as pb2_grpc
import protobuf_queries_pb2 as pb2

# Connect to Redis
r = redis.Redis(
    host='redis-19489.c275.us-east-1-4.ec2.redns.redis-cloud.com',
    port=19489,
    username='user1',
    password='Coen6313@poc'
)

# Function to handle each query
def query_total_laureates_by_category_and_year_range(category, start_year, end_year):
    query = f'@year:[{start_year} {end_year}] @category:{{{category}}}'
    result = r.execute_command('FT.SEARCH', 'prizeIndex', query)
    total_laureates = 0
    for i in range(2, len(result), 2):
        prize_json = result[i][1]
        prize_dict = json.loads(prize_json)
        if 'laureates' in prize_dict:
            total_laureates += len(prize_dict['laureates'])
    return total_laureates

def query_total_laureates_by_keyword(keyword):
    query = f'@motivation:{keyword}'
    result = r.execute_command('FT.SEARCH', 'prizeIndex', query)
    total_laureates = 0
    for i in range(2, len(result), 2):
        prize_json = result[i][1]
        prize_dict = json.loads(prize_json)
        if 'laureates' in prize_dict:
            for laureate in prize_dict['laureates']:
                if keyword.lower() in laureate.get('motivation', '').lower():
                    total_laureates += 1
    return total_laureates

def query_laureate_by_name(firstname, lastname):
    query = f'@firstname:{firstname} @surname:{lastname}'
    result = r.execute_command('FT.SEARCH', 'prizeIndex', query)
    laureates_data = []
    for i in range(2, len(result), 2):
        prize_json = result[i][1]
        prize_dict = json.loads(prize_json)
        for laureate in prize_dict.get('laureates', []):
            if laureate.get('firstname', '').lower() == firstname.lower() and laureate.get('surname', '').lower() == lastname.lower():
                laureates_data.append({
                    'firstname': laureate['firstname'],
                    'surname': laureate['surname'],
                    'year': int(prize_dict['year']),
                    'category': prize_dict['category'],
                    'motivation': laureate['motivation']
                })
    return laureates_data

# Service class to handle the gRPC queries
class LaureateQueryService(pb2_grpc.LaureateQueryServiceServicer):
    
    def GetLaureatesByCategoryAndYearRange(self, request, context):
        total_laureates = query_total_laureates_by_category_and_year_range(
            request.category, request.start_year, request.end_year
        )
        return pb2.TotalLaureatesResponse(total=total_laureates)

    def GetLaureatesByKeyword(self, request, context):
        total_laureates = query_total_laureates_by_keyword(request.keyword)
        return pb2.TotalLaureatesResponse(total=total_laureates)

    def GetLaureateByName(self, request, context):
        laureates_data = query_laureate_by_name(request.firstname, request.lastname)
        laureates = [pb2.Laureate(
            firstname=laureate['firstname'],
            surname=laureate['surname'],
            year=laureate['year'],
            category=laureate['category'],
            motivation=laureate['motivation']
        ) for laureate in laureates_data]
        
        return pb2.LaureatesResponse(laureates=laureates)


# Function to start the server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_LaureateQueryServiceServicer_to_server(LaureateQueryService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC server started on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
