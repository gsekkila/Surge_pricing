import json
import re

from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
#spark = SparkSession.builder.appName("Test").getOrCreate()


spark = SparkSession \
        .builder \
        .appName("PySpark Structured Streaming with Kafka Demo") \
        .getOrCreate()

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "10.0.0.13:9092") \
  .option("subscribe", "location") \
  .load()
df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
