import redis
import io
from PIL import Image
import pyscreenshot as scr
import datetime
import requests
import json

HOST='10.0.0.18'
PORT=6800
CONTROLLER_ADDR='https://a199339a.ngrok.io/get_edge_address'


class CONN:
    @classmethod
    def create_connection(cls,host_address,port_number):
        r=redis.Redis(host=host_address,port=port_number)
        return r

    @classmethod
    def send_data(cls,conn_obj,filename,key):
        f_obj=open(filename,"rb").read()
        conn_obj.set(key,f_obj)

    @classmethod
    def ping_controller(cls,address):
        '''
            Get an edge address
        '''
        obj=requests.get(address)
        return obj   

class screenshot:

    @classmethod
    def capture_whole_screen(cls,filename):
        im=scr.grab()
        im.save(filename)

class driver:
    @classmethod
    def run(cls):

        print("Started Driver.............")

        #res=CONN.ping_controller(CONTROLLER_ADDR)

        #obj=res.json()
        #val=json.loads(obj)
        # print(val['HOST'])
        # print(val['PORT'])
        #r=CONN.create_connection(val['HOST'],val['PORT'])
        r=CONN.create_connection(HOST,PORT)
        for i  in range(100):
            print("Iteration: "+str(i))
            file_name="sample_"+str(i)+".png"
            screenshot.capture_whole_screen(file_name)
            #CONN.send_data(r,file_name,str(datetime.datetime.now()))
            CONN.send_data(r,file_name,"curr_"+str(i))
        
        print("Exiting.....................")


driver.run()