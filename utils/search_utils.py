from langchain_community.tools import DuckDuckGoSearchResults
import re

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

    # Split the results string into individual result components
    result_items = re.findall(r'\[snippet:.*?\]', results)

    # Collect the details from the result components
    details = []
    for item in result_items:
        title_match = re.search(r'title: (.*?), link:', item)
        link_match = re.search(r'link: (.*?)]', item)
        snippet_match = re.search(r'snippet: (.*?), title:', item)

        if title_match and link_match and snippet_match:
            details.append({
                "title": title_match.group(1).strip(),
                "link": link_match.group(1).strip(),
                "snippet": snippet_match.group(1).strip()
            })

    return details
