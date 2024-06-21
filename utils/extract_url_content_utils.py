from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


def extract_url_content(urls):
    # Setup embeddings
    embeddings = OpenAIEmbeddings()

    # use unstructuredURLLoader
    loader = UnstructuredURLLoader(urls)
    data = loader.load()

    # splitting the text content
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    # load splits into a document
    docs = text_splitter.split_documents(data)

    # vectorize data with FAISS
    db = FAISS.from_documents(docs, embeddings)

    return db

