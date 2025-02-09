from kafka import KafkaConsumer
import json
import mysql.connector
from nltk.sentiment import SentimentIntensityAnalyzer

# Kafka Configuration
KAFKA_TOPIC = "tweets"
KAFKA_SERVER = "localhost:9093"

# MySQL Configuration
DB_NAME = "sentiment_db"
DB_USER = "root"
DB_PASSWORD = ""
DB_HOST = "localhost"
DB_PORT = "3306"

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Connect to MySQL
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = conn.cursor()

# Create Table if Not Exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS tweet_sentiments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tweet TEXT NOT NULL,
    sentiment_score FLOAT NOT NULL,
    sentiment_label VARCHAR(10) NOT NULL
);
""")
conn.commit()

def classify_sentiment(score):
    """Classify sentiment based on score."""
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def process_tweets(max_tweets=10):  # Process only 10 tweets and exit
    """Consume tweets from Kafka, analyze sentiment, and store in MySQL."""
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    print("🟢 Listening for tweets and analyzing sentiment...")

    count = 0
    for message in consumer:
        tweet = message.value["text"]
        
        # Sentiment Analysis
        sentiment_score = sia.polarity_scores(tweet)["compound"]
        sentiment_label = classify_sentiment(sentiment_score)

        # Store in MySQL
        cursor.execute(
            "INSERT INTO tweet_sentiments (tweet, sentiment_score, sentiment_label) VALUES (%s, %s, %s)",
            (tweet, sentiment_score, sentiment_label)
        )
        conn.commit()

        print(f"📩 Tweet: {tweet}")
        print(f"🔍 Sentiment: {sentiment_label} (Score: {sentiment_score})\n")

        count += 1
        if count >= max_tweets:  # Exit after processing 'max_tweets' messages
            print("✅ Processed max tweets. Exiting...")
            break

    consumer.close()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    process_tweets(max_tweets=10)  # Change the number as needed
