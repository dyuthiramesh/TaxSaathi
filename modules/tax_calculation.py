from modules.utils import get_gemini_model

def format_pages_as_text(pages):
    """
    Extracts and formats text from document pages.

    Args:
        pages (list): A list of document pages containing 'page_content'.

    Returns:
        str: Formatted text combining all pages.
    """
    return "\n\n".join(p['page_content'] for p in pages)  # Extract page content correctly

def calculate_tax(pages):
    """
    Computes tax details for both the Old and New tax regimes using AI.

    Args:
        pages (list): A list of document pages with financial details.

    Returns:
        dict: Contains tax details for both regimes and the recommended option.
    """
    model = get_gemini_model()
    context_text = format_pages_as_text(pages)  # Convert document pages into plain text

    # AI prompts for tax computation
    old_regime_prompt = (
        f"Based on the following financial details (all amounts in INR), generate an ITR-2 form under the Indian old tax regime:\n\n{context_text}"
    )
    new_regime_prompt = (
        f"Based on the following financial details (all amounts in INR), generate an ITR-2 form under the Indian new tax regime:\n\n{context_text}"
    )
    recommendation_prompt = (
        f"Based on the following financial details, provide a short conclusion on which tax regime is more beneficial.\n"
        f"Only output in the following format:\n\n"
        f"**Comparison:**\n"
        f"* **Old Regime Tax:** INR X\n"
        f"* **New Regime Tax:** INR Y\n\n"
        f"**Conclusion:**\n"
        f"The **[better regime]** is more beneficial for you, resulting in a tax saving of INR Z.\n\n"
        f"{context_text}"
    )

    # Generate AI responses for both regimes and recommendation
    old_regime_response = model.invoke([{"role": "user", "content": old_regime_prompt}])
    new_regime_response = model.invoke([{"role": "user", "content": new_regime_prompt}])
    recommendation_response = model.invoke([{"role": "user", "content": recommendation_prompt}])

    return {
        "old_regime": old_regime_response.content,
        "new_regime": new_regime_response.content,
        "recommended_regime": recommendation_response.content,
    }
