from PyPDF2 import PdfReader

def process_documents(form_16, investment_proofs=None, bank_statements=None):
    """
    Extract relevant financial data from uploaded documents.
    
    :param form_16: Uploaded Form 16 PDF file
    :param investment_proofs: Optional list of investment proof files
    :param bank_statements: Optional uploaded bank statement PDF file
    :return: Extracted financial data as a dictionary
    """
    document_data = {}

    # Process Form 16
    document_data['form_16'] = extract_text_from_pdf(form_16)
    
    # Process Investment Proofs
    if investment_proofs:
        document_data['investment_proofs'] = [
            extract_text_from_pdf(file) for file in investment_proofs
        ]

    # Process Bank Statements
    if bank_statements:
        document_data['bank_statements'] = extract_text_from_pdf(bank_statements)

    return document_data


def extract_text_from_pdf(file):
    """
    Extracts text from a PDF file using PyPDF2.
    
    :param file: PDF file
    :return: Extracted text as a string
    """
    text_content = ""

    try:
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text_content += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")

    return text_content
