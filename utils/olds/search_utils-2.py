import json
from langchain_community.tools import DuckDuckGoSearchResults

def search_duckduckgo_with_urls(query):
    """
    Perform a search using DuckDuckGo and return the results with URLs.

    Args:
    query (str): The search query string.

    Returns:
    list: A list of search results, each containing a title, URL, and snippet.
    """
    search = DuckDuckGoSearchResults()
    results = search.run(query)
    
    # Debug: Print the results to understand the structure
    print(results)
    
    # Check if results are a string and convert to list of dictionaries
    if isinstance(results, str):
        results = json.loads(results)
    
    formatted_results = [
        {
            "title": result["title"],
            "link": result["link"],
            "snippet": result["snippet"]
        }
        for result in results
    ]
    return formatted_results
