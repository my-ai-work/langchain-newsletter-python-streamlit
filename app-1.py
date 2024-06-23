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

def main():
    st.set_page_config(page_title="Researcher...",
                       page_icon=":parrot:", layout="centered")
    
    st.header("Generate a Newsletter :parrot:")
    search_query = st.text_input("Enter a topic...")

    if search_query:
        print(search_query)
        with st.spinner(f"Generating newsletter for {search_query}"):
            st.write("Generating newsletter for: ", search_query)

             # search results
            search_results = search_duckduckgo_with_details(search_query)
            # display results
            print("Search Results:")
            # Display the log messages
            st.markdown("### Displaying Search Results...")
            st.write(search_results, language='python')

        # Add spinner for the next step
        with st.spinner("Collecting best articles..."):
            # collect best 3 urls as a list
            best_urls = pick_best_articles_urls(search_results, search_query)
            # display 3 urls
            print("Best 3 URLs:")
            st.markdown("### Best URLs:")
            st.write(best_urls, language='python')

            # Step 3: Extract content and create FAISS vector DB
            with st.spinner("Extracting content from URLs and creating FAISS vector DB..."):
                faiss_db = extract_url_content(best_urls)
                st.success("FAISS vector DB created!")

            # Step 4: Summarize vector DB content
            with st.spinner("Summarizing content from FAISS vector DB..."):
                summaries = summerize_content(faiss_db, search_query)
                print("The Summary of the online data:")
                st.markdown("### The Summary of the Online Data:")
                st.write(summaries, language='python')

            # generate newsletter
            # the_news_letter = generate_newsletter(summeries, search_query)


if __name__ == "__main__":
    # running main
    main()
