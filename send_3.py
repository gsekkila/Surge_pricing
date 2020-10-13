import re
import boto3
import time
import pandas as pd
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
from bson import json_util
from json import dumps
import json
import numpy as np

client = boto3.client('s3',aws_access_key_id = 'AKIAIIMFOAGXD77MOKEA', aws_secret_access_key='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')

resource = boto3.resource('s3')
bucket = resource.Bucket('taxitripdata')
#cols = pd.read_csv(csv_obj['Body'],header=0,names=['latitude','longitude'], nrows=1)
#print(cols)
for i in range(10):
	csv_obj = client.get_object(Bucket='taxitripdata', Key='sample.csv')

	data = pd.read_csv(csv_obj['Body'],skiprows=i, nrows=1, usecols=[10,11]) #[['latitude','longitude']]

	producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer = lambda x: json.dumps(x).encode('utf-8'))
	jdata=data.to_json(orient='values')
	jjdata = jdata.translate({ord(x):None for x in '[]'})
	coord = jjdata.split(',')
	number = np.array(coord)
	res = np.asfarray(number,float)
	lists = res.tolist()
	res = json.dumps(lists)
	print(res)
	


	producer.send('location', res)

	print("successfully sent data to kafka topic")
	time.sleep(3)

consumer = KafkaConsumer('location', bootstrap_servers='localhost:9092')
consumer.subscribe(['location_new'])

for msg in consumer:
	print(msg)
