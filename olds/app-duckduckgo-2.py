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

# Load environment variables from .env file
load_dotenv()

# Access the environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize LLM
llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.6)

# Define the prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a friendly AI assistant."),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]
)

# Setup embeddings
embeddings = OpenAIEmbeddings()

from utils.search_utils import search_duckduckgo_with_urls

if __name__ == "__main__":
    search_query = "Langchain development"
    search_results = search_duckduckgo_with_urls(search_query)
    
    for result in search_results:
        print(f"Title: {result['title']}")
        print(f"Link: {result['link']}")
        print(f"Snippet: {result['snippet']}\n")

