from src.orchestator.chain import complianceRAGChain, qna
import json


def run_compliance(structured_json, chat_type=False):
    """
    Runs compliance RAG loop and returns results
    """
    rag = complianceRAGChain(structured_json)
    # auto-fallback handled internally
    rag.run_RAG_model(model_type="llama", chat_type=chat_type)
    return rag.run_compliance_loop()


def run_qna(structured_json, chat_type=True):
    """
    Runs Q&A RAG model and returns answer
    """
    rag = complianceRAGChain(structured_json)
    # auto-fallback handled internally
    qa_chain = rag.run_RAG_model(model_type="llama", chat_type=chat_type)
    return qa_chain


def ask_bot(qa_chain, question):
    """
    Asks question to RAG model and returns answer
    """
    return qna(qa_chain, question)


# def run_compliance(structured_json, chat_type=False):
#     """
#     Reads the markdown and JSON content from the local storage paths.
#     """
#     json_path = "D:/Assessment/ManulifeAssessment/Manulife_assessment/backend/results/complianceResults.json"

#     # Read JSON file
#     try:
#         with open(json_path, 'r', encoding='utf-8') as f:
#             structured_json = json.load(f)
#     except FileNotFoundError:
#         structured_json = {"error": f"File not found at {json_path}"}

#     return structured_json
