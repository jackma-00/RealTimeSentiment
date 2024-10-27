from confluent_kafka.admin import AdminClient, NewTopic


def create_kafka_topic(
    topic_name,
    num_partitions=1,
    replication_factor=1,
    servers="kafka1:19092,kafka2:19093,kafka3:19094",
):
    admin_client = AdminClient({"bootstrap.servers": servers})
    topic = NewTopic(
        topic=topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor,
    )
    try:
        fs = admin_client.create_topics([topic])
        top = fs[topic_name]
        try:
            top.result()
            print(f"Topic '{topic_name}' created successfully.")
        except Exception as e:
            print(f"Failed to create topic '{topic_name}': {e}")
    except Exception as e:
        print(f"Failed to create topic '{topic_name}': {e}")


create_kafka_topic("trump_tweets", 2, 3, "kafka1:19092,kafka2:19093,kafka3:19094")
create_kafka_topic("kamala_tweets", 2, 3, "kafka1:19092,kafka2:19093,kafka3:19094")
