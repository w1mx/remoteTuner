#!/usr/bin/env python3

TIME_BETWEEN_POLLS = 5

import time
import kat500
import asyncio
import websockets
from threading import Thread
from flask import Flask, current_app

app = Flask(__name__)

@app.route('/')
def index():
    return current_app.send_static_file("index.html")

def flask_thread():
    app.run(host = "0.0.0.0", port = 7020)

def tuner_control_thread():
    kat500_mode_names = {kat500.MODE_BYPASS: "bypass", kat500.MODE_MANUAL: "manual", kat500.MODE_AUTO: "auto"}
    tuner = kat500.KAT500(baud_rate = 38400)
    while True:
        tuner_status = {}
        tuner_status["firmwareRevision"] = tuner.get_firmware_revision()
        tuner_status["powered"] = tuner.get_powered()
        tuner_status["vswr"] = tuner.get_vswr()
        tuner_status["mode"] = tuner_mode_names[tuner.get_mode()]
        fault = tuner.get_fault()
        tuner_status["faultCode"] = fault[0]
        tuner_status["faultName"] = fault[1]
        tuner_status["faultDescription"] = fault[2]
        tuner_status["frequencyCounter"] = tuner.get_frequency_counter()
        print(connected_websockets)
        print(type(connected_websockets))
        time.sleep(TIME_BETWEEN_POLLS)

connected_websockets = set()

async def websocket_connection_handler(websocket, path):
    global connected_websockets
    connected_websockets.add(websocket)

if __name__ == "__main__":
    flask_thread_handle = Thread(target = flask_thread, daemon = True)
    flask_thread_handle.start()

    tuner_thread_handle = Thread(target = tuner_control_thread, daemon = True)
    tuner_thread_handle.start()

    asyncio.set_event_loop(asyncio.new_event_loop())
    websockets_server = websockets.serve(websocket_connection_handler, "0.0.0.0", 7030)
    asyncio.get_event_loop().run_until_complete(websockets_server)
    asyncio.get_event_loop().run_forever()
