import json
import os
import time

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from dotenv import load_dotenv
from paho.mqtt import publish


class Agent:

    def __init__(self):
        super().__init__()
        self.green = 27
        self.red = 22
        self.blue = 17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)

    #   get .env
        load_dotenv()
        self.hostname = os.getenv('HOST')
        self.port = os.getenv('MQTT_BROKER_PORT')

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # client.subscribe("$SYS/#")
        self.client.subscribe("#")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode("utf-8")
        if msg.topic in ["DataTopic", "CommandTopic", "ResponseTopic"]:
            data = json.loads(payload)
            print(f"[ {msg.topic} ] - {data}")
        if msg.topic == "CommandTopic":
            if data["method"] == "set":
                if data["cmd"] == "light-blue":
                    GPIO.output(self.blue, data["light-blue"])
                elif data["cmd"] == "light-green":
                    GPIO.output(self.green, data["light-green"])
                elif data["cmd"] == "light-red":
                    GPIO.output(self.red, data["light-red"])

            publish.single(
                "ResponseTopic", json.dumps(data), hostname=self.hostname, port=self.port
            )

    def main(self):
        try:
            GPIO.output(self.red, 0)
            GPIO.output(self.green, 0)
            GPIO.output(self.blue, 0)
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            self.client.connect("118.67.130.122", 1774, 60)
            self.client.loop_forever()

        except Exception as e:
            print(e)
        except KeyboardInterrupt:
            print("keyboardInterrupt")
        finally:
            GPIO.cleanup()
