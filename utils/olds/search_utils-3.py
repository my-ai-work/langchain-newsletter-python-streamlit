from langchain_community.tools import DuckDuckGoSearchResults

def search_duckduckgo_with_urls(query):
    """
    Perform a search using DuckDuckGo and return the results with URLs.

    Args:
    query (str): The search query string.

    Returns:
    list: A list of URLs from the search results.
    """
    search = DuckDuckGoSearchResults()
    results = search.run(query)
    
    # Debug: Print the results to understand the structure
    print(results)
    
    # Collect the URLs from the results
    urls = [result['link'] for result in results if 'link' in result]
    return urls
