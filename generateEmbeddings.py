import boto3
import json

from getData import getData

def save_embeddings():
    try:
        # Save cleaned up extracted data into files
        status = getData()
        if status != "Success":
            raise Exception({'message': status})

        # Load cleaned tweets
        with open("cleaned_tweets.json", "r", encoding="utf-8") as f:
            tweets = json.load(f)

        # Load cleaned articles
        with open("cleaned_articles.json", "r", encoding="utf-8") as f:
            articles = json.load(f)
    except Exception as e:
        return e