from langchain_groq import ChatGroq
from src.generator.llm.base_client import build_qa_chain
import os
from dotenv import load_dotenv
load_dotenv()


def build_llama_rag_model(
    vector_store,
    prompt_template,
    output_parser,
    model_name="llama-3.1-8b-instant",
    temperature=1.0,
    max_retries=2,
):
    """
    Builds a RAG model using ChatGroq (LLaMA).
    """
    try:
        llm = ChatGroq(
            model=model_name,
            temperature=temperature,
            max_retries=max_retries,
            api_key=os.getenv("GROQ_API_KEY"),
        )

        return build_qa_chain(
            llm=llm,
            prompt_template=prompt_template,
            vector_store=vector_store,
            output_parser=output_parser
        )

    except Exception as e:
        raise RuntimeError(
            f"LLaMA RAG model initialization failed: {str(e)}") from e
