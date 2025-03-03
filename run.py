import argparse
import json
import os

from generateEmbeddings import save_embeddings
from generate_opinion import LLMOutput
from responseModel import Opinion
from getData import getData
from llmConfig import LLMConfig

# Creating a command-line argument framework
# Currently it would perform classification
# More featurees can be added eventually

argparser = argparse.ArgumentParser(description="LLM-based Classifier for work-life balance public content")
argsubparsers = argparser.add_subparsers(title = "Commands", dest = "command")
argsubparsers.required = True

classify_parser = argsubparsers.add_parser("classify", help="Classify tweets and articles")

classify_parser.add_argument("--tweet",
                             dest="tweet",
                             metavar="tweet",
                             nargs="+",
                             help="List of twitter keywords to search followed by max tweets per keyword (e.g., worklife 20 wlb 10)")

classify_parser.add_argument("--article",
                             dest="article",
                             metavar="article",
                             nargs="+",
                             help="List of articles to classify (e.g., URLs of articles)")

def runModel(url_list, search_queries):
    try:
        llmInstance = LLMOutput(LLMConfig.Prompt, LLMConfig.LLM_MODEL)
        print("LLM Instance created")
        status = getData(url_list, search_queries)
        if status != "Success":
            raise Exception({'message': status})
        
        if(os.getenv("TWEET_FLAG")):
            with open("cleaned_tweets.json", "r", encoding="utf-8") as f:
                tweets = json.load(f)
            print("Output for the tweets coming up...")
            for content in tweets:
                result = llmInstance.generate_opinion(content=content["content"],object_model=Opinion)
                print(content["content"], result, "\n")

        if(os.getenv("ARTICLE_FLAG")):
            with open("cleaned_articles.json", "r", encoding="utf-8") as f:
                articles = json.load(f)
            print("Output for the articles coming up...")
            for content in articles:
                result = llmInstance.generate_opinion(content=content["text"],object_model=Opinion)
                print(content["text"][:1000], result, "\n")
    except Exception as e:
        print(e)
        raise e
        
    

if __name__ == "__main__":
    args = argparser.parse_args()

    if args.command == "classify":
        url_list = []
        search_queries = []
        if args.article:
            os.environ["ARTICLE_FLAG"] = "True"
            if "tweet" in args.article:
                args.article = args.article[:args.article.index("tweet")]
            
            url_list.extend(args.article)
        if args.tweet: # Parses the information provided and fits it into the template of input being followed
            os.environ["TWEET_FLAG"] = "True"
            tweet_args = args.tweet

            if tweet_args and tweet_args[0] == "tweet":  # Skip the keyword "tweet"
                tweet_args = tweet_args[1:]
            
            if len(tweet_args) % 2 != 0:
                print("Warning: Last tweet keyword has no max_tweets value. Ignoring it.")

            i = 0
            while i < len(tweet_args) - 1:
                keyword = tweet_args[i]
                try:
                    max_tweets = int(tweet_args[i + 1])
                    search_queries.append({'keyword': keyword, 'max_tweets': max_tweets})
                    i += 2
                except ValueError:
                    print(f"Skipping invalid tweet entry: {tweet_args[i:i+2]}")
                    i += 1
        runModel(url_list, search_queries)
    else:
        print(Exception("Arguments are required!"))

    # Deleting the files created during processing
    if os.path.exists("articles.json"):
        os.remove("articles.json")
    if os.path.exists("tweets.json"): 
        os.remove("tweets.json")
    if os.path.exists("cleaned_articles.json"): 
        os.remove("cleaned_articles.json")
    if os.path.exists("cleaned_tweets.json"):
        os.remove("cleaned_tweets.json")

    