import warnings
import os
from dotenv import load_dotenv

from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Ignore warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.2,
    convert_system_message_to_human=True
)

# Ensure ChromaDB directory exists
CHROMA_DB_DIR = "./chroma_db"
os.makedirs(CHROMA_DB_DIR, exist_ok=True)

def setup_rag_pipeline(pages):
    """
    Sets up the RAG (Retrieval-Augmented Generation) pipeline with embeddings and a vector store.

    Args:
        pages (list): A list of document pages containing 'page_content'.

    Returns:
        RetrievalQA: Configured RAG pipeline for answering tax-related queries.
    """
    
    # Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
    context = "\n\n".join(str(p['page_content']) for p in pages)  # Extract page content correctly
    texts = text_splitter.split_text(context)
    print("✅ Text splitting completed.")

    # Initialize embeddings model
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    print("✅ Embeddings model initialized.")

    # Create or update Chroma vector store
    vector_index = Chroma.from_texts(
        texts, 
        embeddings, 
        persist_directory=CHROMA_DB_DIR
    ).as_retriever(search_kwargs={"k": 5})
    print("✅ Vector store created and loaded.")

    # Define prompt template for tax-related queries
    template = """
    You are an AI assistant specialized in answering questions strictly related to Indian taxation. 
    You can use the provided documents and general tax knowledge to assist users. 

    If the question is not related to Indian taxation, simply respond with: 
    "I specialize in Indian taxation-related queries. Please ask me tax-related questions."

    {context}
    Question: {question}
    Answer:
    """
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)
    print("✅ Prompt template initialized.")

    # Initialize the RAG QA chain
    qa_chain = RetrievalQA.from_chain_type(
        model,
        retriever=vector_index,
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    print("✅ RAG pipeline setup complete.")
    return qa_chain

def get_ai_response(question, qa_chain):
    """
    Gets an AI-generated response to a tax-related query.

    Args:
        question (str): The user's tax-related question.
        qa_chain (RetrievalQA): The configured RAG pipeline.

    Returns:
        str: AI-generated response.
    """
    response = qa_chain({"query": question})
    print("✅ AI response generated.")
    return response["result"]
 