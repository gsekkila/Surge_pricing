import sys

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

if __name__ == "__main__":
    


    zkQuorum = "10.0.0.14:9092"
    topic = "word"


    spark = SparkSession.builder.appName("PythonWordcount").getOrCreate()
    sc = spark.sparkContext
    ssc = StreamingContext(sc, 20)

    kvs = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list": zkQuorum})
    lines = kvs.map(lambda x: x[1])
    counts = lines.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
