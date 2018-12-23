import socket                   
import io
from PIL import Image
import pyscreenshot as scr
import datetime
import requests
import json
import datetime
import threading
import time
from data import *
from device import *


class driver:

    @classmethod
    def run(cls,key,exit_flag):

        print("Started Driver.............")

        r=CONN.create_connection()

        CONN.send_data(r,key)

        time.sleep(5)

        if exit_flag==False:

            counter=10
            while counter>0:
                print("Sending"+str(counter))
                CONN.send_data(r,counter)
                counter=counter-1
                time.sleep(2)
        
        print("Exiting")
        r.close()



    @classmethod
    def run_test(cls,header_dict_list):

        thread_list=[]
        for header_dict in header_dict_list:
            thread_list.append(threading.Thread(target=cls.run,args=(header_dict)))

        for i in range(len(thread_list)):
            print("Started thread "+str(i))
            thread_list[i].start()


    @classmethod
    def run_multithread(cls):
        '''
            devices run on separate threads
        '''
        thread_list=[]

        for i in range(10):
            if i%2==0:
                thread_list.append(threading.Thread(target=cls.run, args=(i,True)))
            else:
                thread_list.append(threading.Thread(target=cls.run, args=(i,True)))

        for i in range(10):
            print("started thread"+str(i))
            thread_list[i].start()

    @classmethod
    def run_main(cls,index,iter_count):
        loc_file=LOC_FILE_DIR+"loc_"+str(index)+".txt"
        # data_file=DATA_FILE_DIR+FILE_NAMES[index-1]
        data_file_name=TEST_DF[index]

        device_name=data_file_name[:-4].lower()

        print("device name is " +device_name)

        device=ioT(loc_file,data_file_name,device_name)

        for i in range(1):
            device.connect_edge()
            for j in range(iter_count):
                device.send_data()
                time.sleep(1)
            device.move()
            device.edge_config={}

        device.terminate_connection()

    @classmethod
    def run_1(cls):
        loc_file=LOC_FILE_DIR+"loc_1.txt"
        data_file=DATA_FILE_DIR+FILE_NAMES[0]

        device=ioT(loc_file,data_file,9999999)
        device.connect_edge()
        device.send_data()
        device.terminate_connection()


    @classmethod
    def test_1(cls,iter_count):
        NUM_DEVICES=5
        thread_list=[]

        for i in range(NUM_DEVICES):
            thread_list.append(threading.Thread(target=cls.run_main, args=(i,iter_count,)))
        
        for i in range(NUM_DEVICES):
            print("started device "+str(i))
            thread_list[i].start()

    

itercounts=[50,60,70,80,100,500,1000]

driver.test_1(50)



#driver.run_1()
