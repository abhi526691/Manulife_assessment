import streamlit as st
from src.parser.mistral_ocr_convertor import textExtractor
from src.orchestator.compliance_runner import run_compliance
import streamlit.components.v1 as components
import html as html_module

# Manulife Brand Colors
MANULIFE_GREEN = "#00A758"
MANULIFE_DARK_GREEN = "#006341"
MANULIFE_LIGHT_GREEN = "#E8F5E9"
MANULIFE_GRAY = "#58595B"
MANULIFE_LIGHT_GRAY = "#F5F5F5"

st.set_page_config(
    layout="wide",
    page_title="Contract Compliance Analyzer",
    initial_sidebar_state="collapsed"
)

# Global Manulife Styling
st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');
        
        /* Global Styles */
        html, body, [class*="css"] {{
            font-family: 'Source Sans Pro', sans-serif;
        }}
        
        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
        /* Main container - full width */
        .block-container {{
            padding: 2rem 3rem;
            max-width: 100%;
        }}
        
        /* Title styling */
        h1 {{
            color: {MANULIFE_DARK_GREEN};
            font-size: 2.5rem !important;
            font-weight: 700 !important;
            text-align: center;
            margin-bottom: 0.5rem !important;
            font-family: 'Source Sans Pro', sans-serif !important;
        }}
        
        h2 {{
            color: {MANULIFE_DARK_GREEN};
            font-family: 'Source Sans Pro', sans-serif !important;
            font-weight: 600 !important;
            font-size: 2rem !important;
            text-align: center;
            margin-bottom: 2rem !important;
        }}
        
        .subtitle {{
            text-align: center;
            color: {MANULIFE_GRAY};
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: {MANULIFE_GREEN};
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            font-family: 'Source Sans Pro', sans-serif;
            transition: all 0.3s ease;
            width: 100%;
        }}
        
        .stButton > button:hover {{
            background-color: {MANULIFE_DARK_GREEN};
            box-shadow: 0 4px 12px rgba(0, 167, 88, 0.3);
            transform: translateY(-2px);
        }}
        
        /* File uploader */
        [data-testid="stFileUploader"] {{
            background-color: white;
            border: 2px dashed {MANULIFE_GREEN};
            border-radius: 12px;
            padding: 3rem;
        }}
        
        [data-testid="stFileUploader"] section {{
            border: none;
            padding: 0;
        }}
        
        /* Info boxes */
        .stAlert {{
            background-color: {MANULIFE_LIGHT_GREEN};
            border-left: 4px solid {MANULIFE_GREEN};
            color: {MANULIFE_GRAY};
            font-size: 1.1rem;
        }}
        
        /* Button container styling */
        .button-container {{
            background-color: {MANULIFE_LIGHT_GRAY};
            padding: 1rem 0;
            border-radius: 8px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
    </style>
""", unsafe_allow_html=True)

# ------------------------
# Session State
# ------------------------
if "page" not in st.session_state:
    st.session_state.page = "upload"

if "markdown" not in st.session_state:
    st.session_state.markdown = None

if "structured_json" not in st.session_state:
    st.session_state.structured_json = None

if "compliance_results" not in st.session_state:
    st.session_state.compliance_results = None


# ------------------------
# PAGE 1: Upload + OCR
# ------------------------
if st.session_state.page == "upload":
    # Header
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 3rem;'>
            <h1>📄 Contract Compliance Analyzer</h1>
            <p class='subtitle'>Powered by Manulife</p>
        </div>
    """, unsafe_allow_html=True)

    # Center the upload section
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
            <div style='background-color: white; border-radius: 12px; padding: 2rem; 
                 box-shadow: 0 2px 8px rgba(0,0,0,0.1); text-align: center; margin-bottom: 2rem;'>
                <h3 style='color: {MANULIFE_DARK_GREEN}; margin-bottom: 1rem;'>Upload Contract Document</h3>
                <p style='font-size: 1.1rem; color: {MANULIFE_GRAY};'>
                    Upload a PDF contract to analyze compliance requirements
                </p>
            </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            label_visibility="collapsed"
        )

        if uploaded_file:
            st.markdown(f"""
                <div style='text-align: center; padding: 1rem; background-color: {MANULIFE_LIGHT_GREEN}; 
                     border-radius: 8px; margin: 1.5rem 0;'>
                    <p style='color: {MANULIFE_DARK_GREEN}; font-size: 1.1rem; margin: 0;'>
                        ✅ <strong>{uploaded_file.name}</strong> uploaded successfully
                    </p>
                </div>
            """, unsafe_allow_html=True)

            st.info("📥 Processing document with OCR...")
            extractor = textExtractor(pdf_path=uploaded_file)

            with st.spinner("Extracting and analyzing document content..."):
                result = extractor.get_stored_response()
                st.session_state.markdown = result["markdown"]
                st.session_state.structured_json = result["structured_json"]
                st.session_state.page = "document"
                st.rerun()


