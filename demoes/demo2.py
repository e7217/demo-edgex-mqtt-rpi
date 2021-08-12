import json
import os
import time

import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from dotenv import load_dotenv
from paho.mqtt import publish

load_dotenv()

host = os.getenv('HOST')
port = os.getenv('MQTT_BROKER_PORT')

dataset = {
    "name": "LED-Test-Device",
    "cmd": "",
}

GPIO.setmode(GPIO.BCM)

green = 27
red = 22
blue = 17

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("$SYS/#")
    client.subscribe("#")

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    if msg.topic in ["DataTopic", "CommandTopic", "ResponseTopic"]:
        data = json.loads(payload)
        print(f"[ {msg.topic} ] - {data}")
    if msg.topic == "CommandTopic":
        if data["method"] == "set":
            if data["cmd"] == "light-blue":
                GPIO.output(blue, data["light-blue"])
            elif data["cmd"] == "light-green":
                GPIO.output(green, data["light-green"])
            elif data["cmd"] == "light-red":
                GPIO.output(red, data["light-red"])

        publish.single("ResponseTopic", json.dumps(data), hostname=host, port=port)
    dataset = {
        "name": "LED-Test-Device",
        "cmd": "",
    }

try:
    GPIO.output(red, 0)
    GPIO.output(green, 0)
    GPIO.output(blue, 0)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port, 60)
    client.loop_forever()

except Exception as e:
    print(e)
except KeyboardInterrupt:
    print("keyboardInterrupt")
finally:
	GPIO.cleanup()

