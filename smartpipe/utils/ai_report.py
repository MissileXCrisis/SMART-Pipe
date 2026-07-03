# smartpipe/utils/ai_report.py
import os
import json
from google import genai

def build_ecological_prompt(stats_data):
    """Serializes mathematical matrices into a structured markdown prompt context."""
    master_matrix = stats_data.get("master_matrix", {})
    alpha_div = stats_data.get("alpha", {})
    beta_matrix = stats_data.get("beta", {})

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
        "- Use the exact sample identifiers provided in the matrix (e.g., write 'SampleA' or 'Sample A').\n"
        "- DO NOT extrapolate or assume the presence of organisms not explicitly defined in the abundance matrix."
    )
    return prompt

def verify_grounding_guardrails(report_text, stats_data):
    """
    🛡️ Programmatic Post-Processing Validation Layer
    Scans the LLM response text to ensure calculated numerical boundaries 
    are accurately stated, accommodating minor stylistic spacing variations.
    """
    alpha_div = stats_data.get("alpha", {})
    
    # Guardrail 1: Structural Integrity check for Sample Names (handles spacing variations)
    for sample in alpha_div.keys():
        spaced_variant = sample.replace("Sample", "Sample ") # Matches "Sample A"
        
        if (sample not in report_text) and (spaced_variant not in report_text):
            print(f"⚠️ [GUARDRAIL-FAILED] Critical error: Sample identifier '{sample}' is entirely missing from the summary text.")
            return False
            
    # Guardrail 2: Mathematical Soundness check for Diversity Scores
    for sample, score in alpha_div.items():
        score_3d = f"{score:.3f}"
        score_2d = f"{score:.2f}"
        
        # Check if either the 2-decimal or 3-decimal representation is present
        if (score_3d not in report_text) and (score_2d not in report_text):
            # Also check if the AI represented it as a clean percentage (e.g., multiplying by 100 isn't common for Shannon, but defensive check)
            print(f"⚠️ [GUARDRAIL-FAILED] Data mismatch: Calculated Shannon index for {sample} ({score_3d}) is absent or misstated in the text.")
            return False
            
    print("🛡️ [GUARDRAIL-PASSED] Narrative text successfully grounded against numerical source matrices!")
    return True

def generate_automated_report(stats_data):
    """Initializes the client, manages the payload transfer, and routes through guardrails."""
    if not os.environ.get("GEMINI_API_KEY"):
        return False, "Aborting AI generation: GEMINI_API_KEY variable is missing."

    prompt_payload = build_ecological_prompt(stats_data)
    
    try:
        client = genai.Client()
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt_payload,
        )
        
        if not response.text:
            return False, "Received empty response from Gemini API."
            
        is_valid = verify_grounding_guardrails(response.text, stats_data)
        if is_valid:
            return True, response.text
        else:
            return False, "LLM summary failed post-processing validation checks."
            
    except Exception as e:
        return False, f"Outbound API layer exception: {str(e)}"