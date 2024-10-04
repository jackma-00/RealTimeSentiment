import time
from kafka import KafkaProducer
import json
import csv


def produce_tweets(topic_name, csv_file, servers="localhost:9092,localhost:9093,localhost:9094"):
    producer = KafkaProducer(bootstrap_servers=servers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(
            file, fieldnames=['username', 'tweet'], delimiter='\t')

        for row in reader:
            if row['username'] and row['tweet']:
                message = {
                    'username': row['username'].strip(),
                    'tweet': row['tweet'].strip()
                }
                producer.send(topic_name, value=message)
                print(f"Sent: {message}")
            else:
                print(f"Skipping malformed row: {row}")
            time.sleep(0.25)

    producer.flush()
    producer.close()


produce_tweets('trump_tweets', '../twitter-scraper/tweets.csv',"localhost:9092,localhost:9093,localhost:9094")
produce_tweets('kamala_tweets','../twitter-scraper/khamal_tweets.tsv', "localhost:9092,localhost:9093,localhost:9094")