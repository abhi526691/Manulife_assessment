# 📄 Contract Compliance Analyzer

> **AI-Powered Contract Review System for Automated Compliance Verification**

A sophisticated Retrieval-Augmented Generation (RAG) application that automates the analysis of vendor contracts against predefined compliance requirements. Built with advanced OCR, vector search, and multi-LLM orchestration capabilities.

---

## 🎯 Project Overview

The **Contract Compliance Analyzer** is an enterprise-grade solution designed to streamline contract review processes by automatically extracting, analyzing, and evaluating vendor agreements against security and compliance standards. The system leverages cutting-edge AI technologies to provide detailed compliance assessments with confidence scoring and supporting evidence extraction.

### Key Capabilities

- **Intelligent Document Processing**: Extracts structured data from PDF contracts using Mistral OCR
- **RAG-Powered Analysis**: Retrieves relevant contract sections and generates compliance assessments
- **Multi-LLM Support**: Supports both Llama 3.1 (via Groq) and Gemini Flash with automatic fallback
- **Interactive Chat Interface**: AI assistant for contract Q&A powered by conversational RAG
- **Structured Evaluation**: Step-back reasoning framework for high-quality compliance determinations
- **Real-time Dashboard**: Streamlit-based UI with branded Manulife design system

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                            │
│                    (Streamlit Web App)                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Document   │  │  Compliance  │  │  Interactive │
│   Upload &   │  │   Analysis   │  │     Chat     │
│  Processing  │  │    Engine    │  │   Assistant  │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌──────────────────────────────────────────────────┐
│            Orchestration Layer                    │
│  • Chain Management                               │
│  • Prompt Engineering (Step-back Prompting)       │
│  • Output Parsing & Validation                    │
└────────────────────┬─────────────────────────────┘
                     │
        ┌────────────┼────────────────┐
        │            │                │
        ▼            ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Mistral    │ │   Vector     │ │   LLM        │
│     OCR      │ │   Store      │ │  Providers   │
│   (Parser)   │ │  (FAISS)     │ │ (Llama/      │
│              │ │              │ │  Gemini)     │
└──────────────┘ └──────────────┘ └──────────────┘
```

### Component Breakdown

1. **Parser Layer** (`src/parser/`)
   - Mistral OCR for PDF-to-Markdown conversion
   - Structured JSON generation with section metadata
   - Hierarchical document parsing with keyword tagging

2. **Retrieval Layer** (`src/retriever/`)
   - FAISS vector store for semantic search
   - HuggingFace embeddings (all-MiniLM-L6-v2)
   - Context retrieval with relevance scoring

3. **Generation Layer** (`src/generator/`)
   - Multi-LLM support (Llama 3.1, Gemini Flash)
   - Structured output parsing
   - Step-back prompting for enhanced reasoning

4. **Orchestration Layer** (`src/orchestator/`)
   - Compliance loop execution
   - QA chain management
   - Result aggregation and storage

5. **Presentation Layer** (`app.py`)
   - Streamlit web interface
   - Real-time chat sidebar
   - Results visualization with HTML tables

---

## ✨ Features

### 🔍 **Automated Compliance Analysis**

- Evaluates contracts against 5+ predefined compliance questions
- Generates structured assessments: **Fully Compliant**, **Partially Compliant**, or **Non-Compliant**
- Provides confidence scores (0-100) calibrated to evidence quality
- Extracts verbatim supporting quotes with section references

### 💬 **Interactive AI Assistant**

- Conversational interface for contract Q&A
- Context-aware responses grounded in uploaded documents
- Real-time chat history with user/assistant role separation
- Automatically enabled after compliance analysis completion

### 📊 **Enterprise-Grade Reporting**

- Tabular results display with color-coded compliance states
- Detailed rationale for each assessment
- Source document tracking for audit trails
- Exportable JSON results for downstream integration

### 🎨 **Branded User Experience**

- Manulife corporate design system (green gradient themes)
- Responsive multi-page navigation (Upload → Document → Results)
- Persistent chat sidebar with locked/unlocked states
- Smooth transitions and loading indicators

---

## 🚀 Quick Start

### Prerequisites

- **Python**: 3.9 or higher
- **API Keys**: Mistral, Google (Gemini), Groq
- **Dependencies**: See `requirements.txt`

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-org/contract-compliance-analyzer.git
   cd contract-compliance-analyzer
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   ```bash
   cp .sample.env .env
   ```

   Edit `.env` and add your API keys:

   ```dotenv
   MISTRAL_API_KEY=your_mistral_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   COMPLIANCE_QUESTIONS_PATH=src/utils/questions/complianceQuestion.json
   ```

5. **Run the application**

   ```bash
   streamlit run app.py
   ```

6. **Access the UI**
   - Open your browser to `http://localhost:8501`
   - Upload a PDF contract to begin analysis

