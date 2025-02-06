import tweepy
import time
from twitter_auth import authenticate_twitter

def search_tweets(query, max_results=10):
    """Fetch recent tweets based on a query while respecting rate limits."""
    client = authenticate_twitter()

    try:
        response = client.search_recent_tweets(
            query=query,
            max_results=max_results,
            tweet_fields=["created_at", "lang"]
        )

        if response.data:
            for tweet in response.data:
                print(f"[{tweet.created_at}] {tweet.text}\n")
        else:
            print("No tweets found.")

    except tweepy.TooManyRequests as e:
        print("⚠️ Rate limit reached. Waiting before retrying...")
        time.sleep(900)  # Wait 15 minutes before retrying

    except tweepy.TweepyException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        search_tweets("AI OR Machine Learning OR Data Science", max_results=10)
        time.sleep(60)  # Adjusted delay to avoid hitting rate limits
