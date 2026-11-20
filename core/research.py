"""
Layer 1: Real-Time Research Engine
Combines Tavily Search (fresh 24-48h news) and Firecrawl Deep Web Scraper.
"""
import json
import urllib.request
import urllib.error
from typing import Dict, Any, List
from core.config import TAVILY_API_KEY, FIRECRAWL_API_KEY

def search_tavily(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Query Tavily Search API with advanced depth."""
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is not configured in .env")

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "topic": "news",
        "days": 2,
        "max_results": max_results
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        
    return data.get("results", [])

def scrape_firecrawl(target_url: str) -> str:
    """Deep scrape target URL using Firecrawl API and return clean markdown."""
    if not FIRECRAWL_API_KEY or not target_url:
        return ""

    url = "https://api.firecrawl.dev/v1/scrape"
    payload = {"url": target_url}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("success"):
                markdown = data.get("data", {}).get("markdown", "")
                return markdown[:4000]
    except Exception as e:
        print(f"  [Firecrawl Notice] Fallback to search snippets ({e})")
        
    return ""

def execute_research(query: str = "artificial intelligence engineering breakthroughs developer tools 2026") -> Dict[str, Any]:
    """
    Executes the dual-layer research pipeline:
    1. Tavily AI Search for top recent trends.
    2. Firecrawl Deep Web Scrape on the top source URL.
    """
    print(f"🔍 Step 1: Tavily AI Search -> '{query}'")
    search_results = search_tavily(query, max_results=5)
    
    if not search_results:
        raise RuntimeError(f"No search results returned for query: {query}")
        
    top_story = search_results[0]
    top_url = top_story.get("url", "")
    
    print(f"📖 Step 2: Firecrawl Deep Scraping source -> {top_url}")
    scraped_content = scrape_firecrawl(top_url)
    
    # Synthesize findings
    tavily_summary = "\n\n".join([
        f"Source [{i+1}] {r.get('title')}: {r.get('content')}"
        for i, r in enumerate(search_results[:3])
    ])
    
    final_context = scraped_content if scraped_content else tavily_summary
    
    return {
        "query": query,
        "title": top_story.get("title", ""),
        "url": top_url,
        "published_date": top_story.get("published_date", ""),
        "summary": tavily_summary,
        "deep_content": final_context,
        "raw_results": search_results
    }

if __name__ == "__main__":
    test_res = execute_research("autonomous agent architecture 2026")
    print(f"\nDiscovered: {test_res['title']}")
    print(f"Source URL: {test_res['url']}")
    print(f"Deep Content Length: {len(test_res['deep_content'])} characters")
