docker exec -it kafka1 /bin/sh
# create a topic example
/bin/kafka-topics.sh --create --topic tweets --bootstrap-server 127.0.0.1:9092 --replication-factor 1 --partitions 1

# list all topics
/bin/kafka-topics.sh --list --bootstrap-server 127.0.0.1:9092

# see events in a topic
/bin/kafka-console-consumer.sh --topic tweets --from-beginning --bootstrap-server localhost:9092
