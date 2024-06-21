from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate

def summerize_content(db, query, k=4):
    # collecting docs based on similarity search
    docs = db.similarity_search(query, k=k)

    # join the content of the page_content attribute from eac document...
    docs_page_content = " ".join([d.page_content for d in docs])

    # creating the model
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=.7)

    # prompt engineering template
    template = """
        {docs}
            As a world class journalist, researcher, article, newsletter and blog writer, 
            you will summarize the text above in order to create a 
            newsletter around {query}.
            This newsletter will be sent as an email.  The format is going to be like
            Tim Ferriss' "5-Bullet Friday" newsletter.
            
            Please follow all of the following guidelines:
            1/ Make sure the content is engaging, informative with good data
            2/ Make sure the conent is not too long, it should be the size of a nice newsletter bullet point and summary
            3/ The content should address the {query} topic very well
            4/ The content needs to be good and informative
            5/ The content needs to be written in a way that is easy to read, digest and understand
            6/ The content needs to give the audience actinable advice & insights including resouces and links if necessary
            
            SUMMARY:
        """
    # Prepping the Prompt Template
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", template.format(docs="{docs}", query="{query}"))
        ]
    )

    # Combine the prompt and LLM into a sequence
    summerizer_chain: Runnable = prompt_template | llm | StrOutputParser()

    # Create input for the chain
    input_data = {"docs": docs, "query": query}

    # Invoke the chain
    result = summerizer_chain.invoke(input_data)

    # print(result)
    return result