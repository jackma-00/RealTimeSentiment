import pandas as pd
from parser import TweetParser
from politics import SentimentAnalyzer


def main():
    # Load the tweets from the CSV file
    df = pd.read_csv("src/data/tweets.csv")
    
    # Initialize the TweetParser and SentimentAnalyzer
    parser = TweetParser()
    analyzer = SentimentAnalyzer()
    
    # Parse the tweets
    parsed_tweets = parser.parse_tweets_as_df(df, label="__label__trump")

    # Save the parsed tweets to a new CSV file
    parsed_tweets.to_csv("src/data/parsed_tweets.csv", index=False)

    # Print the sentiment analysis results for the first few tweets
    for i in range(5):
        tweet = parsed_tweets.iloc[i]
        analyzer.print_results(tweet["tweet"])

if __name__ == "__main__":
    main()