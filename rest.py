#!/usr/bin/env python

import paho.mqtt.client as mqtt
from flask import Flask, send_from_directory
import ssl

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile("config.py")

def on_disconnect(client, userdata, rc):
    print("disconnected")
    client.reconnect()

def get_patterns(client, timeout=1.0):
    def on_message(iclient, userdata, msg):
        iclient.patterns = msg.payload
        iclient.on_message = None

    def on_connect(iclient, userdata, flags, rc):
        print("connected")
        iclient.subscribe("juleljus/return")
        iclient.on_message = on_message
    subscriber = mqtt.Client(client_id="fdsafas100")
    subscriber.on_connect = on_connect
    subscriber.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
    subscriber.username_pw_set(app.config['MQTT_USERNAME'], app.config['MQTT_PASSWORD'])
    subscriber.connect(app.config['MQTT_SERVER'], 8883)

    timeout = 0
    while not subscriber.on_message:
        timeout += 1
        if timeout % 100 == 0:
            print("looping")
        subscriber.loop(timeout=0.1, max_packets=1)
        client.loop(timeout=0.1, max_packets=1)

    (mqttresult, mid) = client.publish('juleljus/patterns','get')

    timeout = 0
    while subscriber.on_message:
        timeout += 1
        if timeout % 10 == 0:
            client.reconnect()
            print("looping")
            (mqttresult, mid) = client.publish('juleljus/patterns','get')
        subscriber.loop(timeout=0.1, max_packets=1)
        client.loop(timeout=0.1, max_packets=1)

    subscriber.unsubscribe("juleljus/#")
    subscriber.on_message = None
    patterns = subscriber.patterns
    subscriber.disconnect()
    return subscriber.patterns

@app.route("/api/patterns")
def list_patterns():
    patterns = get_patterns(broker)
    return patterns

@app.route("/api/run/<pattern>")
def run_pattern(pattern):
    if pattern in patterns:
        output = 'running ' + pattern
        broker.reconnect()
        (mqttresult, mid) = broker.publish('juleljus/run',pattern)
        return output
    else:
        return web.notfound("Does not exist")

broker = mqtt.Client()
broker.on_disconnect = on_disconnect
broker.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
broker.username_pw_set(app.config['MQTT_USERNAME'], app.config['MQTT_PASSWORD'])
broker.connect(app.config['MQTT_SERVER'], 8883)

patterns = get_patterns(broker)

if __name__ == "__main__":
    app.run(debug=True)
