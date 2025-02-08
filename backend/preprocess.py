import re

def clean_tweet(text):
    """Cleans tweet text by removing URLs, mentions, and hashtags."""
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
    text = re.sub(r"@\w+", "", text)  # Remove mentions
    text = re.sub(r"#\w+", "", text)  # Remove hashtags
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    return text.strip()

# Example usage:
tweet = "Check out this amazing AI tool! 🚀 #MachineLearning http://example.com"
print(clean_tweet(tweet))  # Output: "Check out this amazing AI tool"
