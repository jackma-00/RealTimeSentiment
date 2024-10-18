from sentiment_analysis.politics import SentimentAnalyzer

analyzer = SentimentAnalyzer()

print(analyzer.analyze_sentiment("I love this product! It's amazing.")[1])