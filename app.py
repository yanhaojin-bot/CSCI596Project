from flask import Flask
from flask_cors import CORS
from flask import request
import requests

app = Flask(__name__)
url = "https://findwork.dev/api/jobs/"
CORS(app)

@app.route('/')
def hello_world():
    return "hello world"

@app.route("/get_jobs/<string:type>")
def get_job(type):
    payload={}
    get_job_url = url + "?search=" + type
    headers = {'Authorization': 'Token 9fe56153c850546257b47713c1cb9810ce7d441b'}
    response = requests.request("GET", get_job_url, headers=headers, data=payload)
    return response.json()

if __name__ == '__main__':
    app.run()
