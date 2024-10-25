import grpc
import protobuf_queries_pb2_grpc as pb2_grpc
import protobuf_queries_pb2 as pb2

# Define query parameters as global variables or in a configuration dictionary
query_params = {
    "category_year_range": {"category": "peace", "start_year": 2013, "end_year": 2023},
    "keyword": "discovery",
    "name": {"firstname": "William", "lastname": "Kaelin"}
}

def create_stub():
    """Creates and returns a gRPC stub with the appropriate channel."""
    # Replace with your Cloud Run URL or local server URL
    target = 'grpc-nobelprize-service-644017900702.us-central1.run.app:443'
    channel = grpc.secure_channel(target, grpc.ssl_channel_credentials())
    return pb2_grpc.LaureateQueryServiceStub(channel)

def query_category_year_range(stub):
    """Executes Query 1 (Laureates by category and year range)."""
    params = query_params["category_year_range"]
    try:
        response = stub.GetLaureatesByCategoryAndYearRange(pb2.CategoryYearRangeRequest(
            category=params["category"],
            start_year=params["start_year"],
            end_year=params["end_year"]
        ))
        return response
    except grpc.RpcError as e:
        print(f"gRPC Error: {e.code()} - {e.details()}")
        return None

def query_keyword(stub):
    """Executes Query 2 (Laureates by keyword)."""
    try:
        response = stub.GetLaureatesByKeyword(pb2.KeywordRequest(
            keyword=query_params["keyword"]
        ))
        return response
    except grpc.RpcError as e:
        print(f"gRPC Error: {e.code()} - {e.details()}")
        return None

def query_name(stub):
    """Executes Query 3 (Laureate by name)."""
    params = query_params["name"]
    try:
        response = stub.GetLaureateByName(pb2.NameRequest(
            firstname=params["firstname"],
            lastname=params["lastname"]
        ))
        return response
    except grpc.RpcError as e:
        print(f"gRPC Error: {e.code()} - {e.details()}")
        return None

if __name__ == "__main__":
    stub = create_stub()
    
    # Query 1: Get laureates by category and year range
    response = query_category_year_range(stub)
    if response:
        print(f"Total laureates: {response.total}")
    
    # Query 2: Get total laureates by keyword
    response = query_keyword(stub)
    if response:
        print(f"Total laureates with '{query_params['keyword']}' in motivation: {response.total}")
    
    # Query 3: Get laureates by name
    response = query_name(stub)
    if response:
        for laureate in response.laureates:
            print(f"Laureate: {laureate.firstname} {laureate.surname}, Year: {laureate.year}, Category: {laureate.category}, Motivation:{laureate.motivation}")
