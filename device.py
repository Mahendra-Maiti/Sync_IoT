from data import *
import datetime
import io
import json
import requests
import socket
import time

class CONN:
    '''
        create connection object
    '''
    @classmethod
    def create_connection(cls,host_address='10.0.0.18',port_number=8081):
        '''
                Create a socket object
        '''
        conn_obj= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn_obj.connect((host_address,port_number))
        return conn_obj

    @classmethod
    def send_data(cls,conn_obj,key):
        '''
                Send data corresponding to a particular key using connection object
        '''
        data_packet=PACKET
        #data_packet['data']=str(datetime.datetime.utcnow())
        #data_packet['key']=key
        data_packet['deviceID']=str(key)
        data_packet['Data']['persist_time']=str(int(key)*10)
        data_packet['Data']['ID']=str((key*23))
        data_packet_string=json.dumps(data_packet)
        encoded_string=data_packet_string.encode('UTF-8')
        byte_obj=bytearray(encoded_string)
        print(byte_obj)
        conn_obj.send(byte_obj)
    

    @classmethod
    def ping_controller(cls,address):
        '''
                 Get an edge address
        '''
        obj=requests.get(address)
        return obj  


class ioT:
    def __init__(self,loc_file,stream_file, device_id):
        self.loc_list=[]
        self.data_points=[]

        self.loc_file=loc_file
        self.stream_file=stream_file

        self.id=device_id
        self.loc_index=0
        self.data_index=0

        self.load_data_points()
        self.load_location_points()

        self.loc_x=self.loc_list[self.loc_index][0]
        self.loc_y=self.loc_list[self.loc_index][1]
        self.edge_config={}
        self.connection_object=None
        self.header_packet={}
        

    def load_location_points(self):
        '''
                Load list of locations to which the device moves
        '''
        lines=[line.rstrip('\n') for line in open(self.loc_file)]
        for line in lines:
            t_list=[]
            t_list.append(int(line.split(" ")[0]))
            t_list.append(int(line.split(" ")[1]))
            self.loc_list.append(t_list)


    def load_data_points(self):
        '''
                Load data points to be streamed
        '''
        lines=[line.rstrip('\n') for line in open(self.stream_file)]
        for line in lines:
            self.data_points.append(float(line))


    def build_header(self):
        '''
                Build header files
        '''
        header_packet=HEADER_DICT.create(self.id,self.loc_x,self.loc_y,persist_time=10)
        self.header_packet=header_packet


    def connect_edge(self):
        '''
                Connect device to an edge repository
        '''
        self.__get_edge_addr()
        self.connection_object=CONN.create_connection(self.edge_config['HOST'],self.edge_config['PORT'])
        print("Device "+str(self.id)+" connected to "+str(self.edge_config['HOST'])+" "+str(self.edge_config['PORT']))

        
    def __get_edge_addr(self):
        '''
                Get address of edge repository by pinging controller
        '''
        if 'HOST' in self.edge_config:  #only ping controller if disconnected from current edge
            return

        obj=requests.get(CONTROLLER_ADDR).json()

        print("obtained response")
        print(obj)
        # val=json.loads(obj)
        self.edge_config['HOST']=obj['HOST']
        self.edge_config['PORT']=int(obj['PORT'])

        # obj=CONN.ping_controller(CONTROLLER_ADDR+"?x="+str(self.loc_x)+"&y="+str(self.loc_y))
        # val=json.loads(obj)
        # self.edge_config['HOST']=val['HOST']
        # self.edge_config['PORT']=val['PORT']


    def move(self):
        '''
                Move to next location
        '''
        self.loc_index=(self.loc_index+1)%(len(self.loc_list))
        self.loc_x=self.loc_list[self.loc_index][0]
        self.loc_y=self.loc_list[self.loc_index][1]
        print("Device "+str(self.id)+" moved to "+"("+str(self.loc_x)+","+str(self.loc_y)+")")


    def send_data(self):
        '''
                Send data to connected edge repository
        '''
        data_point=self.data_points[self.data_index]
        self.data_index=self.data_index+1
        data_packet={}
        data_packet['Data']={}
        data_packet['Data']['value']=str(data_point)
        data_packet['Data']['timestamp']=str(datetime.datetime.utcnow())
        data_packet['deviceName']=str(self.id)
        data_packet['Data']['destination']="dummy"
        data_packet['Data']['x_loc']=self.loc_x
        data_packet['Data']['y_loc']=self.loc_y

        data_packet_string=json.dumps(data_packet)
        encoded_string=data_packet_string.encode('UTF-8')
        byte_obj=bytearray(encoded_string)

        print("Device "+str(self.id)+" sending ")
        print(byte_obj)
        print("...............")
        self.connection_object.send(byte_obj)

    def terminate_connection(self):
        '''
                Close connection to edge repository
        '''
        self.connection_object.close()
        print("Device "+str(self.id)+" disconnecting")

    def send_to_cloud(self):
        '''
                Synchronize data directly with the cloud
        '''
        pass









