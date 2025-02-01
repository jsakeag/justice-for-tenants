# import os
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# from langchain_azure_openai import AzureOpenAIEmbeddings
# from langchain_chroma import Chroma
# from langchain.memory import ConversationBufferMemory
# from langchain.prompts import ChatPromptTemplate
# from langchain.chains import ConversationalRetrievalChain
# from langchain.retrievers import ContextualCompressionRetriever
# from langchain.retrievers.document_compressors import LLMChainExtractor

# # Get the API key from the environment variable
# openai_api_key =  ""


# if not openai_api_key:
#     raise ValueError("OPENAI_API_KEY environment variable is not set")

# # Initialize OpenAI Chat model
# llm = ChatOpenAI(
#     model_name="gpt-4o-mini",
#     temperature=0.7,
#     max_tokens=500,
#     api_key=openai_api_key  # Explicitly pass the API key here
# )

# # Initialize memory for conversation
# memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# # Create embedding model
# embeddings = AzureOpenAIEmbeddings(
#     azure_endpoint="https://justice-for-tenants.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15",
#     openai_api_key="6JzVbcdiTHcmd1zFwhAdBoD1DHiCc0tnhUdRr0gmQT6TvvNZygMVJQQJ99AKACYeBjFXJ3w3AAABACOG3FCm",
#     model="text-embedding-ada-002",  # Moved deployment_name to model parameter
#     api_version="2024-02-15-preview"
# )
# # Initialize Chroma DB (vector database)
# vector_db = Chroma(embedding_function=embeddings, collection_name="my_collection",persist_directory="./my_chroma_db")

# # Create a ContextualCompressionRetriever
# retriever = ContextualCompressionRetriever(
#     base_compressor=LLMChainExtractor.from_llm(llm),
#     base_retriever=vector_db.as_retriever()
# )

# # Create a template for combining the memory, database, and LLM
# prompt_template = ChatPromptTemplate.from_template("""
#     Context: {context}
#     Chat History: {chat_history}
#     Human: {question}
#     AI: Please provide a relevant answer based on the context and chat history.
# """)

# # Create the ConversationalRetrievalChain
# conversation_chain = ConversationalRetrievalChain.from_llm(
#     llm=llm,
#     retriever=retriever,
#     memory=memory,
#     combine_docs_chain_kwargs={"prompt": prompt_template}
# )

# def chatbot_response(user_input):
#     # Get the response based on user input
#     return conversation_chain({"question": user_input})["answer"]
