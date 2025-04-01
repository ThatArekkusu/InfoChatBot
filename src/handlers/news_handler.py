from dotenv import load_dotenv
import random
import requests
import os

def getNews(userInput):
    API_KEY = os.getenv('NEWS_API_KEY')
    articleIndex = random.randint(0, 9)
    
    responseAPI = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={API_KEY}")
    
    if responseAPI.status_code == 200:
        data = responseAPI.json()
        headline = data['articles'][articleIndex]['title']
        description = data['articles'][articleIndex]['description']
        
        news = f"{headline}.\n, {description}"
        
        return f"The latest news is: {news}"
    else:
        return f"Failed to fetch news data. Error: {responseAPI.status_code}"