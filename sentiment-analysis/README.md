# Politics Sentiment Analysis

This repository contains utilities for performing sentiment analysis on political tweets. It is designed to facilitate the analysis of public sentiment surrounding various political candidates through data streaming.

## Directory Structure

### 1. [Parser](/sentiment-analysis/parser.py)
- **Description**: This class contains methods for parsing a raw dataset of political tweets and assigning a candidate label to each entry based on the referenced candidate. 
- **Usage**: This parsing should be performed before initializing data streaming with Kafka.

### 2. [Politics](/sentiment-analysis/politics.py)
- **Description**: This class includes methods for preprocessing tweets into a suitable format for the sentiment analysis model. It also features an analysis method that predicts the sentiment of each tweet and returns scores categorized as negative, neutral, or positive.

### 3. [Main](/sentiment-analysis/main.py)
- **Description**: This script provides an example of how to use the above classes with a Pandas DataFrame.

## Important Note
Before handling the streaming data, the `SentimentAnalyzer` class must be instantiated. It is essential to broadcast this instance to each node in your streaming architecture. For detailed instructions, please refer to the [tutorial](/sentiment-analysis/ML%20inference%20in%20Spark.md).