# ------------------------
# PAGE 2: Document View
# ------------------------
elif st.session_state.page == "document":
    # Header
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 1rem;'>
            <h1>📄 Contract Compliance Analyzer</h1>
            <p class='subtitle'>Powered by Manulife</p>
        </div>
    """, unsafe_allow_html=True)

    # Buttons at the top with background
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([2, 1, 0.5, 1, 2])

    with col2:
        if st.button("⬅️ Back to Upload", key="top_back"):
            st.session_state.page = "upload"
            st.rerun()

    with col4:
        if st.button("▶️ Run Compliance Analysis", type="primary", key="top_run"):
            st.session_state.page = "processing"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <h2>📄 Extracted Document Content</h2>
    """, unsafe_allow_html=True)

    # Document preview with Manulife styling - FULL WIDTH
    st.markdown(f"""
        <style>
        .markdown-container {{
            font-size: 1.05rem;
            line-height: 1.8;
            padding: 2.5rem;
            border: 2px solid {MANULIFE_GREEN};
            border-radius: 12px;
            background-color: white;
            height: 550px;
            overflow-y: auto;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        .markdown-container::-webkit-scrollbar {{
            width: 12px;
        }}
        .markdown-container::-webkit-scrollbar-track {{
            background: {MANULIFE_LIGHT_GRAY};
            border-radius: 10px;
        }}
        .markdown-container::-webkit-scrollbar-thumb {{
            background: {MANULIFE_GREEN};
            border-radius: 10px;
        }}
        .markdown-container::-webkit-scrollbar-thumb:hover {{
            background: {MANULIFE_DARK_GREEN};
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<div class='markdown-container'>{st.session_state.markdown}</div>",
        unsafe_allow_html=True
    )


# ------------------------
# PAGE 3: Processing
# ------------------------
elif st.session_state.page == "processing":
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 3rem;'>
            <h1>📄 Contract Compliance Analyzer</h1>
            <p class='subtitle'>Powered by Manulife</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
            <div style='text-align: center; background-color: white; padding: 3rem; 
                 border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h2 style='color: {MANULIFE_DARK_GREEN};'>🔍 Analyzing Compliance</h2>
                <p style='font-size: 1.2rem; color: {MANULIFE_GRAY};'>
                    Running compliance checks against contract requirements...
                </p>
            </div>
        """, unsafe_allow_html=True)

    with st.spinner("Processing..."):
        st.session_state.compliance_results = run_compliance(
            st.session_state.structured_json
        )
        st.session_state.page = "results"
        st.rerun()


