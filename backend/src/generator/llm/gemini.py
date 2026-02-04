from langchain_google_genai import ChatGoogleGenerativeAI
from src.generator.llm.base_client import build_qa_chain
import os
from dotenv import load_dotenv
load_dotenv()


def build_gemini_rag_model(
    vector_store,
    prompt_template,
    output_parser,
    temperature=1.0,
):
    """
    Builds a RAG model using ChatGoogleGenerativeAI (Gemini).
    """
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            temperature=temperature,
            api_key=os.getenv("GOOGLE_API_KEY"),
        )

        return build_qa_chain(
            llm=llm,
            prompt_template=prompt_template,
            vector_store=vector_store,
            output_format=output_parser
        )

    except Exception as e:
        raise RuntimeError(
            f"Gemini RAG model initialization failed: {str(e)}") from e
