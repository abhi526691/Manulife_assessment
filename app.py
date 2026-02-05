import streamlit as st
from src.parser.mistral_ocr_convertor import textExtractor
from src.orchestator.compliance_runner import run_compliance, run_qna, ask_bot
import streamlit.components.v1 as components
import html as html_module
import time
import re


# --------------------------------------------------
# Manulife Brand Colors
# --------------------------------------------------
MANULIFE_GREEN = "#00A758"
MANULIFE_DARK_GREEN = "#006341"
MANULIFE_LIGHT_GREEN = "#E8F5E9"
MANULIFE_GRAY = "#58595B"
MANULIFE_LIGHT_GRAY = "#F5F5F5"

st.set_page_config(
    layout="wide",
    page_title="Contract Compliance Analyzer",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Enhanced Global Styling with JavaScript to hide collapse button
# --------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@400;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Source Sans Pro', sans-serif;
}}

#MainMenu, footer, header {{ visibility: hidden; }}

.block-container {{
    padding: 1.2rem 2.5rem;
    max-width: 100%;
}}

h1 {{
    margin-bottom: 0.3rem !important;
}}

.subtitle {{
    margin-bottom: 1.2rem;
    color: {MANULIFE_GRAY};
}}

/* Enhanced Chat Sidebar Styling */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #ffffff 0%, {MANULIFE_LIGHT_GRAY} 100%);
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top: 2rem;
}}

/* Keep sidebar always expanded - more aggressive rules */
section[data-testid="stSidebar"] {{
    position: relative !important;
    min-width: 21rem !important;
    max-width: 21rem !important;
    transform: none !important;
    margin-left: 0 !important;
}}

section[data-testid="stSidebar"] > div {{
    min-width: 21rem !important;
    max-width: 21rem !important;
}}

section[data-testid="stSidebar"][aria-expanded="false"] {{
    min-width: 21rem !important;
    max-width: 21rem !important;
    margin-left: 0 !important;
    transform: translateX(0) !important;
}}

section[data-testid="stSidebar"][aria-expanded="true"] {{
    min-width: 21rem !important;
    max-width: 21rem !important;
}}

/* Hide ALL collapse-related buttons - multiple selectors for redundancy */
button[kind="header"] {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}}

button[data-testid="baseButton-header"] {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}}

button[kind="header"][data-testid="baseButton-header"] {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}}

[data-testid="collapsedControl"] {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}}

/* Hide any button in the sidebar header area */
[data-testid="stSidebar"] button[kind="header"] {{
    display: none !important;
    visibility: hidden !important;
}}

/* Remove the space where the button would be */
[data-testid="stSidebar"] > div > div:first-child {{
    padding-left: 1rem !important;
}}

.chat-header {{
    background: linear-gradient(135deg, {MANULIFE_DARK_GREEN}, {MANULIFE_GREEN});
    color: white;
    padding: 1.5rem;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}}

.chat-header h2 {{
    margin: 0;
    font-size: 1.5rem;
    font-weight: 700;
}}

.chat-header p {{
    margin: 0.5rem 0 0 0;
    font-size: 0.9rem;
    opacity: 0.9;
}}

.chat-message {{
    padding: 1rem 1.2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
    animation: fadeIn 0.3s ease-in;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}}

