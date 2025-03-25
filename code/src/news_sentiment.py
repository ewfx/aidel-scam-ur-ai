import requests
import json
from gemini_sentiment import analyze_financial_risk
def get_news_articles(query):
    news_api_key=None
    with open('creds.json', 'r') as file:
        data = json.load(file)
        news_api_key = data['NEWS_API_KEY']
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": news_api_key,
        "sortBy":"relevancy" ,
        "language":"en"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print(type(response.json()['articles'])) # Print the JSON response
        return response.json()['articles']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except json.JSONDecodeError:
        print("Response is not valid JSON")
        return None

def get_sentiment_score(query):
    articles=get_news_articles(query)
    if(articles):
        success_count=0
        score=0.0
        reasoning=""
        for article in articles:
            if(success_count==10):
                break
            result=analyze_financial_risk(article['content'])
            if(result["score"]>-0.1):
                success_count+=1
                score+=result["score"]
                reasoning+=result["explanation"]
        if(success_count==0):
            return -1
        return [score/success_count,reasoning]


get_news_articles("Google")
