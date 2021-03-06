# CSCI596Project

# Overview

## Background
Each year there are about 189,200 openings for software engineering related jobs, according to the data from U.S. Bureau of Labor Statistics [1]. Different positions may expect candidates with different experience and technical skills. In this case, as applicants, we want to know whether our skills are matched with the requirements of some specific positions by scanning their job descriptions. 

## Spark

Apache Spark is a lightning-fast cluster computing designed for fast computation. Spark processes data in RAM using a concept known as an RDD, Resilient Distributed Dataset.

![SparkDiagram](/img/SparkDiagram.png)

Spark makes it easy to combine different processing models seamlessly in the same application, such as data classification with machine learning library, streaming data via Spark Streaming and data query through Spark SQL.

Spark is built on top of the Scale programming language but we can use the Python API for running Spark (PySpark). 


## Scope

- Setup a proxy server and fetch job information from Findwork job API when a client requests the server. 
- Utilize Spark as the parallel processing tool to extract keywords from a list of job descriptions. 
- Calculate the cosine similarity between keywords provided by the client and the keywords extracted from the list.
- Return a list of matching results to the client. 


## Usage
- In this example, we want to find the ios related job and the skills and weight coefficients we provide are swift : 4, android : 2, objective-c : 3. Note: a skill with a larger coefficient means that skill has more weight in the process of the recommendation.

- Start the flask program by following commands on the terminal:

```
cd CSCI596Project
export FLASK_APP=app.py
flask run -h 0.0.0.0
```

- We send a POST request to http://localhost:5000/get_jobs/ios with a json body: (Note: The server is deployed on 20.114.29.101)
```
{
    "skills": {
        "swift": 4,
        "android": 2,
        "objective-c": 3
    }  
}
```

- We can receive the json data with recommendated job information.


## Results

![SparkDiagram](/img/result.png)

## Environment

- Ubuntu 18.04
- Python 3.6.9
- Spark 3.2
- Flask 0.12.2

[1] https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm
