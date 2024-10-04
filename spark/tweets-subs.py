from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

total_trump = 0
total_kamala = 0

def filter_and_add_tweets(batch_df, batch_id):
    existing_tweets_df = spark.read \
        .format("mongo") \
        .option("uri", "mongodb://127.0.0.1:27017/mydb.tweets") \
        .load()
    
    if existing_tweets_df.count() == 0:
        logger.info(f"No existing tweets, adding: {batch_df.count()}")
        batch_df.write \
            .format("mongo") \
            .option("uri", "mongodb://127.0.0.1:27017/mydb.tweets") \
            .mode("append") \
            .save()
        trump_counter_df = spark.createDataFrame([{"_id": "trump", "seq": batch_df.count()}]) 
        trump_counter_df.write \
            .format("mongo") \
            .option("uri", "mongodb://127.0.0.1:27017/mydb.usa2024") \
            .mode("append") \
            .save()
    else:
        new_tweets_df = batch_df.join(existing_tweets_df, (batch_df["tweet"] == existing_tweets_df["tweet"]) & (batch_df["username"] == existing_tweets_df["username"]), "leftanti")
        logger.info(f"New tweets count: {new_tweets_df.count()}")
        if new_tweets_df.count() > 0:
            new_count = new_tweets_df.count()
            new_tweets_df.write \
                .format("mongo") \
                .option("uri", "mongodb://127.0.0.1:27017/mydb.tweets") \
                .mode("append") \
                .save()

            trump_counter_df = spark.read \
                .format("mongo") \
                .option("uri", "mongodb://127.0.0.1:27017/mydb.usa2024") \
                .load()

            current_count = trump_counter_df.collect()[0]["seq"]
            updated_count = current_count + new_count
            logger.info(f"Updated count: {updated_count}")
            trump_counter_df = spark.createDataFrame([{"_id": "trump", "seq": updated_count}])
            trump_counter_df.write \
                .format("mongo") \
                .option("uri", "mongodb://127.0.0.1:27017/mydb.usa2024") \
                .mode("overwrite") \
                .save()



# Subscribe to 1 topic
spark = SparkSession.builder \
    .appName("KafkaSparkStreamingJSON") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2,"
            "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .config("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1:27017/mydb.usa2024") \
    .config("spark.mongodb.write.connection.uri", "mongodb://127.0.0.1:27017/mydb.usa2024") \
    .config("spark.mongodb.read.connection.uri", "mongodb://127.0.0.1:27017/mydb.tweets") \
    .config("spark.mongodb.write.connection.uri", "mongodb://127.0.0.1:27017/mydb.tweets") \
    .getOrCreate()

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092,localhost:9093,localhost:9094") \
    .option("subscribe", "trump_tweets") \
    .load()

json_schema = StructType() \
    .add("username", StringType()) \
    .add("tweet", StringType())

df = df.selectExpr("CAST(value AS STRING)") \
       .select(from_json(col("value"), json_schema).alias("data")) \
       .select("data.username", "data.tweet")

query = df.writeStream \
    .foreachBatch(filter_and_add_tweets) \
    .start()

query.awaitTermination()

df2 = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092,localhost:9093,localhost:9094") \
    .option("subscribe", "kamala_tweets") \
    .load()

df2 = df2.selectExpr("CAST(value AS STRING)") \
       .select(from_json(col("value"), json_schema).alias("data")) \
       .select("data.username", "data.tweet")

query2 = df2.writeStream \
    .foreachBatch(filter_and_add_tweets) \
    .start()

query2.awaitTermination()
