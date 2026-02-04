from src.orchestator.chain import complianceRAGChain
import json

# def run_compliance(structured_json):
#     """
#     Runs compliance RAG loop and returns results
#     """
#     rag = complianceRAGChain(structured_json)
#     rag.run_RAG_model(model_type="llama")  # auto-fallback handled internally
#     return rag.run_compliance_loop()


def run_compliance(structured_json):
    """
    Reads the markdown and JSON content from the local storage paths.
    """
    json_path = "D:/Assessment/ManulifeAssessment/Manulife_assessment/backend/results/complianceResults.json"

    # Read JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            structured_json = json.load(f)
    except FileNotFoundError:
        structured_json = {"error": f"File not found at {json_path}"}

    return structured_json
