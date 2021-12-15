from operator import add
from pyspark.sql import SparkSession
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.context import SparkContext
from sklearn.feature_extraction.text import CountVectorizer
from scipy import spatial

import re
class KeywordCounter:
    def __init__(self) -> None:
        self.sc = SparkContext('local')

    # precess given text: remove html tags and special characters
    def pre_precess(self, text):
        text = text.lower()
        tagfree = re.compile('<.*?>')
        text = re.sub(tagfree, '', text)
        text = re.sub('[^A-Za-z0-9\-]+', ' ', text)
        return text


    def extract_keywords(self, data, given_scores):
        data = self.pre_precess(data)
        # send data into RDD and count words
        data_rdd = self.sc.parallelize([data])
        counts = data_rdd.flatMap(lambda x: x.split(' ')) \
            .map(lambda x: (x, 1)) \
            .reduceByKey(add)
        output = counts.collect()
        output = dict(sorted(output, key=lambda x: x[1]))
        output_scores = []
        # calculate the cosine similarity of the given vector and the output vector
        for skill, fraq in given_scores.items():
            if skill in output:
                output_scores.append(fraq)
            else:
                output_scores.append(0)
        given_scores = list(given_scores.values())
        if all(v == 0 for v in output_scores) :
            return 0
        result = 1 - spatial.distance.cosine(given_scores, output_scores)
        return result
