from playwright.sync_api import sync_playwright
import time
import pandas as pd
import os

# article scraper
def scrape_article(url_list):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        article_content = []

        for url in url_list:
            print("Scraping the following URL: {}".format(url))
            try:
                page.goto(url, timeout=90000)  # Increased timeout for slow pages
                page.wait_for_load_state("networkidle")  # Ensures JavaScript content loads

                # Handle missing attributes safely
                title = page.title()
                text = page.locator("body").inner_text()  # Trim text for efficiency
                authors = page.locator("meta[name='author']").get_attribute("content") or "Unknown"
                published_date = page.locator("meta[property='article:published_time']").get_attribute("content") or "Unknown"

                article_content.append({
                    "title": title,
                    "text": text,
                    "authors": authors,
                    "published_date": published_date
                })

            except Exception as e:
                print(f"Error scraping {url}: {e}")
                article_content.append({
                    "title": "Error",
                    "text": f"Failed to scrape {url}",
                    "authors": "N/A",
                    "published_date": "N/A"
                })

        browser.close()
    
    print("Scraped the articles!")

    return pd.DataFrame(article_content)

# tweet scraper
def login_and_scrape_tweets(search_queries):
    TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
    TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Open Twitter login page
        page.goto("https://twitter.com/login")
        time.sleep(1)

        # Enter username
        page.fill("input[name='text']", TWITTER_USERNAME)
        page.keyboard.press("Enter")
        time.sleep(1)  

        # Enter password
        page.fill("input[name='password']", TWITTER_PASSWORD)
        page.keyboard.press("Enter")
        print("Logging in to Twitter")
        time.sleep(5)  # Allow time to log in
        
        all_tweets = []
        # Search for tweets
        for search_query in search_queries:
            search_url = f"https://twitter.com/search?q={search_query['keyword'].replace(' ', '%20')}&f=live"
            page.goto(search_url)
            time.sleep(3)

            # Extract tweets
            tweets = []
            while len(tweets) < search_query['max_tweets']:
                tweet_elements = page.locator("article").all()
                for tweet in tweet_elements:
                    try:
                        content = tweet.locator("div[lang]").inner_text()
                        timestamp = tweet.locator("time").get_attribute("datetime")
                        tweets.append({"timestamp": timestamp, "content": content})
                        if len(tweets) >= search_query['max_tweets']:
                            break
                    except:
                        continue
                page.keyboard.press("PageDown")
                time.sleep(2)

            all_tweets.extend(tweets)

        browser.close()

    print("Scraped the tweets!")
    
    df = pd.DataFrame(all_tweets)
    return df
