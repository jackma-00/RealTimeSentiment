import random


class SentimentAnalyzer:
    def __init__(self):
        """
        Initializes the SentimentAnalysis class.

        Attributes:
            labels (list): A list containing sentiment labels, ["Negative", "Positive"].
        """
        self.labels = ["Negative", "Positive"]

    def analyze_sentiment(self, text: str) -> str:
        """
        Analyzes the sentiment of the given text and returns a sentiment label.

        Args:
            text (str): The text to analyze.

        Returns:
            str: The sentiment label for the given text.
        """
        sentiment = random.choice(self.labels)
        return sentiment
