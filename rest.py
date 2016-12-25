#!/usr/bin/env python

import json
import paho.mqtt.client as mqtt
import web
import time

web.config.debug = True

urls = (
    '/api/patterns', 'list_patterns',
    '/api/run/(.+)/', 'run_pattern',
    '/api/run/(.+)', 'run_pattern',
)

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
    subscriber.connect('blacken.linuxguru.se')

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

class list_patterns:
    def GET(self):
        patterns = get_patterns(broker)
        return patterns

class run_pattern:
    def GET(self, pattern):
        if pattern in patterns:
            output = 'running ' + pattern
            broker.reconnect()
            (mqttresult, mid) = broker.publish('juleljus/run',pattern)
            return output
        else:
            return web.notfound("Does not exist")

broker = mqtt.Client()
broker.on_disconnect = on_disconnect
broker.connect('blacken.linuxguru.se')

patterns = get_patterns(broker)

if __name__ == "__main__":
    app = web.application(urls, globals(), autoreload=True)
    web.httpserver.runsimple(app.wsgifunc(), ("::", 8080))
else:
    app = web.application(urls, globals())
    application = app.wsgifunc()
