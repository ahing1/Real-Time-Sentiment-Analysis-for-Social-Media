from kafka import KafkaConsumer
import json
import mysql.connector
import os
from dotenv import load_dotenv
from textblob import TextBlob

load_dotenv()

# MySQL Configuration
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

# Kafka Configuration
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_SERVER = os.getenv("KAFKA_SERVER")

def get_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return "Positive"
    elif analysis.sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

# Kafka Consumer Setup
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_SERVER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print(f"Listening for messages on topic: {KAFKA_TOPIC}")

for message in consumer:
    tweet_data = message.value
    print(f"Received Tweet: {tweet_data}")

    try:
        if "sentiment" not in tweet_data:
            tweet_data["sentiment"] = get_sentiment(tweet_data["text"])

        # Connect to MySQL
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if tweet already exists (to prevent duplicates)
        check_query = "SELECT COUNT(*) FROM tweet_sentiments WHERE tweet_text = %s"
        cursor.execute(check_query, (tweet_data["text"],))
        result = cursor.fetchone()

        if result[0] > 0:
            print("⚠️ Tweet already exists in database. Skipping.")
        else:
            # Insert tweet into MySQL
            insert_query = "INSERT INTO tweet_sentiments (tweet_text, sentiment_label) VALUES (%s, %s)"
            cursor.execute(insert_query, (tweet_data["text"], tweet_data["sentiment"]))
            conn.commit()
            print("✅ Tweet stored in MySQL!")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error storing tweet: {e}")