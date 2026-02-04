import json
from src.retriever.vector_store import vectorStoreRetriever
from src.generator.llm.gemini import build_gemini_rag_model
from src.generator.llm.llama import build_llama_rag_model
from src.orchestator.helper import baseOrchestrator


class complianceRAGChain(baseOrchestrator):
    def __init__(self, structured_data):
        self.structured_data = structured_data
        self.retriever = vectorStoreRetriever(self.structured_data)
        self.compliance_question = self.load_compliance_questions(
            file_path="D:\\Assessment\\ManulifeAssessment\\Manulife_assessment\\backend\\src\\utils\\questions\\complianceQuestion.json"
        )
        self.qa_chain = None

    def run_RAG_model(self, model_type="llama"):
        vector_store = self.retriever.vector_store

        if model_type == "llama":
            try:
                self.qa_chain = build_llama_rag_model(
                    vector_store=vector_store,
                    output_parser=self.output_parser()
                )
            except Exception as llama_error:
                print(
                    f"[WARN] LLaMA failed, falling back to Gemini: {llama_error}")
                self.qa_chain = build_gemini_rag_model(
                    vector_store=vector_store,
                    output_parser=self.output_parser()
                )

        elif model_type == "gemini":
            self.qa_chain = build_gemini_rag_model(
                vector_store=vector_store,
                output_parser=self.output_parser()
            )
        else:
            raise ValueError(f"Unsupported model_type: {model_type}")

    def query_rag_model(self, question):
        """
        Query RetrievalQA and parse structured output
        """
        result = self.qa_chain.invoke({"query": question})

        parsed_output = self.output_parser().parse(result["result"])

        return {
            **parsed_output,
            "source_documents": result["source_documents"]
        }

    def run_compliance_loop(self):
        output = []

        questions = self.compliance_question["contract_audit_config"]["questions"]

        for q in questions:
            combined_question = f"{q['pre_condition']} {q['question']}"

            result = self.query_rag_model(combined_question)

            output.append({
                "Compliance Question": q["title"],
                "Compliance State": result["compliance_state"],
                "Confidence": result["confidence"],
                "Relevant Quotes": result["relevant_quotes"],
                "Rationale": result["rationale"]
            })

        self.save_output_json(output, file_path="complianceResults.json")
        return output
