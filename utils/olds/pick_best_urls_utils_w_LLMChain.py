import json
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


def pick_best_articles_urls(response_dict, query):
    """
    Use LLM to choose the best articles from search results and return their URLs.

    Args:
    response_dict (dict): The dictionary containing search results.
    query (str): The search query string.

    Returns:
    list: A list of URLs of the best articles.
    """
    # Convert dictionary to JSON string
    response_str = json.dumps(response_dict)
    
    # Create LLM to choose best articles
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.6
    )

    # the prompt engineering template
    template = """ 
      You are a world class journalist, researcher, tech, Software Engineer, Developer, and an online course creator.
      You are amazing at finding the most interesting, relevant, and useful articles on certain topics.
      
      QUERY RESPONSE: {response_str}
      
      Above is the list of search results for the query "{query}".
      
      Please choose the best 3 articles from the list and return ONLY an array of the URLs.  
      Do not include anything else -
      return ONLY an array of the URLs. 
      Also make sure the articles are recent and not too old.
      If the file, or URL is invalid, show www.google.com.
    """
    prompt_template = PromptTemplate(
        input_variables=["response_str", "query"],
        template=template
    )
    article_chooser_chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=True
    )
    urls = article_chooser_chain.run(response_str=response_str, query=query)
    
    # Convert string to list
    url_list = json.loads(urls)
    return url_list
