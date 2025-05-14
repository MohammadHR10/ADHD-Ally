from transformers import pipeline
import numpy as np

class MLFeatures:
    def __init__(self):
        # Initialize sentiment analysis pipeline
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        
    def analyze_sentiment(self, text):
        """
        Analyze the sentiment of a text and return a score and mood label.
        
        Args:
            text (str): The text to analyze
            
        Returns:
            tuple: (sentiment_score, mood_label)
        """
        try:
            # Get sentiment analysis
            result = self.sentiment_analyzer(text)[0]
            score = result['score']
            label = result['label']
            
            # Convert label to mood
            mood_map = {
                'POSITIVE': 'happy',
                'NEGATIVE': 'sad',
                'NEUTRAL': 'neutral'
            }
            mood = mood_map.get(label, 'neutral')
            
            return score, mood
            
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            return 0.5, 'neutral'  # Default values if analysis fails

# Create a singleton instance
ml_features = MLFeatures() 