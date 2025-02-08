import tweepy
import json
import time
from twitter_auth import authenticate_twitter
from preprocess import clean_tweet

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
            with open("tweets.json", "a") as file:
                for tweet in response.data:
                    cleaned_text = clean_tweet(tweet.text)  # Preprocess text
                    json.dump({"created_at": tweet.created_at.isoformat(), "text": cleaned_text}, file)
                    file.write("\n")
                    print(f"Saved Cleaned Tweet: {cleaned_text}")

        else:
            print("No new tweets found.")

    except tweepy.TooManyRequests as e:
        print("⚠️ Rate limit reached. Waiting before retrying...")
        time.sleep(900)  # Wait 15 minutes before retrying

    except tweepy.TweepyException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        search_tweets("AI OR Machine Learning OR Data Science", max_results=10)
        time.sleep(60)  # Adjusted delay to avoid hitting rate limits
