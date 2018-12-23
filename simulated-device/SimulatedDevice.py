# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
import random
import time
import sys
import datetime
import threading
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

from data import *

MESSAGE_TIMEOUT = 10000

# Define the JSON message to send to IoT Hub.

MSG_TXT = "{ SLN: %d, timestamp : %s, CO_level: %.2f}"


def load_data_points(f_name,point_list):
    lines=[line.rstrip('\n') for line in open(f_name)]
    for line in lines:
        point_list.append(float(line))

    return point_list


def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def connect_direct(index):  #input index is 1-index based
  try:
    client_device=IoTHubClient(CONNECTION_STRINGS[index-1],PROTOCOL_NAME)
    print(" Device "+DEVICE_NAMES[index-1]+" connected to cloud")

    source_data_file=DEVICE_TO_FILE_MAP[DEVICE_NAMES[index-1]]
    print("Sending data file "+source_data_file)

    num_data_points=DATA_POINT_COUNT
    
    point_list=load_data_points(source_data_file,[])

    for i in range(num_data_points):
      data_val=point_list[i]
      message_text_formatted = MSG_TXT % (i,str(datetime.datetime.utcnow()),data_val)
      message = IoTHubMessage(message_text_formatted)
      print(sys.getsizeof(message))
      print( "Sending message: %s" % message.get_string() )
      client_device.send_event_async(message, send_confirmation_callback, None)
      time.sleep(1)

  except IoTHubError as iothub_error:
    print ( "Unexpected error %s from IoTHub" % iothub_error )
  except KeyboardInterrupt:
    print ( "IoTHubClient sample stopped" )


print("Sending data directly to cloud")
NUM_DEVICES=5

start_time=time.clock()
print(start_time)
connect_direct(4)
end_time=time.clock()
print(end_time)
print("Time taken: "+str(end_time-start_time))

#thread_list=[]
#for i in range(NUM_DEVICES):
#  thread_list.append(threading.Thread(target=connect_direct, args=(i+1,)))
#
#for i in range(NUM_DEVICES):
#  print("started device "+str(i+1))
#  thread_list[i].start()





