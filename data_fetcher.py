import os
import requests
from typing import List, Dict

# App runs without APIs
DEMO_ARTICLES = [
    {
        "title": "Analysts weigh in on premium pricing and early adopters",
        "content": "Early reviews highlight strong build quality and immersive experience. Critics point to high pricing and limited enterprise tooling."
    },
    {
        "title": "Competitors announce new mid-range devices",
        "content": "Meta and HTC aim at broader consumer segments with lower price points and expanded content libraries."
    },
    {
        "title": "Developers explore productivity use-cases",
        "content": "Teams evaluate design workflows, remote collaboration, and AR note-taking, citing opportunities in enterprise adoption."
    }
]

# API request; It standardizes data for downstream processing
def fetch_newsapi(company: str) -> List[Dict]:
    key = os.getenv("NEWS_API_KEY")

    if not key: # DEMO mode
        return DEMO_ARTICLES 

    url = "https://newsapi.org/v2/everything"
    params = {"q": company, # Search for articles about the company
              "language": "en", # Limit to English
              "pageSize": 10, # Fetch top 10 relevant articles
              "apiKey": key, 
              "sortBy": "relevancy" # Sort by relevance (not date or popularity)
             }

    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status() # raises error for HTTP failures (403, 429, etc.)
        payload = r.json()
        out = []

        for a in (payload.get("articles") or [])[:10]: # NewsAPI responses are messy and inconsistent, normalize them into: title and content
            out.append({
                "title": a.get("title") or "",
                "content": (a.get("content") or "") + " " + (a.get("description") or "")
            })
        
        return out or DEMO_ARTICLES
    
    except Exception:
        return DEMO_ARTICLES

def fetch_reddit(company: str) -> List[Dict]:
    # Placeholder (Reddit-style data): real OAuth in M1
    return [{
        "title": f"Reddit discussion on {company}",
        "content": f"Users discuss {company} strengths, pricing concerns, and app ecosystem readiness."
    }]
