#!/bin/bash

sleep 10

python3 /code/src/kafka-create-topic.py &
python3 /code/src/consumer.py