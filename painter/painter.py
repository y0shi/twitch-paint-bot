import time
import os
import threading
import paho.mqtt.client as mqtt
import driver

host = os.environ['MQ_HOST']
port = int(os.environ['MQ_PORT'])
topic = os.environ['MQ_TOPIC']

DEFAULT_P_TIME = 1.5
DEFAULT_D_DELAY = 0.5

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    text = msg.payload.decode('utf-8', 'ignore')
    print(f'Topic {msg.topic} Message: {text}')
    if text == 'FORWARD':
        driver.forward(paint=True)
        time.sleep(DEFAULT_P_TIME)
        driver.set_relay(False)
        time.sleep(DEFAULT_D_DELAY)
        driver.stop_all()

    elif text == 'RIGHT':
        driver.start_right(paint=True)
        time.sleep(DEFAULT_P_TIME)
        driver.set_relay(False)
        time.sleep(DEFAULT_D_DELAY)
        driver.stop_all()

    elif text == 'LEFT':
        driver.start_left(paint=True)
        time.sleep(DEFAULT_P_TIME)
        driver.set_relay(False)
        time.sleep(DEFAULT_D_DELAY)
        driver.stop_all()


if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port, 60)

    run = True
    while run:
        client.loop(timeout=1)
