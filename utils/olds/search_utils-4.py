from langchain_community.tools import DuckDuckGoSearchResults

def search_duckduckgo_with_details(query):
    """
    Perform a search using DuckDuckGo and return the details with URLs.

    Args:
    query (str): The search query string.

    Returns:
    list: A list of search results, each containing a title, URL, and snippet.
    """
    search = DuckDuckGoSearchResults()
    results = search.run(query)
    
    # Debug: Print the results to understand the structure
    print(results)
    
    # Collect the details from the results
    details = [
        {
            "title": result.get("title", ""),
            "link": result.get("link", ""),
            "snippet": result.get("snippet", "")
        }
        for result in results if 'link' in result
    ]
    return details
