from flask import Flask, request
import yaml
import requests
import logging
import traceback
import socket
host=socket.gethostname()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def inhello():
    
    return "Hi Srikar Version2! ==> from "+host, 200


@app.route('/healthz', methods=['GET'])
def index():
    return "Healthy Probe Version2- ==>"+host, 200


@app.route('/ready', methods=['GET'])
def indexi():
    return "Ready Probe Version2--------------------!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8085)
