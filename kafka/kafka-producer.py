import time
from kafka import KafkaProducer
from confluent_kafka.admin import AdminClient  
import json
import csv
import concurrent.futures

def wait_for_topics(topic_names, servers="kafka1:19092,kafka2:19093,kafka3:19094"):
    admin_client = AdminClient({"bootstrap.servers": servers})

    while True:
        topics = admin_client.list_topics(timeout=10).topics
        if all(topic in topics for topic in topic_names):
            print("All topics exist.")
            break
        print("Waiting for topics to be created...")
        time.sleep(1)

def produce_tweets(topic_name, csv_file, servers="kafka1:19092,kafka2:19093,kafka3:19094"):
    producer = KafkaProducer(bootstrap_servers=servers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file, fieldnames=['username', 'tweet'], delimiter='\t')

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
            time.sleep(1)

    producer.flush()
    producer.close()

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        wait_for_topics(['trump_tweets', 'kamala_tweets'])
        
        future_trump = executor.submit(produce_tweets, 'trump_tweets', './twitter-scraper/tweets.csv')
        future_kamala = executor.submit(produce_tweets, 'kamala_tweets', './twitter-scraper/kamala_tweets.tsv')

        concurrent.futures.wait([future_trump, future_kamala])
