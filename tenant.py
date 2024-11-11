import os
import json
import re
import requests
from typing import Dict, Any, List, Union, Tuple

import google.generativeai as genai
from dotenv import load_dotenv

from langchain import LLMChain, PromptTemplate
from langchain.agents import (
    Tool,
    AgentExecutor,
    LLMSingleActionAgent,
    load_tools,
    initialize_agent
)
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import RetrievalQA
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader
)
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import (
    BaseChatPromptTemplate,
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.schema import AgentAction, AgentFinish, HumanMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_community.utilities import (
    GoogleSearchAPIWrapper,
    TextRequestsWrapper
)
from LegalDocumentProcessor import LegalDocumentProcessor
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID', '44cccd4214e594369')
GOOGLE_SEARCH_KEY = os.getenv('GOOGLE_SEARCH_KEY', 'AIzaSyAOI--7LYnBplAtoCzYx-0lLnneHz0euso')
GEMINI_API = "AIzaSyDYIEW4XVSeuMaVlcmXgv2rqI20jqUolwk"

# First, process and load your historical hearing orders
processor = LegalDocumentProcessor()
vectorstore = processor.process_documents("/nas/ucb/davidyang/legal-rent/petition-decisions/")

def demo_search(k : int = 1):
    all_docs = vectorstore.similarity_search(
        query="locking a cat up",  # Empty query to try to get all docs
        k=k  # Set this to a number larger than your total documents
    )
    return all_docs[0]

def demo_query(query : str):
    loader = PyPDFLoader("/nas/ucb/davidyang/legal-rent/petition-decisions/California_1556 2023.11.21 HODecision_Redacted.pdf")
    loadfile = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=400)
    docs = text_splitter.split_documents(loadfile)
    docsearch = FAISS.from_documents(docs, embeddings)
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=docsearch.as_retriever(), input_key="question")
    return qa.run(query)

#demo_search()
demo_query("What was the final monthly rent amount?")