#!/usr/bin/env python3

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

async def websocket_connection_handler(websocket, path):
    print("Conn")
    name = await websocket.recv()
    print(name)
    await websocket.send(name)

if __name__ == "__main__":
    flask_thread_handle = Thread(target = flask_thread, daemon = True)
    flask_thread_handle.start()

    asyncio.set_event_loop(asyncio.new_event_loop())
    websockets_server = websockets.serve(websocket_connection_handler, "0.0.0.0", 7030)
    asyncio.get_event_loop().run_until_complete(websockets_server)
    asyncio.get_event_loop().run_forever()
