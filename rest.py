#!/usr/bin/env python

import json
from paho.mqtt import client
import web

web.config.debug = True

patterns = ['running_red', 'running_white', 'red_in_white', 'running_white_blue']

urls = (
    '/api/patterns', 'list_patterns',
    '/api/run/(.+)/', 'run_pattern',
    '/api/run/(.+)', 'run_pattern',
)

class list_patterns:
    def GET(self):
        output = json.dumps(patterns)
        return output


class run_pattern:
    def GET(self, pattern):
        if pattern in patterns:
            output = 'running ' + pattern
            broker.reconnect()
            (mqttresult, mid) = broker.publish('juleljus/',pattern)
            print(mqttresult)
            print(mid)
            return output
        else:
            return web.notfound("Does not exist")

def on_disconnect(client, userdata, rc):
    print("disconnected")
    client.reconnect()

def on_connect(client, userdata, flags, rc):
    print("Connection returned result: "+connack_string(rc))

broker = client.Client()
broker.on_disconnect = on_disconnect
broker.on_connect = on_connect
broker.connect('blacken.linuxguru.se')

if __name__ == "__main__":
    app = web.application(urls, globals(), autoreload=True)
    web.httpserver.runsimple(app.wsgifunc(), ("::", 8080))
else:
    app = web.application(urls, globals())
    application = app.wsgifunc()
