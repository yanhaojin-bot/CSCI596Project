from flask import Flask
from flask_cors import CORS
from flask import request
import requests
import wordcount
import json

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
    results = []
    responseDict = response.json()

    if "results" in responseDict:
        results = responseDict["results"]
    if "next" in responseDict:
        next_url = responseDict["next"]
        results = results + get_next_page(next_url)
    returnResults = {}
    returnResults["results"] = results
    print(len(results))
    wc = wordcount.Wordcount()
    scores = []
    given_scores = {
        "swift" : 4,
        "android" : 2,
        "objectivec" : 3
    }
    for result in results:
        score = wc.extract_keywords(json.dumps(result), given_scores)
        scores.append(score)

    return returnResults

def get_next_page(get_job_url):
    payload={}
    headers = {'Authorization': 'Token 9fe56153c850546257b47713c1cb9810ce7d441b'}
    response = requests.request("GET", get_job_url, headers=headers, data=payload)
    results = []
    responseDict = response.json()
    print(get_job_url)
    if "results" in responseDict:
        results = responseDict["results"]
    if "next" in responseDict:
        next_url = responseDict["next"]
        if next_url is not None:
            results = results + get_next_page(next_url)
    return results
    
if __name__ == '__main__':
    app.run()
