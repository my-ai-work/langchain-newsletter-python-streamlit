import os
import json
import openai
import requests
import logging
from dotenv import find_dotenv, load_dotenv
from langchain_openai import OpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import Runnable
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
# ---------------------------------------------------------------------------
# KEEP THESE IMPORTS FOR REFERENCE. SICK OF FREQUENT CHANGES
# ---------------------------------------------------------------------------
import streamlit as st

# Load environment variables from .env file
load_dotenv()
# Access the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Load development moduels
from utils.search_utils import search_duckduckgo_with_details
from utils.pick_best_urls_utils import pick_best_articles_urls
from utils.extract_url_content_utils import extract_url_content
from utils.summerize_content_utils import summerize_content
from utils.generate_newsletter_utils import generate_newsletter


if __name__ == "__main__":
    # search query
    search_query = "The Real Estate Market in Atlanta in the year 2024"
    # search results
    search_results = search_duckduckgo_with_details(search_query)
    # display results
    print("Search Results:")
    # print(search_results)
    for result in search_results:
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print(f"Snippet: {result['snippet']}\n")
    
    # collect best 3 urls as a list
    best_urls = pick_best_articles_urls(search_results, search_query)
    # display 3 urls
    print("Best URLs:")
    print(best_urls)

    # extract url content
    faiss_db = extract_url_content(best_urls)

    # summerize vector db content
    summeries = summerize_content(faiss_db, search_query)
    print("The Summary of the online data:")
    print(summeries)

    # generate newsletter
    generate_newsletter(summeries, search_query)




