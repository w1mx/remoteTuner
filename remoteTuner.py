#!/usr/bin/env python3

from flask import Flask, current_app

app = Flask(__name__)

@app.route('/')
def index():
    return current_app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 7020)
