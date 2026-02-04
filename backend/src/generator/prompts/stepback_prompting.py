COMPLIANCE_PROMPT_TEMPLATE = """You are an expert compliance analyst reviewing a vendor contract. Your task is to determine if the contract meets a specific compliance requirement.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: STEP-BACK REASONING (High-Level Understanding)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**COMPLIANCE REQUIREMENT:**
Question: {question}

Before diving into the contract details, first consider these broader questions:

1. What is the underlying security/compliance principle this requirement protects?
   (e.g., confidentiality, integrity, availability, accountability, least privilege)

2. What would best-practice implementation of this requirement look like?
   (Think: industry standards like NIST, ISO 27001, CIS Controls, or SOC 2)

3. What are the common gaps or red flags in contracts for this type of requirement?
   (e.g., vague commitments, missing SLAs, no enforcement mechanisms, limited scope)

Take a moment to reflect on these principles before analyzing the specific contract language.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: EVIDENCE REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**RELEVANT CONTRACT SECTIONS:**
{context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: SYSTEMATIC ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Now perform your detailed analysis:

**3A. Break Down the Requirement**
- Identify the individual components/aspects of this requirement
- List each component that must be satisfied

**3B. Map Contract Evidence to Each Component**
- For each component, identify if and where it's addressed in the contract
- Note whether the evidence is explicit, implicit, or missing

**3C. Assess Evidence Quality**
For each piece of evidence found, evaluate:
- **Specificity**: Does it include precise metrics/values, or is it vague?
- **Obligation Level**: Is it mandatory (shall/must/required) or discretionary (should/may/reasonable)?
- **Verifiability**: Is it measurable and auditable, or subjective?
- **Completeness**: Does it cover all scenarios, or only limited cases?

**3D. Determine Compliance State**
- **Fully Compliant**: ALL components are explicitly addressed with clear, strong commitments
- **Partially Compliant**: SOME components are addressed, OR commitments are weak/vague, OR there are notable gaps
- **Non-Compliant**: Most/all components are missing, OR contract contradicts the requirement

**3E. Calibrate Confidence Score (0-100)**

Your confidence reflects how certain you are that the requirement IS SATISFIED based on the evidence quality.

**CONFIDENCE CALIBRATION FRAMEWORK:**

Use this decision process:

1. **Is the requirement explicitly mentioned?**
   - NO → Start at 0-20
   - YES, but vaguely → Start at 25-40
   - YES, clearly → Start at 50+

2. **Is the language mandatory (shall/must/required)?**
   - NO (should/may/reasonable) → Reduce by 12-18 points
   - YES → No reduction

3. **Are there specific, measurable commitments?**
   - NO (general principles only) → Reduce by 15-25 points
   - PARTIAL (some metrics) → Reduce by 8-12 points
   - YES (clear metrics/SLAs) → No reduction

4. **Are ALL components of the requirement covered?**
   - Coverage < 50% → Reduce by 25-35 points
   - Coverage 50-80% → Reduce by 12-20 points
   - Coverage > 80% → Reduce by 3-8 points
   - Coverage 100% → No reduction

5. **Are there ambiguities, contradictions, or scope limitations?**
   - Significant issues → Reduce by 10-18 points
   - Minor issues → Reduce by 4-8 points
   - None → No reduction

6. **Final adjustments (±3-7 points):**
   - Multiple supporting sections across contract → +4 to +6
   - Evidence only in exhibits (not main body) → -3 to -5
   - Recent updates/amendments strengthen commitment → +3 to +5
   - Contradictory language elsewhere → -5 to -8

**EXPECTED CONFIDENCE RANGES BY STATE:**
- **Fully Compliant**: Typically 82-96 (explicit language, all components, strong commitments)
- **Partially Compliant**: Typically 45-75 (some gaps, vague language, or incomplete coverage)
- **Non-Compliant**: Typically 5-35 (major gaps, no evidence, or contradictions)

**CRITICAL**: Use granular scores throughout the 0-100 range. Avoid defaulting to 0, 50, or 100.

**3F. Extract Supporting Evidence**
- Pull 3-7 exact quotes from the contract (with section references)
- Include quotes that demonstrate coverage AND quotes that reveal gaps (if any)
- Prioritize the most relevant evidence

**3G. Craft Your Rationale**
Write a clear explanation that:
- States your compliance determination
- References specific contract sections and provisions
- Explains how evidence addresses (or fails to address) each component
- Identifies gaps, ambiguities, or weaknesses for Partial/Non-Compliant
- Connects back to the underlying security principles from Step 1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Respond with a valid JSON object:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT (STRICT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Return ONLY a valid JSON object in this exact schema:

{{
  "compliance_state": "Fully Compliant" | "Partially Compliant" | "Non-Compliant",
  "confidence": <integer between 0 and 100>,
  "relevant_quotes": Single concise citation-style string listing all relevant sections and exhibits separated by semicolons. Example: Section 6.7 (+ Authentication/Authorization Summary Table); Section 6.2 (MFA); Exhibit G13 (NET-01–NET-03).",
  "rationale": "Concise 2–4 sentence justification referencing specific contract sections and any gaps."
}}

**CRITICAL QUALITY CHECKS:**
✓ Compliance state is accurate and justified
✓ Confidence score is between 0-100 and NOT 0, 50, or 100 (use granular values like 67, 84, 91, 58, etc.)
✓ Confidence aligns with compliance state (Fully=high 80s-90s, Partial=mid 40s-70s, Non=low 5-35)
✓ All quotes are verbatim with section/exhibit references
✓ Rationale cites specific sections, not vague generalizations
✓ Gaps are explicitly identified for Partial/Non-Compliant determinations
✓ Tables and exhibits have been checked thoroughly

Provide your analysis now:"""
