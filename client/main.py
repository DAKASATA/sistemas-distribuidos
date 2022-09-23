from flask import Flask, request, render_template  


import proto_site_pb2 as pb2_grpc
import proto_site_pb2_grpc as pb2
import grpc
import redis
import logging
from random import randint
import json, time

app = Flask(__name__)

r1 = redis.Redis(host="redis1", port=6379, db=0)
#r1.config_set('maxmemory', 1048576)
r1.config_set('maxmemory-policy', 'allkeys-lru')

r1.flushall()
r2 = redis.Redis(host="redis2", port=6379, db=0)
#r2.config_set('maxmemory', 1048576)
r2.config_set('maxmemory-policy', 'allkeys-lru')
r2.flushall()

r3 = redis.Redis(host="redis3", port=6379, db=0)
#r3.config_set('maxmemory', 1048576)
r3.config_set('maxmemory-policy', 'allkeys-lru')
r3.flushall()



class BuscarCliente(object):
    def __init__(self):
        self.host = 'backend'
        self.server_port = '50051'
        self.channel = grpc.insecure_channel('{}:{}'.format(self.host, self.server_port))
        self.stub = pb2.SearchStub(self.channel)

    def get_url(self, message):
        message = pb2_grpc.Message(message = message)
        print(f'{message}')
        stub = self.stub.GetServerResponse(message)
        return stub


@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/search', methods = ['GET'])

def search():
    client = BuscarCliente()
    search = request.args['search']
    cache = r1.get(search)
    if cache[0] == None and cache[1] == None and cache[2] == None:
        data = client.get_url(message=search)
        r1.set(search, str(data))
        
        return render_template('index.html', datos = data, procedencia = "Datos sacados de PostgreSQL")
    
    else:
        print(cache)
        data = cache.decode("utf-8")
        print(data)
        dicc = dict()
        dicc['Resultado'] = data
        print(cache)
        print(dicc)
        return render_template('index.html', datos = data, procedencia = "Datos sacados de Redis")
        
                

if __name__ == '__main__':
    time.sleep(25)