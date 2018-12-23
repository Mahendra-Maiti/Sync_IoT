import flask
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import json
import socket

HOST='10.0.0.18'

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)
api = Api(app)




class Edge_Address(Resource):
    def get(self):
        '''
            return ip address of edge repository on being accessed by an ioT device
        '''

        host=socket.gethostbyname(socket.gethostname())
        return json.dumps({"HOST": HOST, "PORT": 8002})



api.add_resource(Edge_Address, '/get_edge_address') # end point


if __name__ == '__main__':
     print("App Started")
     app.run(port='5000')
