import warnings
from PyPDF2 import PdfReader

warnings.filterwarnings("ignore")

def process_documents(*pdf_files):
    """Extracts and splits text from multiple PDF files using PyPDF2."""
    all_pages = []

    for pdf_file in pdf_files:
        if not pdf_file:
            continue  # Skip if the file is None (e.g., optional file not uploaded)
        
        try:
            # Load PDF using PyPDF2
            reader = PdfReader(pdf_file)
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                
                if text:
                    all_pages.append({"page_number": page_num + 1, "page_content": text})
            
            print(f"Loaded {len(reader.pages)} pages from {pdf_file.name}")
        
        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")
    
    print(f"Total pages loaded: {len(all_pages)}")
    return all_pages
