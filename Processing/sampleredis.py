from pyspark import *

full_df = spark.read.csv("pantheon.tsv", sep="\t", quote="", header=True, inferSchema=True)

data.write.format("org.apache.spark.sql.redis").option("table", "people").option("key.column", "en_curid").save()

data = full_df.select("en_curid", "countryCode", "occupation")
data.show(2)
data.write.format("org.apache.spark.sql.redis").option("table", "people").option("key.column", "en_curid").save()

