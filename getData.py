import json
import pandas as pd
import os

from helperScraper import login_and_scrape_tweets, scrape_article

def save_tweets_to_json(data, filename="tweets.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str)
    except Exception as e:
        print(f"Error saving tweets to JSON: {e}")

def save_article_to_json(article, filename="articles.json"):
    try:
        if isinstance(article, pd.DataFrame):
            article.to_json(filename, orient="records", indent=4)  # ✅ Proper DataFrame to JSON
        else:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(article, f, indent=4, default=str)
    except Exception as e:
        print(f"Error saving articles to JSON: {e}")

def clean_tweets():
    try:
        tweets_df = pd.read_json("tweets.json")

        # Remove duplicates and clean tweets
        tweets_df["content"] = tweets_df["content"].str.replace(r"http\S+|www\S+|bit.ly\S+", "", regex=True)
        tweets_df["content"] = tweets_df["content"].str.replace(r"[^a-zA-Z0-9#@ ]", "", regex=True)
        tweets_df["content"] = tweets_df["content"].str.replace(r"\s+", " ", regex=True).str.strip().str.lower()

        # Drop duplicates based on cleaned content
        tweets_df.drop_duplicates(subset=["content"], inplace=True)

        # Save cleaned data
        tweets_df.to_json("cleaned_tweets.json", orient="records", indent=4)

        print(f"Cleaned {len(tweets_df)} unique tweets.")
    except Exception as e:
        print(f"Error in clean_tweets: {e}")

def clean_article():
    try:
        articles_df = pd.read_json("articles.json")

        if "text" not in articles_df.columns:
            raise ValueError("articles.json does not contain 'text' column.")

        # Clean text
        articles_df["text"] = articles_df["text"].str.replace(r"[\n]+", " ", regex=True)  # Remove newlines
        articles_df["text"] = articles_df["text"].str.replace(r"[^a-zA-Z0-9.,!? ]", "", regex=True)  # Remove special chars
        articles_df["text"] = articles_df["text"].str.lower().str.strip()  # Lowercase and trim spaces

        # Save cleaned data
        articles_df.to_json("cleaned_articles.json", orient="records", indent=4)

    except Exception as e:
        print(f"Error in clean_article: {e}")


def getData(url_list, search_queries):
    try:
        if(os.getenv("ARTICLE_FLAG")):
            print("Scraping articles now")
            article_content = scrape_article(url_list)
            save_article_to_json(article_content)
            clean_article()
        if(os.getenv("TWEET_FLAG")):
            print("Scraping tweets now")
            tweets_df = login_and_scrape_tweets(search_queries)

            if not isinstance(tweets_df, pd.DataFrame):
                raise ValueError("login_and_scrape_tweets did not return a DataFrame.")

            save_tweets_to_json(tweets_df.to_dict(orient="records"))

            clean_tweets()

        return "Success"

    except Exception as e:
        print(f"Error in getData: {e}")
        return str(e)