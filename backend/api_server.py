from fastapi import FastAPI
import mysql.connector
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import os

# MySQL Configuration
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

# Initialize FastAPI App
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sentiment-dashboard.vercel.app"],  # Allow all origins (change to specific domain if needed)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.get("/")
def home():
    return {"message": "Sentiment Analysis API is Running!"}

@app.get("/tweets")
def get_all_tweets():
    """Fetch all tweets with sentiment analysis."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM tweet_sentiments ORDER BY id DESC LIMIT 20;")
    tweets = cursor.fetchall()
    
    conn.close()
    return {"tweets": tweets}

@app.get("/tweets/{sentiment}")
def get_tweets_by_sentiment(sentiment: str):
    """Fetch tweets filtered by sentiment (Positive, Negative, Neutral)."""
    sentiment = sentiment.capitalize()  # Ensure correct casing

    if sentiment not in ["Positive", "Negative", "Neutral"]:
        return {"error": "Invalid sentiment type. Choose Positive, Negative, or Neutral."}
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM tweet_sentiments WHERE sentiment_label = %s ORDER BY id DESC LIMIT 10;", (sentiment,))
    tweets = cursor.fetchall()
    
    conn.close()
    return {"tweets": tweets}

@app.get("/stats")
def get_sentiment_stats():
    """Fetch sentiment statistics (count of Positive, Negative, Neutral tweets)."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT sentiment_label, COUNT(*) as count FROM tweet_sentiments GROUP BY sentiment_label;
    """)
    stats = cursor.fetchall()
    
    conn.close()
    return {"stats": stats}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

