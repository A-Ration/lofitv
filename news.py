import requests
from utils.api_keys import NYT_API_KEY

def get_headlines(section="home"):
    url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={NYT_API_KEY}"
    r = requests.get(url).json()
    headlines = []
    for article in r["results"][:7]:
        headlines.append({
            "title": article["title"],
            "abstract": article["abstract"]
        })
    return headlines
