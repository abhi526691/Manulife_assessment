# 📘 Usage Guide - Contract Compliance Analyzer

## Table of Contents

1. [Getting Started](#getting-started)
2. [User Interface Walkthrough](#user-interface-walkthrough)
3. [Compliance Analysis Workflow](#compliance-analysis-workflow)
4. [Chat Assistant Features](#chat-assistant-features)
5. [Advanced Usage](#advanced-usage)
6. [Best Practices](#best-practices)
7. [Interpreting Results](#interpreting-results)

---

## Getting Started

### First-Time Setup

#### 1. Verify Installation

```bash
# Check Python version (requires 3.9+)
python --version

# Verify all dependencies installed
pip list | grep -E 'streamlit|langchain|faiss|mistralai'
```

#### 2. Validate API Keys

```bash
# Test environment variables loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('MISTRAL_API_KEY:', os.getenv('MISTRAL_API_KEY')[:10] + '...')"
```

#### 3. Launch Application

```bash
streamlit run app.py
```

Expected output:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## User Interface Walkthrough

### Page 1: Document Upload

#### Interface Elements

- **Header**: "Contract Compliance Analyzer" with Manulife branding
- **File Uploader**: Drag-and-drop or click to browse
- **Accepted Format**: PDF only

#### Upload Process

1. Click the file uploader or drag PDF into the box
2. System displays: "📥 Processing document with OCR..."
3. Progress spinner appears: "Extracting document content..."
4. Automatic redirect to Document View (typically 10-30 seconds)

#### Troubleshooting Upload

| Issue                     | Cause                 | Solution                             |
| ------------------------- | --------------------- | ------------------------------------ |
| "File type not supported" | Non-PDF file uploaded | Convert to PDF using Adobe Acrobat   |
| OCR timeout               | Large file (>50MB)    | Split document into smaller sections |
| API error                 | Invalid Mistral key   | Check `.env` file for correct key    |

---

### Page 2: Document View

#### Layout

```
┌─────────────────────────────────────────────────────────┐
│  📄 Contract Compliance Analyzer                        │
│     Extracted Document                                  │
├─────────────────────────────────────────────────────────┤
│  [⬅️ Back to Upload]           [📊 View Results] →     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │                                                   │ │
│  │   Rendered Markdown Content                       │ │
│  │   (Scrollable, formatted text)                    │ │
│  │                                                   │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  Status: 🔍 Compliance analysis running…                │
└─────────────────────────────────────────────────────────┘
```

#### Features

- **Markdown Rendering**: Tables, headers, and lists displayed with proper formatting
- **Scrollable Container**: 68vh height with overflow support
- **Status Bar**: Real-time updates on analysis progress
- **Auto-Navigation**: Redirects to Results page when analysis completes

#### Background Processing

While viewing the document, the system:

1. Loads compliance questions from `complianceQuestion.json`
2. Retrieves relevant sections using vector search
3. Generates assessments for each question using Llama/Gemini
4. Parses structured JSON outputs
5. Saves results to `results/complianceResults.json`

**Expected Duration**: 30-90 seconds for 5 questions

---

### Page 3: Compliance Results

#### Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  ✅ Compliance Analysis Results                                     │
│     Automated contract review                                       │
├─────────────────────────────────────────────────────────────────────┤
│  [⬅️ Back to Document]                                              │
│  💬 AI Assistant is now available in the sidebar!                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Compliance Question │ State │ Score │ Quotes │ Rationale    │   │
│  ├─────────────────────────────────────────────────────────────┤   │
│  │ Password Mgmt       │ ✅    │  87   │ Sec 6.7│ Contract     │   │
│  │ IT Asset Mgmt       │ ⚠️    │  62   │ Sec 4.2│ specifies... │   │
│  │ Security Training   │ ❌    │  23   │ N/A    │ No evidence  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

SIDEBAR:
┌─────────────────────────┐
│ 💬 AI Assistant         │
├─────────────────────────┤
│ [Chat messages]         │
│                         │
│ 💬 Your question:       │
│ [Text area]             │
│ [📤 Send] [🗑️ Clear]   │
└─────────────────────────┘
```

#### Compliance Table Columns

1. **Compliance Question**: Short title from `complianceQuestion.json`
2. **State**: Color-coded status
   - 🟢 **Fully Compliant**: Green background
   - 🟡 **Partially Compliant**: Orange background
   - 🔴 **Non-Compliant**: Red background
3. **Score**: Confidence percentage (0-100)
4. **Relevant Quotes**: Extracted section references
5. **Rationale**: 2-4 sentence justification

#### Interactivity

- **Hover Effects**: Rows highlight with light green background
- **Scrollable**: 750px height with vertical scroll
- **Chat Unlock**: Notification appears when assistant is ready

---

## Compliance Analysis Workflow

### How the System Works

#### Step 1: Question Loading

```python
# From complianceQuestion.json
{
  "id": 1,
  "title": "Password Management",
  "pre_condition": "The contract must require...",
  "question": "Does the vendor maintain...",
  "search_keywords": ["password", "hashing"],
  "category": "Access Control"
}
```

#### Step 2: Vector Retrieval

1. User's combined question: `{pre_condition} {question}`
2. Question embedded using `all-MiniLM-L6-v2`
3. Top 3 similar sections retrieved from FAISS
4. Sections passed as `{context}` to LLM

#### Step 3: LLM Reasoning

The prompt instructs the LLM to:

1. **Understand broader principles** (Step-back reasoning)
2. **Map evidence to requirements** (Component breakdown)
3. **Assess evidence quality** (Specificity, obligation level, verifiability)
4. **Determine compliance state** (Fully/Partially/Non)
5. **Calibrate confidence** (0-100 rubric)
6. **Extract supporting quotes** (Verbatim with section refs)
7. **Generate rationale** (Concise justification)

#### Step 4: Output Parsing

```json
{
  "compliance_state": "Partially Compliant",
  "confidence": 67,
  "relevant_quotes": "Section 6.7 (...); Exhibit G13 (...)",
  "rationale": "The contract requires MFA for admin access (Sec 6.7) but lacks specifics on session logging."
}
```

#### Step 5: Result Aggregation

All 5 assessments saved to `results/complianceResults.json` and displayed in table.

---

## Chat Assistant Features

### When Chat Unlocks

- ✅ After compliance analysis completes
- ✅ When `qa_chain` is successfully initialized
- ✅ Indicated by: "💬 AI Assistant is now available in the sidebar!"

### Chat Interface Components

#### 1. Chat Header

```
┌─────────────────────────┐
│ 💬 AI Assistant         │
│ Ask questions about     │
│ your contract           │
└─────────────────────────┘
```

#### 2. Message History

- **User Messages**: Light green background, left-aligned
- **AI Messages**: Gray background, right-aligned
- **Icons**: 👤 (User), 🤖 (Assistant)
- **Empty State**: "💭 No messages yet. Start a conversation!"

#### 3. Input Area

- **Text Area**: Multi-line input (100px height)
- **Placeholder**: "e.g., What are the payment terms in this contract?"
- **Buttons**:
  - **📤 Send**: Primary action (blue)
  - **🗑️ Clear**: Secondary action (gray)

### Sample Interactions

#### Example 1: Factual Query

**User**: "Does the vendor require MFA for admin access?"  
**AI**: "Yes, according to Section 6.7, the vendor requires multi-factor authentication (MFA) for all administrative accounts. Specifically, the contract states 'Admin access SHALL require MFA via SAML or OAuth providers.'"

#### Example 2: Open-Ended Query

**User**: "What are the payment terms?"  
**AI**: "The contract specifies NET-30 payment terms in Section 8.4. Payments are due within 30 days of invoice receipt. Late payments incur a 1.5% monthly interest charge as outlined in Exhibit F."

#### Example 3: Out-of-Scope Query

**User**: "What's the weather today?"  
**AI**: "I am sorry, but the provided contract sections do not contain information regarding weather. I can only answer questions based on the uploaded document."

### Chat Best Practices

1. **Be specific**: "What's the data retention period?" vs. "Tell me about data"
2. **Reference sections**: "Explain Section 6.7" for targeted answers
3. **Ask follow-ups**: Build on previous answers for deeper insights
4. **Clear history**: Use Clear button when switching topics

---

## Advanced Usage

### Programmatic API

#### Run Compliance Without UI

```python
from src.parser.mistral_ocr_convertor import textExtractor
from src.orchestator.compliance_runner import run_compliance

# Extract document
extractor = textExtractor(pdf_path="contracts/vendor_agreement.pdf")
result = extractor.ocr_response_file()

# Run analysis
compliance_results = run_compliance(result["structured_json"])

# Access results
for item in compliance_results:
    print(f"{item['Compliance Question']}: {item['Compliance State']}")
```

#### Custom Q&A Loop

```python
from src.orchestator.compliance_runner import run_qna, ask_bot

# Initialize chat
qa_chain = run_qna(result["structured_json"], chat_type=True)

# Ask multiple questions
questions = [
    "What's the termination notice period?",
    "Are subprocessors allowed?",
    "What are the audit rights?"
]

for q in questions:
    answer = ask_bot(qa_chain, q)
    print(f"Q: {q}\nA: {answer}\n")
```

### Batch Processing

```python
import os
from pathlib import Path

contracts_dir = Path("input_files/batch")
results = []

for pdf_file in contracts_dir.glob("*.pdf"):
    print(f"Processing {pdf_file.name}...")

    extractor = textExtractor(pdf_path=str(pdf_file))
    result = extractor.ocr_response_file()

    compliance = run_compliance(result["structured_json"])
    results.append({
        "file": pdf_file.name,
        "compliance": compliance
    })

# Save batch results
import json
with open("batch_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

---

## Best Practices

### Document Preparation

1. **Scan Quality**: Use high-resolution PDFs (300+ DPI)
2. **Text-Based PDFs**: Avoid image-only scans (reduces OCR accuracy)
3. **File Size**: Keep under 25MB for optimal performance
4. **Structure**: Ensure clear section headers for better parsing

### Question Customization

```json
// Good Question
{
  "title": "Encryption Standards",
  "pre_condition": "The contract must specify AES-256 or equivalent for data at rest.",
  "question": "Does the vendor commit to AES-256 encryption for all stored Company Data?",
  "search_keywords": ["encryption", "AES", "cipher", "at-rest"]
}

// Poor Question (too vague)
{
  "title": "Security",
  "question": "Is the vendor secure?",
  "search_keywords": ["security"]
}
```

### Prompt Engineering Tips

1. **Be explicit**: "Must include specific metrics" vs. "Should be detailed"
2. **Use examples**: "e.g., 99.9% uptime SLA"
3. **Define scope**: "Refer only to Sections 1-10"
4. **Set constraints**: "Limit quotes to 15 words"

### Interpreting Confidence Scores

| Score Range | Interpretation                       | Action                          |
| ----------- | ------------------------------------ | ------------------------------- |
| **85-96**   | High certainty, explicit evidence    | Accept assessment               |
| **70-84**   | Moderate certainty, some gaps        | Manual verification recommended |
| **50-69**   | Low certainty, vague language        | Require contract amendment      |
| **< 50**    | Very low certainty, weak/no evidence | Reject or renegotiate           |

---

## Interpreting Results

### Compliance States Explained

#### ✅ Fully Compliant

**Criteria**:

- ALL requirement components explicitly addressed
- Mandatory language (shall/must/required)
- Specific, measurable commitments
- No ambiguities or contradictions

**Example**:

> "Section 6.7 requires MFA for all admin accounts using SAML 2.0 or OAuth 2.0 providers, with session logging to SIEM systems."

#### ⚠️ Partially Compliant

**Criteria**:

- SOME components addressed OR
- Weak language (should/may/reasonable) OR
- Notable gaps in coverage OR
- Vague commitments

**Example**:

> "Section 6.7 mentions MFA for 'critical systems' but doesn't define scope or specify protocols."

#### ❌ Non-Compliant

**Criteria**:

- Most/all components missing OR
- Contract contradicts requirement OR
- Only generic security statements

**Example**:

> "Contract only states 'Vendor shall maintain industry-standard security practices' with no MFA reference."

### Rationale Analysis

Look for these red flags in rationales:

- **"Contract only states..."**: Indicates vague language
- **"No specific mention of..."**: Missing critical component
- **"Limited to..."**: Scope restriction issue
- **"Contradicts in Section X..."**: Internal inconsistency

### Quote Verification

Always cross-check quotes:

1. Open the Document View (Page 2)
2. Use browser search (Ctrl+F) to find section reference
3. Verify quote context matches LLM interpretation
4. Check for qualifying language ("unless", "except")

---

## Troubleshooting Common Issues

### Issue: Chat Not Responding

**Symptoms**: Send button clicked, but no response appears  
**Causes**:

1. `qa_chain` not initialized properly
2. LLM API quota exceeded
3. Network timeout

**Solutions**:

```bash
# Check logs
streamlit run app.py --logger.level=debug

# Verify API keys
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GROQ_API_KEY'))"

# Test QA chain manually
python
>>> from src.orchestator.compliance_runner import run_qna
>>> qa_chain = run_qna(structured_json, chat_type=True)
```

### Issue: Low Confidence Scores Across Board

**Symptoms**: All scores < 50  
**Causes**:

1. Poor document quality (OCR errors)
2. Contract lacks specific language
3. Retrieval returning irrelevant sections

**Solutions**:

1. Re-upload higher quality PDF
2. Check extracted markdown for garbled text
3. Adjust `search_keywords` in `complianceQuestion.json`
4. Increase `k` parameter in `vector_store.py` (default: 3)

### Issue: Compliance State Mismatch

**Symptoms**: State says "Fully Compliant" but rationale mentions gaps  
**Causes**: LLM output parsing error or prompt instruction conflict

**Solutions**:

1. Check `results/complianceResults.json` for raw output
2. Review `stepback_prompting.py` for conflicting instructions
3. Increase LLM temperature (currently 1.0) for more conservative outputs

---

## Next Steps

After reviewing results:

1. **Export data**: Save `complianceResults.json` for audit trails
2. **Request amendments**: Share specific gaps with vendor legal team
3. **Iterate**: Re-upload amended contracts for re-assessment
4. **Integrate**: Use programmatic API for CI/CD pipelines

---

**For additional support, contact**: [support@manulife.com]