@keyframes fadeIn {{
    from {{
        opacity: 0;
        transform: translateY(10px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.chat-message.user {{
    background: linear-gradient(135deg, {MANULIFE_LIGHT_GREEN}, #d4f1e3);
    border-left: 4px solid {MANULIFE_GREEN};
    margin-left: 1rem;
}}

.chat-message.assistant {{
    background: linear-gradient(135deg, {MANULIFE_LIGHT_GRAY}, #e8e8e8);
    border-left: 4px solid {MANULIFE_DARK_GREEN};
    margin-right: 1rem;
}}

.chat-message .role {{
    font-weight: 700;
    margin-bottom: 0.6rem;
    color: {MANULIFE_DARK_GREEN};
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.chat-message .content {{
    color: {MANULIFE_GRAY};
    line-height: 1.6;
    font-size: 0.95rem;
    word-wrap: break-word;
    white-space: pre-wrap;
}}

.chat-disabled {{
    background: #fff3cd;
    border: 2px dashed #ffc107;
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
    color: #856404;
}}

.chat-disabled svg {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}

.chat-disabled h3 {{
    margin: 1rem 0 0.5rem 0;
    color: #856404;
}}

.chat-disabled p {{
    margin: 0;
    font-size: 0.9rem;
}}

/* Empty state styling */
.chat-empty {{
    text-align: center;
    padding: 2rem;
    color: {MANULIFE_GRAY};
    opacity: 0.6;
}}

.chat-empty svg {{
    font-size: 3rem;
    margin-bottom: 1rem;
}}
</style>

<script>
// JavaScript to forcefully remove collapse button on load and monitor for changes
(function() {{
    function hideCollapseButton() {{
        const buttons = window.parent.document.querySelectorAll(
            'button[kind="header"], button[data-testid="baseButton-header"], [data-testid="collapsedControl"]'
        );
        buttons.forEach(btn => {{
            btn.style.display = 'none';
            btn.style.visibility = 'hidden';
            btn.style.opacity = '0';
            btn.style.pointerEvents = 'none';
        }});
    }}

    // Run immediately
    hideCollapseButton();

    // Run after page load
    window.addEventListener('load', hideCollapseButton);

    // Monitor for DOM changes and hide button if it appears
    const observer = new MutationObserver(hideCollapseButton);
    observer.observe(window.parent.document.body, {{
        childList: true,
        subtree: true
    }});

    // Run repeatedly for the first few seconds to catch dynamic loading
    setTimeout(hideCollapseButton, 100);
    setTimeout(hideCollapseButton, 500);
    setTimeout(hideCollapseButton, 1000);
    setTimeout(hideCollapseButton, 2000);
}})();
</script>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Session State
# --------------------------------------------------
st.session_state.setdefault("page", "upload")
st.session_state.setdefault("markdown", None)
st.session_state.setdefault("structured_json", None)
st.session_state.setdefault("compliance_results", None)
st.session_state.setdefault("has_results", False)
st.session_state.setdefault("auto_run", False)
st.session_state.setdefault("qa_chain", None)
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("chat_enabled", False)

# ==================================================
# CHAT SIDEBAR COMPONENT
# ==================================================


def render_chat_sidebar():
    """Renders the chat interface in the sidebar"""
    with st.sidebar:
        # Chat Header
        if st.session_state.chat_enabled:
            st.markdown(f"""
                <div class="chat-header">
                    <h2>💬 AI Assistant</h2>
                    <p>Ask questions about your contract</p>
                </div>
            """, unsafe_allow_html=True)

        # Chat not enabled state
        if not st.session_state.chat_enabled:
            st.markdown("""
                <div class="chat-disabled">
                    <div style="font-size: 3rem;">🔒</div>
                    <h3>Chat Locked</h3>
                    <p>Complete the compliance analysis to unlock the AI assistant</p>
                </div>
            """, unsafe_allow_html=True)
            return

        # Chat messages display
        if len(st.session_state.chat_history) == 0:
            st.markdown("""
                <div class="chat-empty">
                    <div style="font-size: 2.5rem;">💭</div>
                    <p>No messages yet. Start a conversation!</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Create a container for scrollable messages
            st.markdown(
                '<div style="max-height: 50vh; overflow-y: auto;">', unsafe_allow_html=True)

            # Display each message
            for idx, message in enumerate(st.session_state.chat_history):
                role_label = "You" if message["role"] == "user" else "AI Assistant"
                role_icon = "👤" if message["role"] == "user" else "🤖"

                st.markdown(f"""
                    <div class="chat-message {message['role']}">
                        <div class="role">{role_icon} {role_label}</div>
                        <div class="content">{html_module.escape(message['content'])}</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        # Spacer
        st.markdown("<br>", unsafe_allow_html=True)

        # Chat input section
        st.markdown("💬 **Your question:**")

        user_question = st.text_area(
            "Type your question here",
            key=f"user_input_{st.session_state.page}",
            placeholder="e.g., What are the payment terms in this contract?",
            height=100,
            label_visibility="collapsed"
        )

        col1, col2 = st.columns([3, 2])

        with col1:
            send_button = st.button(
                "📤 Send", use_container_width=True, type="primary")
        with col2:
            clear_button = st.button("🗑️ Clear", use_container_width=True)

        # Handle clear button
        if clear_button:
            st.session_state.chat_history = []
            st.rerun()

        # Handle send button
        if send_button and user_question.strip():
            # Add user message to history
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question
            })

            # Get response from bot
            with st.spinner("🤔 Thinking..."):
                try:
                    answer = ask_bot(st.session_state.qa_chain, user_question)
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })
                except Exception as e:
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"⚠️ I encountered an error while processing your question: {str(e)}"
                    })

            st.rerun()


# ==================================================
# PAGE 1 — Upload + OCR
# ==================================================
if st.session_state.page == "upload":

    st.markdown("""
        <div style="text-align:center;">
            <h1>📄 Contract Compliance Analyzer</h1>
            <p class="subtitle">Powered by Manulife</p>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        st.info("📥 Processing document with OCR...")
        extractor = textExtractor(pdf_path=uploaded_file)

        with st.spinner("Extracting document content..."):
            result = extractor.ocr_response_file()

        st.session_state.markdown = result["markdown"]
        st.session_state.structured_json = result["structured_json"]

        # Reset for new document
        st.session_state.has_results = False
        st.session_state.auto_run = True
        st.session_state.qa_chain = None
        st.session_state.chat_history = []
        st.session_state.chat_enabled = False

        st.session_state.page = "document"
        st.rerun()

# ==================================================
# PAGE 2 — Document View
# ==================================================
elif st.session_state.page == "document":

    # Render chat sidebar
    render_chat_sidebar()

    # ---------------- Main Content ----------------
    st.markdown("""
        <div style="text-align:center;">
            <h1>📄 Contract Compliance Analyzer</h1>
            <p class="subtitle">Extracted Document</p>
        </div>
    """, unsafe_allow_html=True)

    # ---------------- TOP STATUS BAR ----------------
    status_bar = st.empty()

    # ---------------- Top Navigation ----------------
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("⬅️ Back to Upload"):
            st.session_state.page = "upload"
            st.rerun()

    with col3:
        if st.session_state.get("has_results", False):
            if st.button("📊 View Compliance Results"):
                st.session_state.page = "results"
                st.rerun()

    # ---------------- Document Display ----------------

    def convert_markdown_to_html_complete(markdown_text):
        """Convert markdown to HTML with proper handling of all elements"""
        html = markdown_text

        # 1. Convert images first (before other conversions)
        def replace_images(match):
            alt_text = match.group(1)
            data_uri = match.group(2)
            return f'<img src="{data_uri}" alt="{alt_text}" style="max-width: 100%; height: auto; border-radius: 8px; margin: 1.5rem 0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); display: block;">'

        html = re.sub(r'!\[([^\]]*)\]\((data:image/[^)]+)\)',
                      replace_images, html)

        # 2. Convert tables
        def convert_table(table_match):
            table_text = table_match.group(0)
            lines = [line.strip()
                     for line in table_text.strip().split('\n') if line.strip()]

            if len(lines) < 2:
                return table_text

            # Parse header
            headers = [cell.strip()
                       for cell in lines[0].split('|') if cell.strip()]

            # Skip separator line
            data_lines = lines[2:] if len(lines) > 2 else []

            # Build HTML table
            table_html = '<table>'
            table_html += '<thead><tr>'
            for header in headers:
                table_html += f'<th>{header}</th>'
            table_html += '</tr></thead><tbody>'

            for line in data_lines:
                cells = [cell.strip()
                         for cell in line.split('|') if cell.strip()]
                if cells:
                    table_html += '<tr>'
                    for cell in cells:
                        table_html += f'<td>{cell}</td>'
                    table_html += '</tr>'

            table_html += '</tbody></table>'
            return table_html

        # Match markdown tables
        table_pattern = r'(?:^\|.+\|\s*$\n)+(?:^\|[\s\-:]+\|\s*$\n)?(?:^\|.+\|\s*$\n?)+'
        html = re.sub(table_pattern, convert_table, html, flags=re.MULTILINE)

        # 3. Convert headers (with proper spacing)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

        # 4. Convert checkboxes
        html = re.sub(
            r'\[ \]', '<input type="checkbox" disabled style="margin-right: 8px;">', html)
        html = re.sub(
            r'\[x\]', '<input type="checkbox" checked disabled style="margin-right: 8px;">', html, flags=re.IGNORECASE)

        # 5. Convert unordered lists (bullets)
        def convert_ul(match):
            items = match.group(0).strip().split('\n')
            list_html = '<ul>'
            for item in items:
                # Remove the bullet marker and convert
                item_text = re.sub(r'^[\s]*[-*+]\s+', '', item)
                if item_text:
                    list_html += f'<li>{item_text}</li>'
            list_html += '</ul>'
            return list_html

        # Match consecutive bullet point lines
        ul_pattern = r'(?:^[\s]*[-*+]\s+.+$\n?)+'
        html = re.sub(ul_pattern, convert_ul, html, flags=re.MULTILINE)

        # 6. Convert ordered lists (numbers)
        def convert_ol(match):
            items = match.group(0).strip().split('\n')
            list_html = '<ol>'
            for item in items:
                # Remove the number marker and convert
                item_text = re.sub(r'^[\s]*\d+\.\s+', '', item)
                if item_text:
                    list_html += f'<li>{item_text}</li>'
            list_html += '</ol>'
            return list_html

        # Match consecutive numbered lines
        ol_pattern = r'(?:^[\s]*\d+\.\s+.+$\n?)+'
        html = re.sub(ol_pattern, convert_ol, html, flags=re.MULTILINE)

        # 7. Convert bold and italic
        html = re.sub(r'\*\*\*(.+?)\*\*\*',
                      r'<strong><em>\1</em></strong>', html)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        html = re.sub(r'___(.+?)___', r'<strong><em>\1</em></strong>', html)
        html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
        html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)

        # 8. Convert inline code
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

        # 9. Convert code blocks
        html = re.sub(r'```[\w]*\n(.*?)```',
                      r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)

        # 10. Convert links
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                      r'<a href="\2" target="_blank">\1</a>', html)

        # 11. Convert horizontal rules
        html = re.sub(r'^[\s]*---[\s]*$', '<hr>', html, flags=re.MULTILINE)
        html = re.sub(r'^[\s]*\*\*\*[\s]*$', '<hr>', html, flags=re.MULTILINE)

        # 12. Convert line breaks and paragraphs
        # Split by double newlines to identify paragraphs
        blocks = re.split(r'\n\n+', html)
        processed_blocks = []

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            # Check if block is already an HTML element
            if block.startswith('<') and '>' in block:
                processed_blocks.append(block)
            else:
                # Regular text - wrap in paragraph and convert single newlines to <br>
                block = block.replace('\n', '<br>')
                processed_blocks.append(f'<p>{block}</p>')

        html = '\n'.join(processed_blocks)

        return html

    st.markdown(f"""
    <style>
    .markdown-container {{
        font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        font-size: 15px;
        line-height: 1.7;
        padding: 2rem;
        border: 2px solid {MANULIFE_GREEN};
        border-radius: 12px;
        background-color: white;
        height: 68vh;
        overflow-y: auto;
        margin-top: 0.8rem;
        color: #333;
    }}

    .markdown-container h1 {{
        color: {MANULIFE_DARK_GREEN};
        font-size: 2em;
        font-weight: 700;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid {MANULIFE_LIGHT_GREEN};
    }}

    .markdown-container h2 {{
        color: {MANULIFE_GREEN};
        font-size: 1.6em;
        font-weight: 600;
        margin: 1.8rem 0 0.8rem 0;
    }}

    .markdown-container h3 {{
        color: {MANULIFE_GRAY};
        font-size: 1.3em;
        font-weight: 600;
        margin: 1.5rem 0 0.7rem 0;
    }}

    .markdown-container h4 {{
        color: {MANULIFE_GRAY};
        font-size: 1.1em;
        font-weight: 600;
        margin: 1.2rem 0 0.6rem 0;
    }}

    .markdown-container p {{
        margin: 0.8rem 0;
        line-height: 1.7;
    }}

    .markdown-container ul {{
        margin: 1rem 0;
        padding-left: 2rem;
        list-style-type: disc;
    }}

    .markdown-container ol {{
        margin: 1rem 0;
        padding-left: 2rem;
        list-style-type: decimal;
    }}

    .markdown-container li {{
        margin: 0.5rem 0;
        line-height: 1.6;
    }}

    .markdown-container ul ul {{
        list-style-type: circle;
        margin-top: 0.3rem;
    }}

    .markdown-container ol ol {{
        list-style-type: lower-alpha;
        margin-top: 0.3rem;
    }}

    .markdown-container table {{
        border-collapse: collapse;
        width: 100%;
        margin: 1.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        font-size: 14px;
    }}

    .markdown-container thead {{
        background: linear-gradient(135deg, {MANULIFE_DARK_GREEN}, {MANULIFE_GREEN});
    }}

    .markdown-container th {{
        color: white;
        font-weight: 600;
        padding: 12px 14px;
        text-align: left;
        border: 1px solid {MANULIFE_GREEN};
    }}

    .markdown-container td {{
        padding: 10px 14px;
        border: 1px solid #ddd;
        text-align: left;
        vertical-align: top;
    }}

    .markdown-container tbody tr:nth-child(even) {{
        background-color: #f9f9f9;
    }}

    .markdown-container tbody tr:hover {{
        background-color: {MANULIFE_LIGHT_GREEN};
        transition: background-color 0.2s ease;
    }}

    .markdown-container img {{
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        margin: 1.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        display: block;
    }}

    .markdown-container code {{
        background-color: #f5f5f5;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: 'Courier New', 'Monaco', monospace;
        font-size: 0.9em;
        color: #d63384;
    }}

    .markdown-container pre {{
        background-color: #f5f5f5;
        padding: 1rem;
        border-radius: 6px;
        overflow-x: auto;
        margin: 1rem 0;
        border-left: 4px solid {MANULIFE_GREEN};
    }}

    .markdown-container pre code {{
        background: none;
        padding: 0;
        color: #333;
        font-size: 0.9em;
    }}

    .markdown-container a {{
        color: {MANULIFE_GREEN};
        text-decoration: none;
        border-bottom: 1px solid transparent;
        transition: border-bottom 0.2s ease;
    }}

    .markdown-container a:hover {{
        border-bottom: 1px solid {MANULIFE_GREEN};
    }}

    .markdown-container hr {{
        border: none;
        border-top: 2px solid {MANULIFE_LIGHT_GREEN};
        margin: 2rem 0;
    }}

    .markdown-container strong {{
        font-weight: 600;
        color: {MANULIFE_DARK_GREEN};
    }}

    .markdown-container em {{
        font-style: italic;
    }}

    .markdown-container input[type="checkbox"] {{
        margin-right: 8px;
        cursor: default;
    }}

    .markdown-container blockquote {{
        border-left: 4px solid {MANULIFE_GREEN};
        padding-left: 1rem;
        margin: 1rem 0;
        color: {MANULIFE_GRAY};
        font-style: italic;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Convert markdown to HTML
    html_content = convert_markdown_to_html_complete(st.session_state.markdown)

    # Display using the container
    st.markdown(
        f"<div class='markdown-container'>{html_content}</div>",
        unsafe_allow_html=True
    )

    # ---------------- Compliance Execution ----------------
    if not st.session_state.get("has_results", False):

        status_bar.info("🔍 Compliance analysis running…")

        st.session_state.compliance_status = "running"

        with st.spinner("Analyzing contract clauses..."):
            st.session_state.compliance_results = run_compliance(
                st.session_state.structured_json
            )
            time.sleep(1.5)

        st.session_state.has_results = True
        st.session_state.compliance_status = "done"

        status_bar.success("✅ Compliance analysis completed")

        # brief UX pause
        time.sleep(0.6)

        st.session_state.page = "results"
        st.rerun()

# ==================================================
# PAGE 3 — Results
# ==================================================
elif st.session_state.page == "results":

    # Initialize QA chain and enable chat if not already done
    if not st.session_state.chat_enabled and st.session_state.has_results:
        with st.spinner("🤖 Initializing AI Assistant..."):
            try:
                st.session_state.qa_chain = run_qna(
                    st.session_state.structured_json,
                    chat_type=True
                )
                st.session_state.chat_enabled = True
                time.sleep(0.5)
            except Exception as e:
                st.error(f"Failed to initialize chat: {str(e)}")

    # Render chat sidebar
    render_chat_sidebar()

    # ---------------- Main Content ----------------
    st.markdown("""
        <div style="text-align:center;">
            <h1>✅ Compliance Analysis Results</h1>
            <p class="subtitle">Automated contract review</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("⬅️ Back to Document"):
            st.session_state.page = "document"
            st.rerun()

    # Show chat enabled notification
    if st.session_state.chat_enabled:
        st.success("💬 AI Assistant is now available in the sidebar!")

    rows_html = ""
    for row in st.session_state.compliance_results:

        state = row.get("Compliance State", "N/A")
        if "Fully" in state:
            state_color = MANULIFE_GREEN
            state_bg = MANULIFE_LIGHT_GREEN
        elif "Partially" in state:
            state_color = "#FF8C00"
            state_bg = "#FFF3E0"
        else:
            state_color = "#D32F2F"
            state_bg = "#FFEBEE"

        rows_html += f"""
        <tr>
            <td>{html_module.escape(row.get("Compliance Question", ""))}</td>
            <td style="background:{state_bg}; color:{state_color}; font-weight:700;">
                {html_module.escape(state)}
            </td>
            <td style="text-align:center;">{row.get("Confidence", 0)}</td>
            <td>{html_module.escape(row.get("Relevant Quotes", ""))}</td>
            <td>{html_module.escape(row.get("Rationale", ""))}</td>
        </tr>
        """

    html = f"""
    <style>
    table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
    }}
    th {{
        background: linear-gradient(135deg, {MANULIFE_DARK_GREEN}, {MANULIFE_GREEN});
        color: white;
        padding: 16px;
        text-align: left;
    }}
    td {{
        padding: 16px;
        border-bottom: 1px solid #e0e0e0;
        vertical-align: top;
    }}
    tr:hover {{
        background: {MANULIFE_LIGHT_GREEN};
    }}
    </style>

    <table>
        <thead>
            <tr>
                <th>Compliance Question</th>
                <th>State</th>
                <th>Score</th>
                <th>Relevant Quotes</th>
                <th>Rationale</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """

    components.html(html, height=750, scrolling=True)
