"""News briefing using RSS feeds — no API key needed."""
import requests
import xml.etree.ElementTree as ET

FEEDS = {
    "tech":    "https://feeds.feedburner.com/ndtvnews-tech",
    "india":   "https://feeds.feedburner.com/ndtvnews-top-stories",
    "world":   "https://rss.cnn.com/rss/edition_world.rss",
    "sports":  "https://feeds.feedburner.com/ndtvnews-sports",
}

def get_news(category="india", count=3):
    url = FEEDS.get(category, FEEDS["india"])
    try:
        res = requests.get(url, timeout=8)
        root = ET.fromstring(res.content)
        items = root.findall(".//item")[:count]
        headlines = [item.find("title").text for item in items if item.find("title") is not None]
        if not headlines:
            return "No news available right now."
        return f"Top {len(headlines)} headlines: " + ". ".join(headlines)
    except Exception as e:
        return f"Could not fetch news: {e}"

def morning_briefing():
    from datetime import datetime
    hour = datetime.now().hour
    news = get_news("india", 3)
    return f"Here's your briefing. {news}"
