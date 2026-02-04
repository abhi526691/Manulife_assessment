import json
import re
import os
from langchain_classic.output_parsers import ResponseSchema, StructuredOutputParser


class baseOrchestrator:
    def __init__(self):
        pass

    def load_compliance_questions(self, file_path="complianceQuestion.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse_llm_output(self, answer_text: str):
        """
        Extract and parse JSON from LLM output that may be wrapped in ```json fences.
        """

        if not answer_text:
            return {
                "compliance_state": "",
                "confidence": "",
                "relevant_quotes": [],
                "rationale": ""
            }

        # 1. Remove ```json ... ``` or ``` ... ```
        cleaned = re.sub(r"^```(?:json)?\s*", "",
                         answer_text.strip(), flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)

        # 2. Attempt JSON parse
        try:
            parsed = json.loads(cleaned)
            return {
                "compliance_state": parsed.get("compliance_state", ""),
                "confidence": f"{parsed.get('confidence', '')}%",
                "relevant_quotes": parsed.get("relevant_quotes", []),
                "rationale": parsed.get("rationale", "")
            }
        except json.JSONDecodeError:
            # 3. Hard fallback (never lose the answer)
            return {
                "compliance_state": "",
                "confidence": "",
                "relevant_quotes": [],
                "rationale": answer_text
            }

    def save_output_json(self, results, file_path="complianceResults.json"):
        results_dir = "results"
        # create folder if it doesn't exist
        os.makedirs(results_dir, exist_ok=True)

        full_path = os.path.join(results_dir, file_path)

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"Results saved to: {full_path}")

    def output_parser(self):
        self.response_schemas = [
            ResponseSchema(
                name="compliance_state",
                description="Compliance determination: Fully Compliant, Partially Compliant, or Non-Compliant"
            ),
            ResponseSchema(
                name="confidence",
                description="Integer confidence score between 0 and 100"
            ),
            ResponseSchema(
                name="relevant_quotes",
                description=(
                    "Single concise citation-style string listing all relevant sections "
                    "and exhibits separated by semicolons. Example: "
                    "Section 6.7 (+ Authentication/Authorization Summary Table); "
                    "Section 6.2 (MFA); Exhibit G13 (NET-01–NET-03)."
                )
            ),
            ResponseSchema(
                name="rationale",
                description="Concise explanation referencing contract sections and gaps if any"
            )
        ]

        return StructuredOutputParser.from_response_schemas(self.response_schemas)
