# python-spark

For installing the required packages, run the following command:
```bash
pip install -r requirements.txt
```

Once the kafka server is up and running, to creating a topic, run the following command:
```bash
python kafka-create-topic.py
```

Once the topic has been created, run the following command to subscribe the spark session to the topic and then store unique tweets and voter sentiments in the mongo database:
```bash
python consumer.py
```