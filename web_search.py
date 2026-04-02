# web_search.py 
import requests
from bs4 import BeautifulSoup

def search_web(query: str, max_results=3):
    str
    url = "https://duckduckgo.com/html/"
    params = {"q": query}

    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.post(url, data=params, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for res in soup.select(".results__snippet") [max_results]:
        results.append(res.get_text())

    if not results:
        return "Ничего не найдено."
    
    return "\n".join(results)