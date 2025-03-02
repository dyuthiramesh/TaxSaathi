import os
import re
from io import BytesIO
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# Load environment variables from .env file
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Google API Key not found. Please set it in the .env file.")

def get_gemini_model():
    """
    Initializes and returns the Gemini AI model for tax-related queries.

    Returns:
        ChatGoogleGenerativeAI: Configured Gemini model.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
        convert_system_message_to_human=True
    )

def get_vector_index(pages):
    """
    Creates a vector index using Chroma for tax-related document retrieval.

    Args:
        pages (list): List of document pages with 'page_content'.

    Returns:
        Retriever: Chroma retriever for similarity search.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    context = "\n\n".join(str(p["page_content"]) for p in pages)  # Extract page text
    texts = text_splitter.split_text(context)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    return Chroma.from_texts(texts, embeddings).as_retriever(search_kwargs={"k": 5})

def clean_markdown(text):
    """
    Cleans markdown formatting (bold, italic, code blocks, headings) and replaces ₹ with INR.

    Args:
        text (str): Input text with markdown formatting.

    Returns:
        str: Cleaned text with markdown removed and ₹ replaced with INR.
    """
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Remove **bold**
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # Remove *italic*
    text = re.sub(r'`(.*?)`', r'\1', text)        # Remove `code`
    text = re.sub(r'#{1,6}\s?', '', text)         # Remove # headings
    text = re.sub(r'[\[\]]', '', text)            # Remove square brackets (common in links)
    text = text.replace("₹", "INR")               # Replace rupee symbol with INR
    return text.strip()

def generate_pdf(content, file_name):
    """
    Generates a formatted PDF with wrapped text.

    Args:
        content (str): Text content to be written in the PDF.
        file_name (str): Name of the output PDF file.

    Returns:
        bytes: Binary PDF data for downloading.
    """
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.setFont("Times-Roman", 12)

    max_width = 500  # Maximum width for text wrapping
    y_position = 750  # Start position for text

    for line in content.split("\n"):
        cleaned_line = clean_markdown(line)  # Remove markdown and replace ₹
        wrapped_lines = simpleSplit(cleaned_line, "Times-Roman", 12, max_width)

        for sub_line in wrapped_lines:
            c.drawString(50, y_position, sub_line)  # Draw text at position
            y_position -= 20  # Move down for next line

            if y_position < 50:  # If bottom is reached, create a new page
                c.showPage()
                c.setFont("Times-Roman", 12)
                y_position = 750

    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()  # Return binary PDF data