# ------------------------
# PAGE 4: Results
# ------------------------
elif st.session_state.page == "results":
    # Header
    st.markdown(f"""
        <div style='text-align: center; margin-bottom: 1rem;'>
            <h1>📄 Contract Compliance Analyzer</h1>
            <p class='subtitle'>Powered by Manulife</p>
        </div>
    """, unsafe_allow_html=True)

    # Button at the top with background
    st.markdown("<div class='button-container'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("⬅️ Back to Document", key="top_back_result"):
            st.session_state.page = "document"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <h2>✅ Compliance Analysis Results</h2>
    """, unsafe_allow_html=True)

    # Build table rows
    rows_html = ""
    for row in st.session_state.compliance_results:
        # Format quotes
        raw_quotes = row.get('Relevant Quotes', "")
        if isinstance(raw_quotes, str) and raw_quotes:
            parts = [q.strip() for q in raw_quotes.replace(
                ';', ',').split(',') if q.strip()]
            escaped_parts = [html_module.escape(part) for part in parts]
            display_quotes = "<br><br>• ".join(escaped_parts)
            if display_quotes:
                display_quotes = "• " + display_quotes
        else:
            display_quotes = ""

        # Determine state color
        state = row.get('Compliance State', 'N/A')
        if 'Fully Compliant' in state:
            state_color = MANULIFE_GREEN
            state_bg = MANULIFE_LIGHT_GREEN
        elif 'Partially' in state:
            state_color = "#FF8C00"
            state_bg = "#FFF3E0"
        else:
            state_color = "#D32F2F"
            state_bg = "#FFEBEE"

        rows_html += f"""
        <tr>
            <td class="question-col">{html_module.escape(row.get('Compliance Question', 'N/A'))}</td>
            <td style="background-color: {state_bg}; text-align: center;">
                <span style="color: {state_color}; font-weight: 700;">{html_module.escape(state)}</span>
            </td>
            <td class="score-col" style="text-align: center;">{row.get('Confidence', 0)}</td>
            <td class="quotes-col">{display_quotes}</td>
            <td class="rationale-col">{html_module.escape(row.get('Rationale', 'No rationale provided.'))}</td>
        </tr>
        """

    # Complete HTML with Manulife styling - FULL WIDTH TABLE
    complete_html = f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');
        
        body {{
            font-family: 'Source Sans Pro', sans-serif;
            margin: 0;
            padding: 0;
        }}
        .table-wrapper {{
            width: 100%;
            overflow-x: auto;
        }}
        .compliance-results-table {{
            width: 100%;
            border-collapse: collapse;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
            border-radius: 12px;
            overflow: hidden;
        }}
        .compliance-results-table thead {{
            background: linear-gradient(135deg, {MANULIFE_DARK_GREEN} 0%, {MANULIFE_GREEN} 100%);
        }}
        .compliance-results-table th {{
            color: white;
            padding: 20px 18px;
            text-align: left;
            font-weight: 700;
            font-size: 1.1rem;
            letter-spacing: 0.5px;
        }}
        .compliance-results-table td {{
            padding: 20px 18px;
            border-bottom: 1px solid #e0e0e0;
            vertical-align: top;
            font-size: 1.05rem;
            line-height: 1.8;
        }}
        .compliance-results-table tbody tr {{
            background-color: white;
        }}
        .compliance-results-table tbody tr:nth-child(even) {{
            background-color: #fafafa;
        }}
        .compliance-results-table tbody tr:hover {{
            background-color: {MANULIFE_LIGHT_GREEN} !important;
            transition: background-color 0.2s ease;
        }}
        .compliance-results-table tbody tr:last-child td {{
            border-bottom: none;
        }}
        .question-col {{
            font-weight: 700;
            color: {MANULIFE_DARK_GREEN};
            font-size: 1.15rem;
        }}
        .score-col {{
            font-weight: 700;
            font-size: 1.3rem;
            color: {MANULIFE_GREEN};
        }}
        .quotes-col {{
            color: {MANULIFE_GRAY};
            font-size: 1rem;
            line-height: 1.9;
        }}
        .rationale-col {{
            color: {MANULIFE_GRAY};
            line-height: 1.9;
        }}
    </style>
    <div class="table-wrapper">
        <table class="compliance-results-table">
            <thead>
                <tr>
                    <th style="width: 15%;">Compliance Question</th>
                    <th style="width: 12%; text-align: center;">State</th>
                    <th style="width: 8%; text-align: center;">Score</th>
                    <th style="width: 25%;">Relevant Quotes</th>
                    <th style="width: 40%;">Rationale</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </div>
    """

    # Render with appropriate height
    components.html(complete_html, height=700, scrolling=True)
