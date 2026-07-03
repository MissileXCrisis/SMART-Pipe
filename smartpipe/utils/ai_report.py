# smartpipe/utils/ai_report.py
import os
import json
from google import genai

def build_ecological_prompt(stats_data):
    """
    Programmatically serializes mathematical matrices into a structured, 
    highly contextual prompt for the LLM.
    ```
    """
    # Extract calculated metrics from our biostats dictionary payload
    master_matrix = stats_data.get("master_matrix", {})
    alpha_div = stats_data.get("alpha", {})
    beta_matrix = stats_data.get("beta", {})

    # Construct the base prompt with rigorous systemic expectations
    prompt = (
        "You are an expert molecular bioinformatician and microbial ecologist analyzing a "
        "shotgun metagenomics pipeline run. Your job is to translate complex technical statistical arrays "
        "into a clean, clear, natural language executive summary for a clinical report.\n\n"
        "--- START RAW DATA MATRICES ---\n\n"
        "1. TAXONOMIC ABUNDANCE MATRIX (Proportions per sample):\n"
        f"{json.dumps(master_matrix, indent=2)}\n\n"
        "2. ALPHA DIVERSITY (Shannon-Wiener Index H'):\n"
        f"{json.dumps(alpha_div, indent=2)}\n\n"
        "3. BETA DIVERSITY MATRIX (Bray-Curtis Dissimilarity Distance):\n"
        f"{json.dumps(beta_matrix, indent=2)}\n\n"
        "--- END RAW DATA MATRICES ---\n\n"
        "CRITICAL INSTRUCTIONS:\n"
        "- Synthesize the data into exactly two cohesive, descriptive paragraphs.\n"
        "- Paragraph 1 must detail internal community properties (Alpha Diversity), specifically contrast which sample is the most even/diverse and highlight the dominating taxa.\n"
        "- Paragraph 2 must synthesize community distance trends (Beta Diversity), explaining how similar or distinct the samples are from one another.\n"
        "- Maintain a neutral, professional, data-grounded scientific tone.\n"
        "- DO NOT extrapolate or assume the presence of organisms not explicitly defined in the abundance matrix."
    )
    return prompt

def generate_automated_report(stats_data):
    """
    Initializes the Google GenAI client, crafts the context prompt, and 
    handles the outbound integration layer call.
    """
    # 1. Structural Security Check
    if not os.environ.get("GEMINI_API_KEY"):
        return False, "Aborting AI generation: GEMINI_API_KEY variable is missing from host environment."

    print("[AI-SYNTHESIS] Structuring engineering prompt payload...")
    prompt_payload = build_ecological_prompt(stats_data)
    
    print("[AI-SYNTHESIS] Initializing Google GenAI Client connection...")
    try:
        # Client natively auto-discovers os.environ["GEMINI_API_KEY"] as set up in Phase 1
        client = genai.Client()
        
        print("[AI-SYNTHESIS] Transmitting payload to gemini-3.5-flash...")
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt_payload,
        )
        
        if response.text:
            return True, response.text
        else:
            return False, "Received empty text payload response from Gemini API."
            
    except Exception as e:
        return False, f"Outbound API integration layer failed: {str(e)}"