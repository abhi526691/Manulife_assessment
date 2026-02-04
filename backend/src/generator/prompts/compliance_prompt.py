PROMPT_TEMPLATE = """You are a compliance analyst reviewing a vendor contract. Your task is to determine if the contract meets a specific compliance requirement.

**COMPLIANCE REQUIREMENT:**
Name: {question['name']}
Pre-condition: {question['pre_condition']}
Question: {question['question']}
Category: {question['category']}

**RELEVANT CONTRACT SECTIONS:**
{sections_text}

**ANALYSIS TASK:**
Based on the contract sections above, determine the compliance state for this requirement. You must:

1. Carefully read all relevant sections
2. Identify specific contract language that addresses (or fails to address) each part of the requirement
3. Determine if the contract is:
   - **Fully Compliant**: All aspects of the requirement are explicitly addressed with appropriate controls
   - **Partially Compliant**: Some aspects are addressed but others are missing or inadequate
   - **Non-Compliant**: The requirement is not addressed or explicitly contradicted

4. Extract exact quotes from the contract that support your determination (include section references)
5. Provide clear rationale explaining your assessment

**OUTPUT FORMAT:**
You must respond with a valid JSON object with this exact structure:
{{
    "compliance_state": "Fully Compliant" | "Partially Compliant" | "Non-Compliant",
    "confidence": <number between 0 and 100>,
    "relevant_quotes": [
        "Section X.Y: 'exact quote from contract'",
        "Exhibit Z: 'another relevant quote'"
    ],
    "rationale": "Detailed explanation of why you assigned this compliance state, referencing specific contract provisions and identifying any gaps."
}}

**IMPORTANT GUIDELINES:**
- Be precise: Only mark as "Fully Compliant" if ALL aspects of the requirement are met
- Quote accurately: Use exact quotes with section references
- Be thorough: Check for requirements in both main sections and exhibits
- Consider tables and structured data: Many requirements are in exhibits or tables
- Assign confidence based on clarity of contract language (high=explicit, medium=implicit, low=ambiguous)

Provide your analysis now:"""
