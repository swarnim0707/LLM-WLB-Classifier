import pytest
import json
import os
import sys
from unittest.mock import patch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from generate_opinion import LLMOutput
from responseModel import Opinion
from getData import save_tweets_to_json, clean_tweets

# Test LLM Output
@pytest.fixture
def mock_llm():
    return LLMOutput("Test template", "test-model")

@patch("generate_opinion.ChatOllama.invoke")
def test_generate_opinion(mock_invoke, mock_llm):
    mock_invoke.return_value.content = '{"for_or_against": "for", "employee_or_employer": "employee", "promotional_or_opinion": "opinion"}'
    
    result_dict = mock_llm.generate_opinion("Work-life balance is important", Opinion)
    
    # Convert result to Opinion model if needed
    if isinstance(result_dict, dict):
        result = Opinion(**result_dict)
    else:
        result = result_dict
    
    assert result.for_or_against == "for"
    assert result.employee_or_employer == "employee"
    assert result.promotional_or_opinion == "opinion"

@patch("generate_opinion.ChatOllama.invoke")
def test_generate_opinion_error(mock_invoke, mock_llm):
    mock_invoke.return_value.content = "Invalid JSON Response"
    result = mock_llm.generate_opinion("Invalid input", Opinion)
    assert isinstance(result, str) 
    assert "Error" in result 

# Test Data Saving
@pytest.fixture
def sample_tweets():
    return [{"content": "This is a test tweet", "timestamp": "2025-03-03T12:00:00"}]

def test_save_tweets_to_json(sample_tweets):
    save_tweets_to_json(sample_tweets, "test_tweets.json")
    with open("test_tweets.json", "r") as f:
        data = json.load(f)
    os.remove("test_tweets.json")
    assert data == sample_tweets

# Test Tweet Cleaning
def test_clean_tweets():
    test_data = [{"content": "Check this out http://example.com !!", "timestamp": "2025-03-03T12:00:00"}]
    save_tweets_to_json(test_data, "tweets.json")
    clean_tweets()
    with open("cleaned_tweets.json", "r") as f:
        cleaned_data = json.load(f)
    os.remove("tweets.json")
    os.remove("cleaned_tweets.json")
    assert "http" not in cleaned_data[0]["content"]
    assert "!" not in cleaned_data[0]["content"]