---

## 📖 Usage Guide

### Step 1: Upload Contract

1. Navigate to the **Upload** page
2. Click "Choose a PDF file" and select your vendor contract
3. Wait for OCR processing (typically 10-30 seconds)
4. Automatically redirects to the Document view

### Step 2: Review Extracted Content

1. Verify the extracted markdown rendering
2. Compliance analysis runs automatically in the background
3. Monitor the status bar for progress updates
4. Click "View Compliance Results" when ready

### Step 3: Analyze Compliance Results

1. Review the compliance table with 5 evaluation criteria:
   - **Password Management**
   - **IT Asset Management**
   - **Security Training & Background Checks**
   - **Data in Transit Encryption**
   - **Network Authentication & Authorization**

2. Each result includes:
   - **Compliance State**: Fully/Partially/Non-Compliant
   - **Confidence Score**: 0-100 scale
   - **Relevant Quotes**: Extracted contract sections
   - **Rationale**: Detailed justification

### Step 4: Chat with AI Assistant

1. Once analysis completes, the chat sidebar unlocks
2. Type questions in the text area (e.g., "What are the payment terms?")
3. Click **Send** to receive grounded answers
4. Use **Clear** to reset conversation history

---

## 🧪 Example Workflow

```python
# Programmatic usage (alternative to UI)
from src.orchestator.compliance_runner import run_compliance, run_qna, ask_bot
from src.parser.mistral_ocr_convertor import textExtractor

# Step 1: Extract document
extractor = textExtractor(pdf_path="input_files/Sample Contract.pdf")
result = extractor.ocr_response_file()

# Step 2: Run compliance analysis
compliance_results = run_compliance(result["structured_json"])

# Step 3: Initialize chat
qa_chain = run_qna(result["structured_json"], chat_type=True)

# Step 4: Ask questions
answer = ask_bot(qa_chain, "Does the vendor require MFA for admin access?")
print(answer)
```

---

## 🔧 Configuration

### Compliance Questions

Customize evaluation criteria by editing `src/utils/questions/complianceQuestion.json`:

```json
{
  "contract_audit_config": {
    "questions": [
      {
        "id": 1,
        "title": "Your Custom Question",
        "pre_condition": "Required contract clause description",
        "question": "Specific evaluation query",
        "search_keywords": ["keyword1", "keyword2"],
        "category": "Category Name"
      }
    ]
  }
}
```

### LLM Selection

Change the model in `src/orchestator/compliance_runner.py`:

```python
# Use Gemini (Google)
rag.run_RAG_model(model_type="gemini")

# Use Llama (Groq) - default
rag.run_RAG_model(model_type="llama")
```

### Prompt Engineering

Modify reasoning frameworks in `src/generator/prompts/`:

- `stepback_prompting.py`: Compliance analysis prompts
- `compliance_prompt.py`: QA chat prompts

---

## 📁 Project Structure

