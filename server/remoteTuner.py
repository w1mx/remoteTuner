#!/usr/bin/env python3

TIME_BETWEEN_POLLS = 5

import time
import json
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

tuner = kat500.KAT500(baud_rate = 38400)
connected_websockets = set()
tuner_status_json = "{}"

def update_tuner_status():
    global tuner
    global tuner_status_json

    tuner_mode_names = {kat500.MODE_BYPASS: "bypass", kat500.MODE_MANUAL: "manual", kat500.MODE_AUTO: "auto"}

    tuner_status = {}
    tuner_status["time"] = time.time()
    tuner_status["firmwareRevision"] = tuner.get_firmware_revision()
    tuner_status["powered"] = tuner.get_powered()
    tuner_status["vswr"] = tuner.get_vswr()
    tuner_status["mode"] = tuner_mode_names[tuner.get_mode()]
    fault = tuner.get_fault()
    tuner_status["faultCode"] = fault[0]
    tuner_status["faultName"] = fault[1]
    tuner_status["faultDescription"] = fault[2]
    tuner_status["usersConnected"] = sum(not websocket.closed for websocket in connected_websockets)
    tuner_status["tuning"] = tuner.get_tuning()
    #tuner_status["frequencyCounter"] = tuner.get_frequency_counter()
    tuner_status_json = json.dumps(tuner_status)

def tuner_control_thread():
    while True:
        update_tuner_status()
        time.sleep(TIME_BETWEEN_POLLS)

async def receive_from_websocket(websocket):
    tuner_modes = {"bypass": kat500.MODE_BYPASS, "manual": kat500.MODE_MANUAL, "auto": kat500.MODE_AUTO}
    while True:
        try:
            message_json = await websocket.recv()
            message = json.loads(message_json)
            if "tune" in message:
                if message["tune"]:
                    print("Starting full search tune.");
                    tuner.set_full_search_tune()
                else:
                    print("Canceling full search tune.");
                    tuner.cancel_full_search_tune()
                update_tuner_status()
                asyncio.ensure_future(websocket.send(tuner_status_json))
            if "mode" in message and message["mode"] in tuner_modes:
                tuner.set_mode(tuner_modes[message["mode"]])
                update_tuner_status()
                asyncio.ensure_future(websocket.send(tuner_status_json))
        except:
            break

async def websocket_connection_handler(websocket, path):
    global connected_websockets

    connected_websockets.add(websocket)
    asyncio.create_task(receive_from_websocket(websocket))
    try:
        while True:
            if websocket.closed:
                break
            asyncio.ensure_future(websocket.send(tuner_status_json))
            await asyncio.sleep(TIME_BETWEEN_POLLS)
    finally:
        connected_websockets.remove(websocket)

if __name__ == "__main__":
    flask_thread_handle = Thread(target = flask_thread, daemon = True)
    flask_thread_handle.start()

    tuner_thread_handle = Thread(target = tuner_control_thread, daemon = True)
    tuner_thread_handle.start()

    asyncio.set_event_loop(asyncio.new_event_loop())
    websockets_server = websockets.serve(websocket_connection_handler, "0.0.0.0", 7030)
    asyncio.get_event_loop().run_until_complete(websockets_server)
    asyncio.get_event_loop().run_forever()
