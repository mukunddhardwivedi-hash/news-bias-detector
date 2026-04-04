import feedparser
import requests
import os
from dotenv import load_dotenv

load_dotenv()

RSS_SOURCES = {
    "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
    "Reuters": "https://feeds.reuters.com/reuters/topNews",
    "Fox News": "https://moxie.foxnews.com/google-publisher/latest.xml",
    "NPR": "https://feeds.npr.org/1001/rss.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
}

BIAS_MAP = {
    "BBC News": "center",
    "Reuters": "center",
    "Fox News": "right",
    "NPR": "left",
    "Al Jazeera": "center",
}

def fetch_rss():
    articles = []
    for source, url in RSS_SOURCES.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            articles.append({
                "title": entry.get("title", ""),
                "source": source,
                "url": entry.get("link", ""),
                "published": entry.get("published", ""),
                "bias": BIAS_MAP[source],
            })
    return articles

def fetch_newsapi():
    key = os.getenv("NEWS_API_KEY")
    if not key:
        return []
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=20&apiKey={key}"
    res = requests.get(url).json()
    articles = []
    for item in res.get("articles", []):
        articles.append({
            "title": item.get("title", ""),
            "source": item.get("source", {}).get("name", "Unknown"),
            "url": item.get("url", ""),
            "published": item.get("publishedAt", ""),
            "bias": "center",
        })
    return articles

def fetch_all():
    return fetch_rss() + fetch_newsapi()