```
Manulife_assessment/
│
├── app.py                          # Streamlit UI entry point
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (not in git)
├── .sample.env                     # Template for .env
│
├── input_files/                    # Sample contracts for testing
│   └── Sample Contract.pdf
│
├── results/                        # Output compliance reports
│   └── complianceResults.json
│
├── Ontology/                       # Knowledge base schemas
│   ├── complianceOntology.json
│   └── knowledgebase.json
│
├── src/
│   ├── parser/                     # Document extraction
│   │   ├── mistral_ocr_convertor.py   # OCR pipeline
│   │   ├── pdf_parser.py              # Markdown/JSON processing
│   │   ├── Json_files/                # Structured outputs
│   │   └── markdown_files/            # Extracted text
│   │
│   ├── retriever/                  # Vector search
│   │   └── vector_store.py            # FAISS integration
│   │
│   ├── generator/                  # LLM generation
│   │   ├── llm/
│   │   │   ├── base_client.py         # QA chain builder
│   │   │   ├── llama.py               # Groq/Llama client
│   │   │   └── gemini.py              # Google Gemini client
│   │   └── prompts/
│   │       ├── stepback_prompting.py  # Compliance prompts
│   │       └── compliance_prompt.py   # QA prompts
│   │
│   ├── orchestator/                # Business logic
│   │   ├── chain.py                   # RAG chain management
│   │   ├── compliance_runner.py       # Main execution
│   │   └── helper.py                  # Utilities
│   │
│   └── utils/
│       └── questions/
│           └── complianceQuestion.json  # Evaluation criteria
│
└── Notebooks/                      # Jupyter development notebooks
    ├── FinalExtractionPipeline.ipynb
    └── ocr.ipynb
```

---

## 🛠️ Technology Stack

| Component          | Technology                     | Purpose                      |
| ------------------ | ------------------------------ | ---------------------------- |
| **Frontend**       | Streamlit 1.30+                | Web UI framework             |
| **OCR**            | Mistral OCR API                | PDF → Markdown conversion    |
| **Embeddings**     | HuggingFace `all-MiniLM-L6-v2` | Semantic text representation |
| **Vector DB**      | FAISS                          | Similarity search            |
| **LLM (Primary)**  | Llama 3.1 via Groq             | Compliance reasoning         |
| **LLM (Fallback)** | Gemini Flash (Google)          | Alternative generation       |
| **Orchestration**  | LangChain Classic              | RAG pipeline management      |
| **Output Parsing** | Pydantic + LangChain           | Structured data validation   |

---

## 🧩 Key Design Decisions

### 1. **Step-Back Prompting**

Implements a multi-phase reasoning framework:

- **Phase 1**: High-level principle identification
- **Phase 2**: Evidence review
- **Phase 3**: Systematic analysis with confidence calibration

This ensures the LLM considers broader security principles before making granular assessments.

### 2. **Confidence Calibration**

Uses a rubric-based scoring system:

- Explicit language presence: +50 base score
- Mandatory language (shall/must): No penalty
- Measurable commitments: +15-25 points
- Coverage completeness: Up to -35 penalty
- Ambiguities: -10 to -18 penalty

Final scores align with compliance states (Fully: 82-96, Partial: 45-75, Non: 5-35).

### 3. **Multi-LLM Fallback**

Automatically switches from Llama to Gemini if Groq API fails, ensuring 99%+ uptime.

### 4. **Hierarchical Document Parsing**

Extracts document structure using markdown headers (# and ##), enabling precise section referencing in citations.

---

## 🔒 Security & Privacy

- **API Keys**: Stored in `.env` (excluded from version control)
- **Data Handling**: All processing occurs server-side; no client-side storage
- **Compliance**: Designed for enterprise security audit workflows
- **Session Isolation**: Streamlit session state prevents cross-user data leakage

---

## 🐛 Troubleshooting

### Issue: OCR Fails to Process PDF

**Solution**: Ensure `MISTRAL_API_KEY` is valid and PDF is not password-protected.

### Issue: Llama Model Returns Errors

**Solution**: Check Groq API quota. System auto-falls back to Gemini.

### Issue: Chat Not Unlocking After Analysis

**Solution**: Verify `run_qna()` completed successfully. Check browser console for errors.

### Issue: Confidence Scores Always 0 or 100

**Solution**: Review `stepback_prompting.py` calibration rules. Ensure LLM follows instructions.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Manulife Assessment Team**
- Contact: [your-email@manulife.com]

---

## 🙏 Acknowledgments

- **Mistral AI** for advanced OCR capabilities
- **Anthropic** for Claude reasoning frameworks
- **LangChain** for RAG infrastructure
- **Streamlit** for rapid UI development

---

## 📊 Project Status

**Current Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: February 2026

---

## 📚 Additional Resources

- [API Documentation](docs/API.md) _(to be created)_
- [Deployment Guide](docs/DEPLOYMENT.md) _(to be created)_
- [Compliance Question Schema](src/utils/questions/complianceQuestion.json)
- [Prompt Engineering Guide](docs/PROMPTS.md) _(to be created)_

---

**Built with ❤️ for Manulife**
