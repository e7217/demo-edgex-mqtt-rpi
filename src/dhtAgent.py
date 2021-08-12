import json
import os
import time

import Adafruit_DHT
from dotenv import load_dotenv
from paho.mqtt import publish


class Agent:
    def __init__(self):
        super().__init__()
        self.dataset = {"name": "RPI-Test-Device", "cmd": "", "data": ""}

        #   get .env
        load_dotenv()
        self.hostname = os.getenv('HOST')
        self.port = os.getenv('MQTT_BROKER_PORT')

    def get_DHT(self):
        pin = 4
        sensor = Adafruit_DHT.DHT11
        h, t = Adafruit_DHT.read_retry(sensor, pin)
        if h is not None and t is not None:
            self.dataset["cmd"] = "temperature"
            self.dataset["data"] = 0
            self.dataset["temperature"] = t
            publish.single(
                "DataTopic",
                json.dumps(self.dataset),
                hostname=self.hostname,
                port=self.port,
            )
            self.dataset["cmd"] = "humidity"
            self.dataset["data"] = 0
            self.dataset["humidity"] = h
            publish.single(
                "DataTopic",
                json.dumps(self.dataset),
                hostname=self.hostname,
                port=self.port,
            )
            print("Temperature = {0:0.1f}*C Humidity = {1:0.1f}%".format(t, h))
            self.dataset = {"name": "RPI-Test-Device", "cmd": "", "data": ""}
        else:
            print("Read error")

    def main(self):
        try:
            while True:
                self.get_DHT()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Terminated by Keyboard")

        finally:
            print("End of Program")
