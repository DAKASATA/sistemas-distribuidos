import grpc 
from concurrent import futures
import proto_site_pb2 as pb2
import proto_site_pb2_grpc as pb2_grpc
from time import sleep
from routes import query

class SearchService(pb2_grpc.SearchServicer):
    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):
        item = []
        response = []
        message = request.message
        result = f'"{message}" '
        cursor.execute("SELECT * FROM item;")
        query_res = cursor.fetchall()
        for i in query_res:
            if message in i[1]:
                item.append(i)

        for j in item:
            result = dict()
            result['title'] = j[1]
            result['description'] = j[2]
            result['keywords'] = j[3]
            result['url'] = j[4]
            response.append(result)
        print(pb2.SearchResults(site = response))
        return pb2.SearchResults(site = response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SearchServicer_to_server(SearchService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    sleep(20)
    conn = query.init_db()
    cursor = conn.cursor()
    serve()

