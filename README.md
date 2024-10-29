# Real-Time Sentiment Analysis Project

## Overview
This project is part of the ID2221 Data-Intensive Computing course. It involves designing and implementing a real-time data streaming system for sentiment analysis on political tweets. The system utilizes Hugging Face's transformer library to perform sentiment analysis and Apache Spark to handle a data stream.

This repository contains a demo of a data intensive application. The application is a complete data pipeline that ingests data from a source, processes it, and stores it in a database. The application is implemented in Python and uses the following technologies:
- [Kafka](https://kafka.apache.org/) for the message broker
- [Spark](https://spark.apache.org/) for the data processing
- [Transformer](https://huggingface.co/docs/transformers/en/index) for sentiment analysis
- [MongoDB](https://www.mongodb.com/) for the database

Find a detailed description of the project architecture in the [project report](/project-report.pdf).

### Requirements

To run this project, you only need to have Docker and Docker Compose installed on your machine. Docker Compose will handle the setup and orchestration of all the necessary services.

### Run

To start the entire application, simply run the following command in the root directory of the project:

```bash
docker-compose up --build
```

This command will build and start all the services defined in the 

docker-compose.yml

 file. The application will be up and running, and you can access the dashboard at [localhost:1323](http://localhost:1323/).
