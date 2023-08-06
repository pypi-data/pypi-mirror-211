from flask import Flask
from threading import Thread

object = Flask("ttwizz")
host = "0.0.0.0"
port = 8080

@object.route("/")
def on_register():
    return f"{host, port}"

def init_server():
    object.run(host = host, port = port)

def start_server():
    server = Thread(target = init_server)
    server.start()