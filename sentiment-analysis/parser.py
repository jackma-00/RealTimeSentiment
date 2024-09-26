from pandas import DataFrame

class TweetParser:
    def parse_tweets(self, tweets: DataFrame, label: str = "__label__neutral") -> list[dict]:
        # Check for NaN values in the DataFrame and drop them
        tweets = tweets.dropna(subset=['user', 'tweet'])
        
        # Create a list of dictionaries
        data = [
            {
                "user": row["user"].strip(),
                "tweet": row["tweet"],
                "who": label
            }
            for _, row in tweets.iterrows()
        ]
        
        return data
    
    def parse_tweets_as_df(self, tweets: DataFrame, label: str = "__label__neutral") -> DataFrame:
        # Check for NaN values in the DataFrame and drop them
        tweets = tweets.dropna(subset=['user', 'tweet']).copy()
        
        # Add the "who" column to the DataFrame
        tweets.loc[:, "who"] = label
        
        # Ensure "user" has no leading/trailing whitespace
        tweets.loc[:, "user"] = tweets["user"].str.strip()
        
        return tweets
