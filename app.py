from flask import Flask
from flask_cors import CORS
from flask import request
import requests
import wordcount
import json
import heapq
from flask.json import jsonify

app = Flask(__name__)
url = "https://findwork.dev/api/jobs/"
CORS(app)

@app.route('/')
def hello_world():
    return "hello world"

@app.route("/get_jobs/<string:type>", methods=['POST'])
def get_job(type):
    postJson = request.get_json()
    if "skills" in postJson:
        given_scores = postJson["skills"]
    else :
        return jsonify({
            "error" : "please provide skills in the HTTP request body"
        })
    
    # request target API and get responses
    get_job_url = url + "?search=" + type
    results = get_page(get_job_url)

    # send each job information to the spark util 
    wc = wordcount.Wordcount()
    scores = []
    for i in range(len(results)):
        score = wc.extract_keywords(json.dumps(results[i]), given_scores)
        heapq.heappush(scores, (score,i))
    
    #return results with top 20% score
    recommend_num = int(len(results) * 0.2)
    while len(scores) > recommend_num:
        heapq.heappop(scores)
    
    recommend_results = []
    for score, index in scores:
        results[index]["score"] = score
        recommend_results.append(results[index])
    if len(recommend_results) == 0 :
        return jsonify({
            "error" : "cannot find matching jobs"
        })
    return jsonify(recommend_results)


# util method for requesting url and parsing json
def get_page(get_job_url):
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
            results = results + get_page(next_url)
    return results
    
if __name__ == '__main__':
    app.run()
