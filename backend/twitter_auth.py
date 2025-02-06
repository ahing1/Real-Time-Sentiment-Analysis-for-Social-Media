import tweepy
from config import BEARER_TOKEN

def authenticate_twitter():
    """Authenticate using Twitter API v2 (Recent Search)"""
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    return client
