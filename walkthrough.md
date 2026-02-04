# 🚶 Complete Walkthrough - Contract Compliance Analyzer

This walkthrough provides a comprehensive, step-by-step guide to using the Contract Compliance Analyzer, from initial setup to advanced customization.

---

## 📋 Table of Contents

1. [Pre-Flight Checklist](#pre-flight-checklist)
2. [Installation Walkthrough](#installation-walkthrough)
3. [First Run: Sample Contract Analysis](#first-run-sample-contract-analysis)
4. [Deep Dive: Understanding Each Component](#deep-dive-understanding-each-component)
5. [Customization Walkthrough](#customization-walkthrough)
6. [Production Deployment](#production-deployment)
7. [Troubleshooting Scenarios](#troubleshooting-scenarios)

---

## Pre-Flight Checklist

### Before You Begin

- [ ] Python 3.9 or higher installed (`python --version`)
- [ ] Git installed (optional, for cloning)
- [ ] API keys obtained:
  - [ ] Mistral API key ([platform.mistral.ai](https://platform.mistral.ai))
  - [ ] Google API key ([aistudio.google.com](https://aistudio.google.com))
  - [ ] Groq API key ([console.groq.com](https://console.groq.com))
- [ ] At least 2GB free disk space
- [ ] Stable internet connection
- [ ] PDF contract ready for testing (or use provided sample)

---

## Installation Walkthrough

### Step 1: Get the Code

#### Option A: Clone from Git

```bash
git clone https://github.com/your-org/contract-compliance-analyzer.git
cd contract-compliance-analyzer
```

#### Option B: Download ZIP

1. Download the project archive
2. Extract to your desired location
3. Open terminal in the extracted folder

**Verification**:

```bash
# You should see these files:
ls
# Output: app.py  requirements.txt  src/  input_files/  .sample.env  ...
```

---

### Step 2: Create Virtual Environment

#### Why Virtual Environments?

Virtual environments isolate project dependencies, preventing conflicts with other Python projects.

#### On macOS/Linux:

```bash
# Create venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Verify activation (prompt should show "(venv)")
which python
# Output: /path/to/project/venv/bin/python
```

#### On Windows:

```bash
# Create venv
python -m venv venv

# Activate
venv\Scripts\activate

# Verify
where python
# Output: C:\path\to\project\venv\Scripts\python.exe
```

**Troubleshooting**:

- **"command not found: python3"**: Try `python` instead
- **Permission denied**: Run `chmod +x venv/bin/activate` (Linux/Mac)
- **Execution policy error** (Windows): Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell

---

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Verify installation
pip list | grep streamlit
# Expected: streamlit==1.30.0 (or higher)
```

**Common Issues**:
| Error | Solution |
|-------|----------|
| `error: Microsoft Visual C++ 14.0 is required` (Windows) | Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) |
| `pip: command not found` | Use `python -m pip install -r requirements.txt` |
| `Could not find a version that satisfies` | Update Python to 3.9+ |

**Expected Duration**: 3-5 minutes

---

### Step 4: Configure Environment Variables

```bash
# Copy sample env file
cp .sample.env .env

# Open in text editor
# macOS: open .env
# Linux: nano .env
# Windows: notepad .env
```

**Fill in the following**:

```dotenv
# Required: Mistral API for OCR
MISTRAL_API_KEY=sk-mistral-your-key-here-abc123

# Required: Google API for Gemini (fallback LLM)
GOOGLE_API_KEY=AIzaSyYour-Google-Key-Here-xyz789

# Required: Groq API for Llama (primary LLM)
GROQ_API_KEY=gsk_your-groq-key-here-def456

# Required: Path to compliance questions
COMPLIANCE_QUESTIONS_PATH=src/utils/questions/complianceQuestion.json
```

**Obtaining API Keys**:

#### Mistral API

1. Visit [platform.mistral.ai](https://platform.mistral.ai)
2. Sign up / Log in
3. Navigate to API Keys
4. Click "Create New Key"
5. Copy key (starts with `sk-mistral-...`)

#### Google (Gemini)

1. Visit [aistudio.google.com](https://aistudio.google.com)
2. Click "Get API Key"
3. Create new project or select existing
4. Copy key (starts with `AIza...`)

#### Groq (Llama)

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up with GitHub/Google
3. Go to API Keys section
4. Generate new key
5. Copy key (starts with `gsk_...`)

**Verification**:

```bash
# Test environment loading
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ Mistral Key:', os.getenv('MISTRAL_API_KEY')[:15] + '...')"
```

---

### Step 5: Launch Application

```bash
streamlit run app.py
```

**Expected Output**:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.10:8501

  For better performance, install the Watchdog module:

  $ pip install watchdog
```

**Auto-Open**: Browser should automatically open to `http://localhost:8501`

**If browser doesn't open**:

1. Manually visit `http://localhost:8501`
2. Check firewall settings
3. Try `streamlit run app.py --server.port=8502` (different port)

---

## First Run: Sample Contract Analysis

### Phase 1: Upload Document

#### Step 1: Navigate to Upload Page

You should see:

```
┌─────────────────────────────────────────┐
│   📄 Contract Compliance Analyzer       │
│        Powered by Manulife              │
├─────────────────────────────────────────┤
│                                         │
│   [Drag and drop file here]             │
│   Limit 200MB per file • PDF            │
│                                         │
└─────────────────────────────────────────┘
```

#### Step 2: Select Sample Contract

```bash
# Use provided sample
input_files/Sample Contract.pdf
```

**Or use your own contract** (ensure it's a vendor/supplier agreement with security clauses).

#### Step 3: Monitor Upload Progress

1. Click "Browse files" button
2. Select `Sample Contract.pdf`
3. Watch for status messages:
   - "📥 Processing document with OCR..."
   - "Extracting document content..."
   - Progress spinner (typically 15-30 seconds)

**Behind the Scenes**:

```python
# What happens during upload:
1. File read into memory
2. Uploaded to Mistral API via `client.files.upload()`
3. Signed URL generated for OCR processing
4. `mistral-ocr-latest` model converts PDF → Markdown
5. Structured JSON created with section metadata
6. Files saved to:
   - src/parser/markdown_files/input_data_markdown/extracted_markdown.md
   - src/parser/Json_files/input_data_json/structured_output.json
```

#### Step 4: Automatic Redirect

Once complete, you'll be redirected to the **Document View** page.

---

### Phase 2: Review Extracted Document

#### Step 5: Verify Extraction Quality

The Document View displays the contract as formatted Markdown:

**Good Indicators**:

- ✅ Section headers visible (e.g., "## 6.2 Authentication")
- ✅ Tables rendered properly
- ✅ Lists and bullets formatted correctly
- ✅ No excessive "|||||||" or garbled characters

**Poor Indicators**:

- ❌ Large blocks of unformatted text
- ❌ Missing section headers
- ❌ Tables collapsed into single lines
- ❌ Symbols like "§", "¶" misrendered

**If extraction quality is poor**:

1. Click "⬅️ Back to Upload"
2. Try a higher-resolution PDF
3. Use Adobe Acrobat to "Recognize Text" (OCR) first
4. Re-upload

#### Step 6: Monitor Compliance Analysis

While viewing the document, notice the status bar:

```
Status: 🔍 Compliance analysis running…
```

**Processing Steps**:

1. Loads 5 questions from `complianceQuestion.json`
2. For each question:
   - Combines `pre_condition + question`
   - Retrieves top 3 relevant sections from FAISS
   - Sends to Llama 3.1 via Groq API
   - Parses structured JSON response
   - Saves to `compliance_results` list
3. Aggregates all results
4. Saves to `results/complianceResults.json`

**Expected Duration**: 30-90 seconds (depends on API speed)

#### Step 7: Navigate to Results

When analysis completes:

```
Status: ✅ Compliance analysis completed
```

The "📊 View Compliance Results" button appears (top-right). Click it.

---

### Phase 3: Interpret Compliance Results

#### Step 8: Read the Compliance Table

You'll see a table with 5 rows (one per question):

**Example Row**:

```
┌───────────────────┬──────────────────┬───────┬───────────────────────┬────────────────────┐
│ Compliance        │ State            │ Score │ Relevant Quotes       │ Rationale          │
│ Question          │                  │       │                       │                    │
├───────────────────┼──────────────────┼───────┼───────────────────────┼────────────────────┤
│ Password          │ Fully Compliant  │  87   │ Section 6.7 (Password │ The contract       │
│ Management        │ (GREEN)          │       │ Policy); Exhibit G    │ explicitly requires│
│                   │                  │       │ (Authentication Table)│ 14+ chars for admin│
│                   │                  │       │                       │ and SHA-256 hashing│
└───────────────────┴──────────────────┴───────┴───────────────────────┴────────────────────┘
```

#### Step 9: Analyze Each Result

**Question 1: Password Management**

- **Expected State**: Fully Compliant (if sample contract has Section 6.7)
- **Key Indicators**: Confidence 85+, mentions specific algorithms (SHA-256), character lengths
- **Red Flags**: Score < 60, "No explicit mention of..."

**Question 2: IT Asset Management**

- **Expected State**: Partially Compliant
- **Key Indicators**: Mentions inventory but lacks quarterly review commitment
- **Red Flags**: "Reasonable effort" language instead of "SHALL maintain"

**Question 3: Security Training**

- **Expected State**: Varies by contract
- **Key Indicators**: "Annual training", "Background checks", "All personnel"
- **Red Flags**: "Training may be provided" (discretionary language)

**Question 4: Data in Transit Encryption**

- **Expected State**: Fully Compliant
- **Key Indicators**: "TLS 1.2 or higher", "AES-256 ciphers"
- **Red Flags**: "Industry-standard encryption" (vague)

**Question 5: Network Authentication**

- **Expected State**: Partially Compliant
- **Key Indicators**: MFA required, bastion hosts mentioned
- **Red Flags**: No session logging commitment

#### Step 10: Verify Quotes

For any surprising result:

1. Click "⬅️ Back to Document"
2. Use Ctrl+F (Cmd+F on Mac) to search for quoted section (e.g., "Section 6.7")
3. Read full context
4. Check for qualifying language:
   - "Except as otherwise noted..."
   - "To the extent commercially reasonable..."
   - "Unless prohibited by law..."

---

### Phase 4: Use Chat Assistant

#### Step 11: Activate Chat

Once results load, you'll see:

```
💬 AI Assistant is now available in the sidebar!
```

The sidebar changes from:

```
┌──────────────────────┐
│ 🔒 Chat Locked       │
│ Complete compliance  │
│ analysis to unlock   │
└──────────────────────┘
```

To:

```
┌──────────────────────┐
│ 💬 AI Assistant      │
│ Ask questions about  │
│ your contract        │
├──────────────────────┤
│ 💭 No messages yet.  │
│ Start a conversation!│
├──────────────────────┤
│ 💬 Your question:    │
│ [Text area]          │
│ [📤 Send] [🗑️ Clear]│
└──────────────────────┘
```

#### Step 12: Ask Your First Question

**Suggested Starter Questions**:

1. "What is the termination notice period?"
2. "Does the vendor allow subprocessors?"
3. "What are the data retention requirements?"
4. "Explain the liability cap in Section 10"
5. "Are there any auto-renewal clauses?"

**Example Interaction**:

```
👤 You:
What is the data retention period after contract termination?

[📤 Send clicked]

🤖 AI Assistant:
According to Section 9.4 (Data Deletion), the vendor SHALL delete or return all Company Data within 30 days following contract termination. Backups may be retained for up to 90 days for disaster recovery purposes, after which they must be irreversibly destroyed.
```

#### Step 13: Test Chat Capabilities

**Test 1: Factual Retrieval**

```
Question: "Does Section 6.7 require MFA?"
Expected: Specific answer referencing exact clause
```

**Test 2: Out-of-Scope**

```
Question: "What's the capital of France?"
Expected: "I am sorry, but the provided contract sections do not contain information regarding..."
```

**Test 3: Complex Reasoning**

```
Question: "What happens if the vendor experiences a data breach affecting our systems?"
Expected: Multi-part answer citing breach notification (Sec 11), liability (Sec 10), and termination rights (Sec 12)
```

#### Step 14: Clear Chat History

When switching contexts:

1. Click "🗑️ Clear" button
2. Confirm all messages removed
3. Start fresh conversation

---

## Deep Dive: Understanding Each Component

### Component 1: OCR Pipeline (Mistral)

#### How It Works

```python
# From mistral_ocr_convertor.py

1. File Upload to Mistral API
   client.files.upload(
       file={"file_name": "contract.pdf", "content": pdf_bytes},
       purpose="ocr"
   )

2. Generate Signed URL (1-hour expiry)
   signed_url = client.files.get_signed_url(file_id=uploaded_file.id)

3. Process OCR
   pdf_response = client.ocr.process(
       document=DocumentURLChunk(document_url=signed_url.url),
       model="mistral-ocr-latest",
       include_image_base64=True  # Embeds images as base64
   )

4. Extract Markdown
   for page in pdf_response.pages:
       markdown += page.markdown

5. Parse Structure
   sections = MarkdownHeaderTextSplitter(
       headers_to_split_on=[("#", "Header_1"), ("##", "Header_2")]
   ).split_text(markdown)

6. Generate JSON
   {
     "title": "Scope",
     "content": "## 2.1 Scope\nThis agreement covers...",
     "block_type": "obligation",
     "keywords": ["scope", "agreement"]
   }
```

#### Customization Points

- **Image Handling**: Set `include_image_base64=False` to exclude images
- **Section Splitting**: Add `("###", "Header_3")` for subsections
- **Keyword Tagging**: Edit `auto_tag()` function in `pdf_parser.py`

---

### Component 2: Vector Store (FAISS)

#### How It Works

```python
# From vector_store.py

1. Generate Embeddings
   embeddings = HuggingFaceEmbeddings(
       model_name="sentence-transformers/all-MiniLM-L6-v2"
   ).embed_documents([section['content'] for section in structured_data])

2. Create FAISS Index
   index = faiss.IndexFlatL2(384)  # 384 = embedding dimension

3. Add Documents
   vector_store.add_texts([section['content'] for section in structured_data])

4. Retrieve (during question answering)
   retriever = vector_store.as_retriever(search_kwargs={"k": 3})
   relevant_docs = retriever.get_relevant_documents(question)
```

#### Tuning Parameters

```python
# Increase retrieved sections (default: 3)
search_kwargs={"k": 5}

# Change embedding model (for better semantic understanding)
model_name="sentence-transformers/all-mpnet-base-v2"  # Higher quality, slower

# Use similarity threshold
search_kwargs={"k": 3, "score_threshold": 0.7}  # Only return if >70% similar
```

---

### Component 3: LLM Orchestration

#### Primary: Llama 3.1 (via Groq)

```python
# From llama.py

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=1.0,  # Higher = more creative (range: 0-2)
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY")
)
```

**Why Llama 3.1?**

- ⚡ Fast inference (via Groq's LPU)
- 🎯 Strong reasoning for compliance tasks
- 💰 Cost-effective (free tier: 30 requests/min)

#### Fallback: Gemini Flash (Google)

```python
# From gemini.py

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=1.0,
    api_key=os.getenv("GOOGLE_API_KEY")
)
```

**When Used?**

- Groq API down/rate-limited
- Llama model fails to parse
- Specified via `model_type="gemini"` parameter

#### Automatic Fallback Logic

```python
# From chain.py

try:
    self.qa_chain = build_llama_rag_model(...)
except Exception as llama_error:
    print(f"[WARN] LLaMA failed, falling back to Gemini: {llama_error}")
    self.qa_chain = build_gemini_rag_model(...)
```

---

### Component 4: Prompting Strategy

#### Step-Back Prompting (Compliance Analysis)

```
Phase 1: High-Level Reasoning
  - What security principle does this requirement protect?
  - What does best-practice implementation look like?
  - Common red flags?

Phase 2: Evidence Review
  - Relevant contract sections provided

Phase 3: Systematic Analysis
  3A. Break down requirement into components
  3B. Map contract evidence to each component
  3C. Assess evidence quality (specificity, obligation, verifiability)
  3D. Determine compliance state
  3E. Calibrate confidence (0-100 rubric)
  3F. Extract supporting quotes
  3G. Craft rationale
```

**Benefits**:

- Reduces "hallucination" by forcing principle-first thinking
- Improves confidence calibration (avoids overconfident scores)
- Produces more detailed rationales

#### Grounded QA (Chat Assistant)

```
Step 1: Knowledge Scope Check
  - Is answer in provided context?

Step 2: Evidence Extraction
  - Identify supporting sections

Step 3: Response Construction
  - Single concise paragraph
  - Inline section references
  - Grounded in context only
```

**Benefits**:

- Prevents AI from using external knowledge
- Ensures transparency (always cites sources)
- Reduces false positives

---

## Customization Walkthrough

### Scenario 1: Add New Compliance Question

#### Step 1: Edit Questions File

```bash
nano src/utils/questions/complianceQuestion.json
```

#### Step 2: Add Question Object

```json
{
  "id": 6,
  "title": "Incident Response SLA",
  "pre_condition": "The contract must specify a maximum 24-hour response time for P1 security incidents.",
  "question": "Does the vendor commit to notifying Company within 24 hours of detecting a P1 security incident?",
  "search_keywords": [
    "incident",
    "breach",
    "notification",
    "24 hours",
    "SLA",
    "P1",
    "critical"
  ],
  "category": "Incident Management"
}
```

#### Step 3: Save and Restart

```bash
# Kill Streamlit (Ctrl+C)
# Restart
streamlit run app.py
```

#### Step 4: Verify

Upload a contract and check results table has 6 rows.

---

### Scenario 2: Change Confidence Scoring

#### Current Logic (in `stepback_prompting.py`)

```
Start at 0-20 if requirement not mentioned
+50 if explicitly mentioned
-12-18 for discretionary language
-15-25 for no measurable commitments
-25-35 for <50% component coverage
```

#### Custom Scoring (More Lenient)

Edit `stepback_prompting.py`:

```python
# Before:
**EXPECTED CONFIDENCE RANGES BY STATE:**
- **Fully Compliant**: Typically 82-96
- **Partially Compliant**: Typically 45-75
- **Non-Compliant**: Typically 5-35

# After (more lenient):
**EXPECTED CONFIDENCE RANGES BY STATE:**
- **Fully Compliant**: Typically 75-95
- **Partially Compliant**: Typically 40-70
- **Non-Compliant**: Typically 10-40
```

Adjust penalties:

```python
# Before:
3. **Are there specific, measurable commitments?**
   - NO (general principles only) → Reduce by 15-25 points

# After (less penalty):
3. **Are there specific, measurable commitments?**
   - NO (general principles only) → Reduce by 10-18 points
```

---

### Scenario 3: Use Different Embedding Model

#### Current Model

```python
# vector_store.py
HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# Embedding Dimension: 384
# Speed: Fast
# Quality: Good
```

#### Upgrade to Higher Quality

```python
# vector_store.py
HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
# Embedding Dimension: 768
# Speed: Slower (2x)
# Quality: Excellent
```

**Trade-offs**:

- ✅ Better semantic understanding
- ✅ More accurate retrieval
- ❌ Slower embedding generation
- ❌ Requires more memory

#### Install Model

```bash
# Model auto-downloads on first use
python -c "from langchain_community.embeddings import HuggingFaceEmbeddings; HuggingFaceEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')"
```

---

### Scenario 4: Adjust Retrieved Section Count

#### Current Setting

```python
# base_client.py
qa_chain = RetrievalQA.from_chain_type(
    retriever=vector_store.as_retriever(search_kwargs={"k": 3})
)
```

#### Increase Context Window

```python
# base_client.py
qa_chain = RetrievalQA.from_chain_type(
    retriever=vector_store.as_retriever(search_kwargs={"k": 7})
)
```

**When to increase `k`**:

- Long contracts (>50 pages)
- Complex multi-part questions
- Compliance checks spanning multiple sections

**When to decrease `k`**:

- Short contracts (<10 pages)
- Specific factual queries
- Faster response time needed

---

## Production Deployment

### Option 1: Deploy to Streamlit Cloud

#### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-org/compliance-analyzer.git
git push -u origin main
```

#### Step 2: Deploy on Streamlit Cloud

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select repository: `your-org/compliance-analyzer`
4. Main file path: `app.py`
5. Click "Deploy"

#### Step 3: Add Secrets

In Streamlit Cloud dashboard:

1. App settings → Secrets
2. Add:

```toml
MISTRAL_API_KEY = "sk-mistral-..."
GOOGLE_API_KEY = "AIza..."
GROQ_API_KEY = "gsk_..."
COMPLIANCE_QUESTIONS_PATH = "src/utils/questions/complianceQuestion.json"
```

---

### Option 2: Deploy to Docker

#### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Step 2: Create docker-compose.yml

```yaml
version: "3.8"
services:
  compliance-analyzer:
    build: .
    ports:
      - "8501:8501"
    env_file:
      - .env
    volumes:
      - ./input_files:/app/input_files
      - ./results:/app/results
```

#### Step 3: Build and Run

```bash
docker-compose up --build
# Visit http://localhost:8501
```

---

### Option 3: Deploy to Cloud VM (AWS/GCP/Azure)

#### Step 1: Provision VM

```bash
# AWS EC2 example
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.medium \
  --key-name your-key \
  --security-group-ids sg-xxxxxxxx
```

#### Step 2: SSH and Install

```bash
ssh -i your-key.pem ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com

# Update system
sudo apt update && sudo apt install -y python3-pip

# Clone repo
git clone https://github.com/your-org/compliance-analyzer.git
cd compliance-analyzer

# Install dependencies
pip3 install -r requirements.txt

# Configure environment
cp .sample.env .env
nano .env  # Add API keys
```

#### Step 3: Run with nohup

```bash
nohup streamlit run app.py --server.port=8501 --server.address=0.0.0.0 &
```

#### Step 4: Access

```
http://your-vm-ip:8501
```

---

## Troubleshooting Scenarios

### Scenario 1: "Module Not Found" Errors

**Symptoms**:

```
ModuleNotFoundError: No module named 'langchain_classic'
```

**Solution**:

```bash
# Verify virtual environment activated
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check specific package
pip show langchain-classic
```

---

### Scenario 2: Streamlit Won't Start

**Symptoms**:

```
Address already in use
```

**Solution**:

```bash
# Find process using port 8501
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
streamlit run app.py --server.port=8502
```

---

### Scenario 3: Chat Returns Empty Responses

**Symptoms**:
Send button clicked, but assistant message is blank.

**Diagnosis**:

```python
# Check qa_chain initialization
python
>>> from src.orchestator.compliance_runner import run_qna
>>> qa_chain = run_qna(structured_json, chat_type=True)
>>> from src.orchestator.chain import qna
>>> result = qna(qa_chain, "Test question")
>>> print(result)
```

**Common Causes**:

1. **Empty retrieval**: No relevant sections found
   - Solution: Check vector store has documents
2. **API timeout**: LLM took too long
   - Solution: Increase timeout in `llama.py`
3. **Parsing error**: LLM returned unexpected format
   - Solution: Check `compliance_prompt.py` output instructions

---

### Scenario 4: All Confidence Scores Are 50

**Symptoms**:
Every result shows exactly 50% confidence.

**Diagnosis**:
LLM isn't following calibration rubric.

**Solution**:

```python
# Edit stepback_prompting.py

# Add emphasis to instructions:
**CRITICAL**: Use granular scores throughout the 0-100 range.
Avoid defaulting to 0, 50, or 100.
YOU MUST NOT USE 50 AS A DEFAULT.
Calculate the score step-by-step using the rubric above.
```

Or increase temperature:

```python
# llama.py
temperature=1.2  # More variability (default: 1.0)
```

---

## Advanced Tips

### Tip 1: Batch Processing Contracts

```python
from pathlib import Path
from src.parser.mistral_ocr_convertor import textExtractor
from src.orchestator.compliance_runner import run_compliance

contracts_dir = Path("input_files/batch")

for pdf in contracts_dir.glob("*.pdf"):
    print(f"Processing {pdf.name}...")
    extractor = textExtractor(pdf_path=str(pdf))
    result = extractor.ocr_response_file()
    compliance = run_compliance(result["structured_json"])

    # Save with contract name
    output_file = f"results/{pdf.stem}_compliance.json"
    with open(output_file, "w") as f:
        json.dump(compliance, f, indent=2)
```

### Tip 2: Export to Excel

```python
import pandas as pd

# Load results
with open("results/complianceResults.json") as f:
    results = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(results)

# Export
df.to_excel("compliance_report.xlsx", index=False)
```

### Tip 3: Add Email Alerts

```python
import smtplib
from email.mime.text import MIMEText

def send_alert(results):
    non_compliant = [r for r in results if r['Compliance State'] == 'Non-Compliant']

    if non_compliant:
        msg = MIMEText(f"Found {len(non_compliant)} non-compliant clauses")
        msg['Subject'] = 'Contract Compliance Alert'
        msg['From'] = 'system@manulife.com'
        msg['To'] = 'legal@manulife.com'

        with smtplib.SMTP('smtp.manulife.com') as server:
            server.send_message(msg)
```

---

**You've completed the walkthrough!** 🎉

For additional support:

- 📧 Email: abhi526691shek@gmail.com
