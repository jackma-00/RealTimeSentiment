#!/bin/bash

sleep 10
python3 ./src/kafka-create-topic.py 
python3 ./src/consumer.py