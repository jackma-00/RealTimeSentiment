from transformers import AutoModelForSequenceClassification, AutoTokenizer
import numpy as np
from scipy.special import softmax
import re


MODEL = "cardiffnlp/xlm-twitter-politics-sentiment"


class SentimentAnalyzer:
    def __init__(self):
        """
        Initializes the sentiment analysis model.

        This constructor sets up the tokenizer and model for sequence classification
        using a pre-trained model specified by the `MODEL` constant. It also defines
        the labels used for classification.

        Attributes:
            tokenizer (AutoTokenizer): Tokenizer for processing input text.
            model (AutoModelForSequenceClassification): Pre-trained model for sequence classification.
            labels (list): List of sentiment labels ['Negative', 'Neutral', 'Positive'].
        """
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        self.labels = ['Negative', 'Neutral', 'Positive']

    def preprocess_text(self, text: str) -> str:
        """
        Preprocesses the input text by performing the following operations:
        1. Removes URLs.
        2. Removes mentions (e.g., @username).
        3. Removes hashtags (e.g., #hashtag).
        4. Removes non-alphabetic characters.
        5. Removes extra whitespaces.
        6. Converts text to lowercase and strips leading/trailing whitespaces.

        Args:
            text (str): The input text to preprocess.

        Returns:
            str: The preprocessed text.
        """
        text = re.sub(r"http\S+", "", text)  # Remove URLs
        text = re.sub(r"@\w+", "", text)  # Remove mentions
        text = re.sub(r"#\w+", "", text)  # Remove hashtags
        text = re.sub(r"[^A-Za-z\s]", "", text)  # Remove non-alphabetic characters
        text = re.sub(r"\s+", " ", text)  # Remove extra whitespaces
        text = text.lower().strip()  # Convert to lowercase and strip

        return text

    def analyze_sentiment(self, text: str, preprocess: bool = True) -> tuple[np.ndarray, str]:
        """
        Analyzes the sentiment of the given text.
        Args:
            text (str): The input text to analyze.
            preprocess (bool, optional): Whether to preprocess the input text. Defaults to True.
        Returns:
            tuple[np.ndarray, str]: A tuple containing the sentiment scores as a numpy array and the predominant sentiment label.
        """
        # Preprocess the input text
        if preprocess:
            text = self.preprocess_text(text)
        
        # Tokenize input and run the model
        encoded_input = self.tokenizer(text, return_tensors='pt')
        output = self.model(**encoded_input)
        
        # Convert the model output (logits) into probabilities using softmax
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        
        # Find the predominant label
        max_index = np.argmax(scores)
        predominant_label = self.labels[max_index]
        
        return scores, predominant_label

    def print_results(self, text: str):
        """
        Analyzes the sentiment of the given text and prints the results.
        Args:
            text (str): The text to be analyzed.
        The method performs the following steps:
        1. Runs sentiment analysis on the provided text.
        2. Prints the sentiment scores for each label.
        3. Prints the predominant sentiment label.
        Example:
            self.print_results("This is a sample text.")
        """
        # Run sentiment analysis
        scores, predominant_label = self.analyze_sentiment(text)
        
        # Print the input text
        print(f"Text: {text}")

        # Print scores for each label
        for i in range(len(self.labels)):
            print(f"{self.labels[i]}: {scores[i]}")
        
        # Print the predominant label
        print(f"Predominant label: {predominant_label}")
        print()

