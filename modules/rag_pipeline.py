# rag_pipeline.py
import os
from langchain.vectorstores import Chroma
from langchain.embeddings import GeminiEmbeddings
from langchain.llms import Gemini
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from io import BytesIO
import streamlit as st

# Configuration (Ensure GEMINI_API_KEY is set in environment or Streamlit Secrets)
def setup_rag_pipeline():
    """Sets up the RAG pipeline using ChromaDB and Langchain."""
    try:
        gemini_api_key = os.environ["GEMINI_API_KEY"]
    except KeyError:
        st.error("GEMINI_API_KEY environment variable not set.")
        return None

    embeddings = GeminiEmbeddings(google_api_key=gemini_api_key)
    vector_store = Chroma(persist_directory="chroma_db", embedding_function=embeddings) # Added persist_directory
    llm = Gemini(google_api_key=gemini_api_key)
    qa_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=vector_store.as_retriever())
    return qa_chain

def ingest_documents(pdf_files):
    """Ingests PDF documents into ChromaDB."""
    try:
        gemini_api_key = os.environ["GEMINI_API_KEY"]
    except KeyError:
        st.error("GEMINI_API_KEY environment variable not set.")
        return None

    all_texts = []
    for pdf_file_bytes in pdf_files:
        try:
            with BytesIO(pdf_file_bytes) as file:
                loader = PyPDFLoader(file)
                pages = loader.load()
                text = "".join([page.page_content for page in pages])
                all_texts.append(text)
        except Exception as e:
            st.error(f"Error loading PDF: {e}")
            return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.create_documents(all_texts)

    embeddings = GeminiEmbeddings(google_api_key=gemini_api_key)
    Chroma.from_documents(texts, embeddings, persist_directory="chroma_db") # Added persist_directory

def get_ai_response(query: str) -> str:
    """Answers user queries using the RAG pipeline."""
    qa_chain = setup_rag_pipeline()
    if qa_chain is None:
        return "RAG pipeline could not be initialized. Please check the API key and uploaded documents."
    response = qa_chain.run(query)
    return response