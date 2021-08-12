import os

from celery import Celery
from dotenv import load_dotenv

from src.dhtAgent import Agent as DHT_Agent
from src.ledAgent import Agent as LED_Agent

load_dotenv()

broker_url = os.getenv('AMQP_BROKER')
celery_backend = os.getenv('CELERY_BACKEND')

app = Celery('tasks', broker=broker_url, backend=celery_backend)

@app.task
def init_dht():
    dht_agent = DHT_Agent()
    dht_agent.main()

@app.task
def init_led():
    led_agent = LED_Agent()
    led_agent.main()
