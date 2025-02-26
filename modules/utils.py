import requests

def load_sample_data():
    """
    Loads sample data for testing the application.
    :return: Sample financial data
    """
    return {
        'income': 800000,
        'deductions': 150000,
        'investments': 100000
    }

def generate_gemini_prompt(document_data):
    """
    Generates a structured prompt for the Gemini API based on document data.
    
    :param document_data: Financial data extracted from documents
    :return: Formatted prompt string
    """
    income = document_data.get('income', 0)
    deductions = document_data.get('deductions', 0)
    
    prompt = (
        f"Calculate tax liability for an income of {income} with deductions of {deductions}. "
        "Provide results for both old and new tax regimes in India."
    )
    return prompt

def call_gemini_api(prompt):
    """
    Calls the Gemini API with a formatted prompt.
    
    :param prompt: AI prompt for tax calculation
    :return: Response from the Gemini API as a dictionary
    """
    GEMINI_API_URL = 'https://api.gemini.com/calculate-tax'
    response = requests.post(GEMINI_API_URL, json={'prompt': prompt})

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error calling Gemini API: {response.status_code}")
        return None
