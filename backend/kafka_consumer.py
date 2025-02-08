from kafka import KafkaConsumer
import json

KAFKA_TOPIC = "tweets"
KAFKA_SERVER = "localhost:9093"

def consume_tweets():
    """Consumes tweets from a Kafka topic."""
    
    consumer = KafkaConsumer(KAFKA_TOPIC,
                             bootstrap_servers=KAFKA_SERVER,
                             auto_offset_reset="earliest",
                             value_deserializer=lambda x: json.loads(x.decode("utf-8")))
    
    print("🟢 Listening for tweets...")
    for message in consumer:
        tweet = message.value
        print(f"📩 Received from Kafka: {tweet['text']}")

if __name__ == "__main__":
    consume_tweets()