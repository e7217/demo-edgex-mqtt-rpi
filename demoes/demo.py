import json
import os
import time

import Adafruit_DHT
from dotenv import load_dotenv
from paho.mqtt import publish

load_dotenv()
host = os.getenv('HOST')
port = os.getenv('MQTT_BROKER_PORT')


dataset = {
    "name": "RPI-Test-Device",
    "cmd": "",
    "data": ""
}

def get_DHT():
    pin = 4
    sensor = Adafruit_DHT.DHT11
    h, t = Adafruit_DHT.read_retry(sensor, pin)
    if h is not None and t is not None :
        dataset["cmd"] = "temperature"
        dataset["data"] = 0
        dataset["temperature"] = t
        publish.single("DataTopic", json.dumps(dataset),hostname=host, port=port)
        dataset["cmd"] = "humidity"
        dataset["data"] = 0
        dataset["humidity"] = h
        publish.single("DataTopic", json.dumps(dataset),hostname=host, port=port)
        print("Temperature = {0:0.1f}*C Humidity = {1:0.1f}%".format(t, h))
    else :
        print('Read error')

try:
    while True :
        get_DHT()
        time.sleep(1)
except KeyboardInterrupt:
    print("Terminated by Keyboard")
 
finally:
    print("End of Program")