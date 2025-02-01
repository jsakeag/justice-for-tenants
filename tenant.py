from langchain.chains import RetrievalQA
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from LegalDocumentProcessor import LegalDocumentProcessor

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