import org.apache.spark.sql.functions.from_json


val spark = SparkSession
 .builder
 .appName("Spark-Kafka-Integration")
 .master("local")
 .getOrCreate()


spark
  // Read the data
  .readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "10.0.0.14:9092") 
  .option("subscribe", "location")
  .load()
