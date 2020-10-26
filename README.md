# Surge_pricing

## Introduction

Companies like Uber, Lyft, and other taxi services, increase taxi fares when there are more ride requests in a particular area. They do this in order to make sure that the cabs are available for those people who are willing to pay the higher fare. Let us consider a common scenario where a person pays $20 to watch a game and then pays $80 for a cab ride to go back home makes anyone upset.

This leads to the goal of the project.I’m showing the real-time price surge in different locations on a map. The price surge is shown as a multiplier like is it 1.8 times the normal fare or twice the normal fare. The multiplier is based on the number of pickup requests at that particular location.
So if a ride usually costs 20$ at a place during off-peak hours, it may cost $30 if the multiplier is 1.5 and the multiplier can keep on increasing like 1.8 or twice the normal fare if the number of requests is also increasing.

How is this useful for drivers and passengers?
The profit ratio between the driver and a cab company is 80:20. So a driver gets 80% of the fare. If the driver knows that there is a price surge in a particular location then he could go there to get a pickup request as he would get paid more.
Users can decide whether they are willing to pay the higher fare or wait and request at a later time or request the ride at a place nearby where there is no price surge.
Companies can also use this data to introduce features like low fares during off-peak hours and direct drivers to the place where there is a price surge in order to fulfill more pickup requests.



[Presentaion Link](https://docs.google.com/presentation/d/1k4JkmKybe1vA3XIKXbkomEsgG9qJASuMiKjh6ghnXZA/edit?usp=sharing)

## Output
![alt text](https://github.com/gsekkila/Surge_pricing/blob/master/Images/output.gif)

## Architecture
![alt text](https://github.com/gsekkila/Surge_pricing/blob/master/Images/techstack.png)
My dataset is in S3. I’m using Kafka for ingesting the real-time data and sending it to Spark. Processing tasks such as clustering the locations, and calculating price multiplier count are all done in spark. From spark, I’m sending the processed data to Redis and PostgreSQL database. PostgreSQL is used for permanent storage of the data. Redis is used as a temporary in-memory storage for the processed data and is used for accessing the data by the visualization tool dash

## Dataset

I'm using the taxi trip dataset from the City of Chicago [website.](https://data.cityofchicago.org/Transportation/Taxi-Trips/wrvz-psew) It is about 75GB in size and has more than 200 million records. The dataset contains the taxi trip records from 2013 to present. I am using this dataset to sumlate my real time data.

## Engineering challenges
### Clustering Locations
One of the difficulties that I faced is determining which requests are nearby. Since data comes in a high velocity there is very little time to cluster the locations and calculate the multiplier count. I started with calculating the distance between each points using euclidean distance. This took alot of processing time.
![alt text](https://github.com/gsekkila/Surge_pricing/blob/master/Images/chal1.png)
I ended up solving this by forming a radius around a location to determine which other ride requests affect the current request. The radius is 0.5km/0.3mi. This reduced the processing time from calculating the distance to just checking if the doppin is within the radius.
![alt text](https://github.com/gsekkila/Surge_pricing/blob/master/Images/chal2.png)
### Redis database access
Initially, I was using different database tools. I chose to PostgreSQL. It does a great job of storing data. But I wanted to use a much faster tool for accessing the data. That’s how I decided to use Redis. It is a cache-based database. It works on RAM memory so it is much faster compared to other relational databases.
Redis is a temporary storage solution for quick retrieval of information and PostgreSQL acts as a permanent storage of real time data  so it can be used in the future by other engineers for the analysis of historical data
#### Benchmarks
![alt text](https://github.com/gsekkila/Surge_pricing/blob/master/Images/bench1.png)
![alt text](https://github.com/gsekkila/Surge_pricing/blob/master/Images/bench2.png)
