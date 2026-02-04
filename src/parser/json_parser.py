from langchain_classic.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal


class ComplianceOutput(BaseModel):
    compliance_state: Literal["Fully Compliant",
                              "Partially Compliant", "Non-Compliant"]
    confidence: int = Field(ge=0, le=100, description="Confidence score 0-100")
    relevant_quotes: str = Field(description="Citation string with sections")
    rationale: str = Field(description="2-4 sentence justification")


def get_compliance_parser():
    return PydanticOutputParser(pydantic_object=ComplianceOutput)
