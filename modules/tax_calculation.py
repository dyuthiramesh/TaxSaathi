import os
from modules.utils import generate_gemini_prompt, call_gemini_api

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def calculate_tax(document_data):
    """
    Calculate tax liabilities using the Gemini API and suggest the best regime.
    
    :param document_data: Financial data extracted from documents
    :return: Tax details and recommended regime as a dictionary
    """
    prompt = generate_gemini_prompt(document_data)
    tax_details = call_gemini_api(prompt)
    
    if not tax_details:
        return {'error': 'Failed to fetch tax details from Gemini API.'}

    return {
        'old_regime': tax_details.get('old_regime_tax', 0),
        'new_regime': tax_details.get('new_regime_tax', 0),
        'recommended_regime': (
            'Old Regime' if tax_details.get('old_regime_tax', float('inf')) < tax_details.get('new_regime_tax', float('inf'))
            else 'New Regime'
        )
    }

def generate_itr_files(document_data):
    """
    Generates ITR-2 forms for both tax regimes.
    
    :param document_data: Financial data extracted from documents
    :return: Byte data for old and new regime ITR forms
    """
    # Placeholder: Implement actual ITR generation logic
    old_itr = b"Old Regime ITR PDF content"
    new_itr = b"New Regime ITR PDF content"
    
    return old_itr, new_itr
