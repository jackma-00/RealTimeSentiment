# python-kafka

For installing the required packages, run the following command:
```bash
pip install -r requirements.txt
```
For running the script, run the following command:
```bash
python kafka.py
```



docker exec -it kafka /bin/sh
# create a topic example
/opt/bitnami/kafka/bin/kafka-topics.sh --create --topic tweets --bootstrap-server 127.0.0.1:9092 --replication-factor 1 --partitions 1

# list all topics
/opt/bitnami/kafka/bin/kafka-topics.sh --list --bootstrap-server 127.0.0.1:9092

# see events in a topic
/opt/bitnami/kafka/bin/kafka-console-consumer.sh --topic tweets --from-beginning --bootstrap-server localhost:9092
