from kafka import KafkaProducer
import json
import csv
from confluent_kafka.admin import AdminClient, NewTopic



def create_kafka_topic(topic_name, num_partitions=1, replication_factor=1, servers="localhost:9092,localhost:9093,localhost:9094"):
    """Creates a Kafka topic with the specified name, partitions, and replication factor."""
    admin_client = AdminClient({"bootstrap.servers": servers})

    topic = NewTopic(topic=topic_name, num_partitions=num_partitions, replication_factor=replication_factor)

    fs = admin_client.create_topics([topic])
    for topic, f in fs.items():
        try:
            f.result()
            print(f"Topic '{topic_name}' created successfully.")
        except Exception as e:
            print(f"Failed to create topic '{topic_name}': {e}")


def produce_tweets(topic_name, servers="localhost:9092,localhost:9093,localhost:9094"):
    producer = KafkaProducer(bootstrap_servers=servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    csv_file = '../twitter-scraper/tweets.csv'
    
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

    
    producer.flush()
    producer.close()

create_kafka_topic('tweets',2,3,"localhost:9092,localhost:9093,localhost:9094")
produce_tweets('tweets',"localhost:9092,localhost:9093,localhost:9094")