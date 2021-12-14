import sys
from operator import add
import pyspark
from pyspark.sql import SparkSession
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.context import SparkContext
from sklearn.feature_extraction.text import CountVectorizer

import re
def pre_precess(text):
    text = text.lower()
    tagfree = re.compile('<.*?>')
    text = re.sub(tagfree, '', text)
    text = re.sub('[^A-Za-z0-9]+', ' ', text)
    return text


#if __name__ == "__main__":
def extract_keywords(data) :
    # text_file = open("data.txt", "r")
    # data = text_file.read()
    # text_file.close()
    data = pre_precess(data)



    sc = SparkContext('local')
    spark = SparkSession\
        .builder\
        .appName("PythonWordCount")\
        .getOrCreate()
    data_rdd = sc.parallelize([data])
    lines = sc.textFile("data.txt")

    counts = data_rdd.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    output = counts.collect()
    output = sorted(output, key = lambda x:x[1])
    for (word, count) in output:
        print("%s: %i" % (word, count))
    spark.stop()