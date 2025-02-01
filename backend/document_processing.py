from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# returns a python <class 'list'> of <class 'langchain_core.documents.base.Document'> objects
def get_document_chunks():
    loader = PyPDFLoader("../data/Petition-Decisions/California_1556 2023.11.21 HODecision_Redacted.pdf")  # Adjust path to your PDF
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0) # prev hyperparameters 3000, 400
    chunks = text_splitter.split_documents(documents)

    # num_total_characters = sum([len(x.page_content) for x in chunks])
    # print (f"Now you have {len(chunks)} documents that have an average of {num_total_characters / len(chunks):,.0f} characters (smaller pieces)")

    return chunks

# TO DO: similarity search to include ALL documents
# def demo_search(k : int = 1):
#     all_docs = Chroma.similarity_search(
#         query="locking a cat up",  # Empty query to try to get all docs
#         k=k  # Set this to a number larger than your total documents
#     )
#     return all_docs[0]
#demo_search()