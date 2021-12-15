import sys
from operator import add
import pyspark
from pyspark.sql import SparkSession
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.context import SparkContext
from sklearn.feature_extraction.text import CountVectorizer
from scipy import spatial

import re
class Wordcount:
    def __init__(self) -> None:
        self.sc = SparkContext('local')
        #self.spark = SparkSession.builder.master("Cluster").appName(name).getOrCreate()
        pass
    def pre_precess(self, text):
        text = text.lower()
        tagfree = re.compile('<.*?>')
        text = re.sub(tagfree, '', text)
        text = re.sub('[^A-Za-z0-9]+', ' ', text)
        return text


    def extract_keywords(self, data, given_scores):
        
        spark = SparkSession.builder.getOrCreate()
        data = self.pre_precess(data)
        data_rdd = self.sc.parallelize([data])
        counts = data_rdd.flatMap(lambda x: x.split(' ')) \
            .map(lambda x: (x, 1)) \
            .reduceByKey(add)
        output = counts.collect()
        output = dict(sorted(output, key=lambda x: x[1]))
        output_scores = []
        for skill, fraq in given_scores.items():
            if skill in output:
                output_scores.append(fraq)
            else:
                output_scores.append(0)
        given_scores = list(given_scores.values())
        print(given_scores)
        print(output_scores)
        result = 1 - spatial.distance.cosine(given_scores, output_scores)
        print(result)
        return result
        # for (word, count) in output:
        #    print("%s: %i" % (word, count))
        #spark.stop()
