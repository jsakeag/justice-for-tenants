from flask import Flask, request, jsonify, make_response
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings # We'll use OpenAI's embedding engine
from langchain_openai import ChatOpenAI # We'll use OpenAI as our LLM
from document_processing import get_document_chunks
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize Flask app
app = Flask(__name__)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=openai_api_key,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Get chunks, initialize embeddings, create vector database, and build retriever
chunks = get_document_chunks()
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",  # OpenAI's text embedding model
    openai_api_key=openai_api_key
)
db = Chroma.from_documents(chunks, embeddings)
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever()) #input_key="question"

@app.route('/query', methods=['OPTIONS', 'POST'])
def query():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response, 204
    
    data = request.json
    user_query = data.get("query")
    if not user_query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    # Create response with CORS headers
    response_json = make_response(jsonify({"response": response}))
    response_json.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return response_json
    #response = qa.invoke(user_query)
    #return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)