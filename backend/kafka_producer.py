from kafka import KafkaProducer
import json
import time

KAFKA_TOPIC = "tweets"
KAFKA_SERVER = "localhost:9093"

def read_tweets_from_file(filename):
    """Reads stored tweets from a JSON file."""
    
    with open(filename, "r") as file:
        tweets = [json.loads(line) for line in file.readlines()]
        
    return tweets

def send_tweets_to_kafka():
    
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                             value_serializer=lambda v: json.dumps(v).encode("utf-8"))
    
    tweets = read_tweets_from_file("tweets.json")
    
    for tweet in tweets:
        producer.send(KAFKA_TOPIC, tweet)
        print(f"✅ Sent to Kafka: {tweet['text']}")
        time.sleep(0.5)  # Add a small delay to avoid flooding the Kafka broker
    
    producer.flush()
    print("✨ All tweets sent to Kafka!")

if __name__ == "__main__":
    send_tweets_to_kafka()