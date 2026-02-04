import json
import os
from src.retriever.vector_store import vectorStoreRetriever
from src.generator.llm.gemini import build_gemini_rag_model
from src.generator.llm.llama import build_llama_rag_model
from src.orchestator.helper import baseOrchestrator
from src.generator.prompts.stepback_prompting import COMPLIANCE_PROMPT_TEMPLATE
from src.generator.prompts.compliance_prompt import QNA_PROMPT_TEMPLATE
from dotenv import load_dotenv
load_dotenv()


class complianceRAGChain(baseOrchestrator):
    def __init__(self, structured_data):
        self.structured_data = structured_data
        self.retriever = vectorStoreRetriever(self.structured_data)
        self.compliance_question = self.load_compliance_questions(
            file_path=os.getenv("COMPLIANCE_QUESTIONS_PATH")
        )
        self.qa_chain = None
        self.prompt_template = COMPLIANCE_PROMPT_TEMPLATE

    def run_RAG_model(self, model_type="llama", chat_type=False):
        vector_store = self.retriever.vector_store
        if chat_type:
            self.prompt_template = QNA_PROMPT_TEMPLATE

        if model_type == "llama":
            try:
                print("----Llama Model Invoked----")
                self.qa_chain = build_llama_rag_model(
                    vector_store=vector_store,
                    prompt_template=self.prompt_template,
                    output_parser=self.output_parser()
                )
                return self.qa_chain
            except Exception as llama_error:
                print(
                    f"[WARN] LLaMA failed, falling back to Gemini: {llama_error}")
                self.qa_chain = build_gemini_rag_model(
                    vector_store=vector_store,
                    prompt_template=self.prompt_template,
                    output_parser=self.output_parser()
                )
                return self.qa_chain

        elif model_type == "gemini":
            self.qa_chain = build_gemini_rag_model(
                vector_store=vector_store,
                prompt_template=self.prompt_template,
                output_parser=self.output_parser()
            )
            return self.qa_chain
        else:
            raise ValueError(f"Unsupported model_type: {model_type}")

    def query_rag_model(self, question):
        """
        Query RetrievalQA and parse structured output
        """
        result = self.qa_chain.invoke({"query": question})
        print("----Raw RAG Model Result----", result)
        parsed_output = self.output_parser().parse(result["result"])
        print("----RAG Model Query Result----")
        print(parsed_output)

        return {
            **parsed_output,
            "source_documents": result["source_documents"]
        }

    def run_compliance_loop(self):
        output = []
        print("----Running Compliance Loop----")
        questions = self.compliance_question["contract_audit_config"]["questions"]
        print(f"Loaded {len(questions)} compliance questions.")
        for q in questions:
            combined_question = f"{q['pre_condition']} {q['question']}"
            print("combined_question:", combined_question)

            result = self.query_rag_model(combined_question)
            print("result from query_rag_model:", result)
            output.append({
                "Compliance Question": q["title"],
                "Compliance State": result["compliance_state"],
                "Confidence": result["confidence"],
                "Relevant Quotes": result["relevant_quotes"],
                "Rationale": result["rationale"]
            })

            print("appended result for question:", output)

        self.save_output_json(output, file_path="complianceResults.json")
        return output



def qna(qa_chain, question):
    """
    Query RetrievalQA and parse structured output
    """
    result = qa_chain.invoke({"query": question})
    print("answers := ", result["result"])
    print("source_docs := ", result["source_documents"])
    return result["result"]
