import streamlit as st
import pandas as pd

from modules.document_processing import process_documents
from modules.tax_calculation import calculate_tax, generate_itr_files
#from modules.rag_pipeline import get_ai_response
from modules.utils import load_sample_data

# Set Streamlit page config
st.set_page_config(page_title='TaxSaathi: Taxes Made Less Taxing', layout='wide')

# Center Alignment & Narrower Width
center_align = """
    <style>
    .stApp {text-align: center; max-width: 1000px; margin: auto;}
    .stButton>button {margin: auto;}
    </style>
"""
st.markdown(center_align, unsafe_allow_html=True)

# Landing Page
st.title('🧾 TaxSaathi: Taxes Made Less Taxing')
st.markdown('**Simplifying your tax filing process with AI-driven automation and smart insights!**')
st.write('Welcome to TaxSaathi, your trusted companion for hassle-free tax filing in India. Get started by uploading your documents and let our AI do the rest!')

if st.button('Get Started'):
    st.session_state['started'] = True

# Document Upload Section
if 'started' in st.session_state:
    st.header('📂 Document Upload')
    form_16 = st.file_uploader('Upload Form 16 (PDF only)', type=['pdf'])
    investment_proofs = st.file_uploader('Upload Investment Proofs (Optional, Multiple Allowed)', type=['pdf', 'jpeg', 'png'], accept_multiple_files=True)
    bank_statements = st.file_uploader('Upload Bank Statements (Optional, PDF only)', type=['pdf'])
    #ais_file = st.file_uploader('Upload AIS (Optional, TXT only)', type=['txt'])

    if st.button('Process Documents'):
        if form_16:
            st.success('Form 16 uploaded successfully!')
            document_data = process_documents(form_16, investment_proofs, bank_statements)
            st.session_state['document_data'] = document_data
        else:
            st.error('Form 16 is required to proceed.')

# Tax Regime Comparison & Recommendation
if 'document_data' in st.session_state:
    st.header('⚖️ Tax Regime Comparison & Recommendation')
    st.write('Choose a tax regime or let us recommend the best option for you:')

    regime_option = st.radio('Tax Regime Options', ('Old Regime', 'New Regime', 'Recommend Best Option'))
    document_data = st.session_state['document_data']

    if regime_option == 'Recommend Best Option':
        tax_details = calculate_tax(document_data)
        recommended_regime = tax_details['recommended_regime']
        st.success(f'We recommend the **{recommended_regime}** for maximum tax savings!')

# AI Query Handling (RAG Pipeline)
st.header('💬 Ask Your Tax Queries')
user_query = st.text_input('Have a tax-related question? Ask here!')

# if st.button('Get Answer') and user_query:
#     ai_response = get_ai_response(user_query, document_data)
#     st.markdown(f'**Answer:** {ai_response}')

# Download ITR Forms
st.header('📥 Download Your ITR Forms')
if st.button('Generate ITR Forms') and 'document_data' in st.session_state:
    old_itr, new_itr = generate_itr_files(document_data)
    st.success('Your ITR forms are ready for download!')

    st.download_button(label='Download ITR (Old Regime)', data=old_itr, file_name='ITR_Old_Regime.pdf')
    st.download_button(label='Download ITR (New Regime)', data=new_itr, file_name='ITR_New_Regime.pdf')

# Tax Summary & Insights
st.header('📊 Tax Summary & Insights')
tax_data = {'Old Regime': [50000], 'New Regime': [60000]}
st.bar_chart(pd.DataFrame(tax_data, index=['Tax Liability']))

# How-To Section
with st.expander('How to Use TaxSaathi?'):
    st.write('''
        1. **Upload your tax documents** - including Form 16, investment proofs, bank statements, and AIS.
        2. **Select your tax regime** or get an AI-driven recommendation.
        3. **Download ready-to-file ITR forms** under both old and new regimes.
        4. **Ask tax-related queries** using our AI assistant.
    ''')

st.markdown('---')
st.markdown('**Disclaimer:** TaxSaathi is a prototype and not a certified tax advisory tool.')
st.markdown('Prototype created by Dyuthi Ramesh for the Google Girl Hackathon')
