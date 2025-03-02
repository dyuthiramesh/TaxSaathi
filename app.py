import streamlit as st
import zipfile
import io

from modules.document_processing import process_documents
from modules.tax_calculation import calculate_tax
from modules.rag_pipeline import setup_rag_pipeline, get_ai_response
from modules.utils import generate_pdf

# 🚀 Set Streamlit page config
st.set_page_config(page_title="TaxSaathi: Taxes Made Less Taxing", layout="wide")

# 🎨 Custom CSS for better styling
st.markdown(
    """
    <style>
        .stApp { max-width: 900px; margin: auto; }
        .stButton>button { width: 100%; font-weight: bold; }
        .header { font-size: 22px; font-weight: bold; padding: 10px 0; }
        .container { background: #f9f9f9; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .success { color: green; font-weight: bold; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🏠 Landing Page
st.title("🧾 TaxSaathi: Taxes Made Less Taxing")
st.markdown("**Your AI-powered companion for hassle-free tax filing in India!**")
st.write("Upload your documents, let our AI do the calculations, and download ready-to-file ITR forms.")

# ℹ️ How-To Section
with st.expander("ℹ️ How to Use TaxSaathi?"):
    st.write(
        """
        1. **Upload your tax documents** (Form 16, investment proofs, bank statements).
        2. **Select your tax regime** or get an AI-driven recommendation.
        3. **Download your pre-filled ITR-2 forms** for both Old and New tax regimes.
        4. **Ask tax-related queries** to our AI assistant.
        """
    )

# 🚀 Start Processing
if st.button("🚀 Get Started"):
    st.session_state["started"] = True

# 📂 Document Upload Section
if "started" in st.session_state:
    st.markdown('<div class="header">📂 Upload Your Tax Documents</div>', unsafe_allow_html=True)

    with st.container():
        form_16 = st.file_uploader("📑 Upload Form 16 (PDF only)", type=["pdf"])
        investment_proofs = st.file_uploader(
            "📄 Upload Investment Proofs (Optional)", type=["pdf", "jpeg", "png"], accept_multiple_files=True
        )
        bank_statements = st.file_uploader("🏦 Upload Bank Statements (Optional, PDF only)", type=["pdf"])

    if st.button("🔄 Process Documents"):
        if form_16:
            with st.spinner("⏳ Processing your documents... Please wait."):
                document_data = process_documents(form_16, *investment_proofs, bank_statements)
                st.session_state["document_data"] = document_data
            st.success("✅ Documents processed successfully!")
        else:
            st.error("⚠️ Form 16 is required to proceed.")

# ⚖️ Tax Regime Comparison
if "document_data" in st.session_state:
    st.markdown('<div class="header">⚖️ Tax Regime Comparison & AI Recommendation</div>', unsafe_allow_html=True)

    if "tax_details" not in st.session_state:
        with st.spinner("⏳ Calculating your tax details..."):
            st.session_state["tax_details"] = calculate_tax(st.session_state["document_data"])

    tax_details = st.session_state["tax_details"]
    st.markdown(f'<span class="success">{tax_details["recommended_regime"]}</span>', unsafe_allow_html=True)

# 📥 Download ITR Forms
st.markdown('<div class="header">📥 Download Your ITR Forms</div>', unsafe_allow_html=True)

if st.button("📄 Generate ITR Forms"):
    if "tax_details" in st.session_state:
        with st.spinner("⏳ Generating your ITR forms..."):
            old_itr = generate_pdf(st.session_state["tax_details"]["old_regime"], "ITR_Old_Regime.pdf")
            new_itr = generate_pdf(st.session_state["tax_details"]["new_regime"], "ITR_New_Regime.pdf")
        st.success("✅ Your ITR forms are ready for download!")

        # 📁 Create ZIP for download
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            zipf.writestr("ITR_Old_Regime.pdf", old_itr)
            zipf.writestr("ITR_New_Regime.pdf", new_itr)
        zip_buffer.seek(0)

        st.download_button("📥 Download Both ITR Forms", zip_buffer, "ITR_Forms.zip", "application/zip")
    else:
        st.warning("⚠️ Please upload the necessary documents and process them first.")

# 💬 AI Tax Assistant
st.markdown('<div class="header">💬 Ask Your Tax Queries</div>', unsafe_allow_html=True)
user_query = st.text_input("💡 Have a tax-related question? Ask here!")

if st.button("🤖 Get Answer"):
    if user_query and "document_data" in st.session_state:
        with st.spinner("⏳ Fetching AI response..."):
            qa_chain = setup_rag_pipeline(st.session_state["document_data"])
            ai_response = get_ai_response(user_query, qa_chain)
        st.markdown(f"**📝 Answer:** {ai_response}")
    else:
        st.warning("⚠️ Please enter a question and ensure documents are processed.")

# 📝 Disclaimer
st.markdown("---")
st.markdown("**⚠️ Disclaimer:** TaxSaathi is a prototype and not a certified tax advisory tool.")
st.markdown("🚀 Prototype created by Dyuthi Ramesh for Google Girl Hackathon 2025")
