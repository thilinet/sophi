from duckduckgo_search import DDGS
from typing import List
import requests
from bs4 import BeautifulSoup as bs
import time 

def web_search(web_query: str, num_results: int=2) -> List[str]:
    return [r["href"] for r in DDGS().text(web_query, max_results=num_results)]



def web_scrape(url: str) -> str:
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = bs(response.text,"html.parser")
            page_text = soup.get_text(separator=" ",strip=True)
            return page_text
        else:
            return f"Could not retrieve web page: status code: {response.status_code}"
    except Exception as e:
        print(e)
        return f"Could not retrieve web page {e}"
    

if __name__ == "__main__":
    urls = []
    contents = []
    search_queries = {'search_query': ['"NVIDIA Corporation"', '"NVIDIA Group"', '"Microarchitecture"', '"GPU Technology"', '"Artificial Intelligence"', '"Deep Learning"', '"Cloud Computing"', '"Datacenter Solutions"', '"Gaming Console"']}
    for query in search_queries['search_query']:
        query = query.replace("\"","")
        query = query.strip()
        print(query)
        urls.extend(web_search(query))
        print(urls)
        time.sleep(10)
    
    print(urls)
    """
    for url in urls:
        content = web_scrape(url)
        contents.append((url, content))

    for url, content in contents:
        print(url)
        print(contents)
        print("*" * 10 )
    """