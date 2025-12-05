import streamlit as st
import streamlit.components.v1 as components  # Add this line
from openai import OpenAI
import os
import requests  # Add this line
from dotenv import load_dotenv
from repo_fetcher import fetch_repository_docs
from ai_summarizer import summarize_markdown_files
from html_builder import generate_onboarding_html, save_html_file

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="Onboarding PDF Generator", layout="wide")

st.title("Onboarding Knowledge Pack Generator")

# ---------------- STATE INIT ----------------
if "markdown_files" not in st.session_state:
    st.session_state["markdown_files"] = None
if "image_files" not in st.session_state:  # Add this
    st.session_state["image_files"] = None

if "repo_meta" not in st.session_state:
    st.session_state["repo_meta"] = None

if "summaries" not in st.session_state:
    st.session_state["summaries"] = None

if "fetch_error" not in st.session_state:
    st.session_state["fetch_error"] = None

if "summary_error" not in st.session_state:
    st.session_state["summary_error"] = None

if "trigger_fetch" not in st.session_state:
    st.session_state["trigger_fetch"] = False

if "html_content" not in st.session_state:
    st.session_state["html_content"] = None

if "html_error" not in st.session_state:
    st.session_state["html_error"] = None

if "pdf_content" not in st.session_state:
    st.session_state["pdf_content"] = None


# ---------------- CALLBACKS ----------------

def do_fetch():
    """Fetch repository documentation and images"""
    if not st.session_state.get("repo_input"):
        st.error("Please enter a repository URL")
        return
        
    try:
        with st.spinner("Fetching repository documentation and images..."):
            result = fetch_repository_docs(st.session_state["repo_input"])
            
        st.session_state["markdown_files"] = result["markdown_files"]
        st.session_state["image_files"] = result["image_files"]
        
        # Create repo_meta from the result structure
        st.session_state["repo_meta"] = {
            "repo": result["repo"],
            "owner": result["owner"],
            "branch": result["branch"],
            "image_files": result["image_files"]  # Add this line
        }
        
        st.session_state["fetch_error"] = None
        
        # Show success message with counts
        num_files = len(result["markdown_files"])
        num_images = len(result["image_files"])
        st.success(f"✅ Found {num_files} markdown files and {num_images} images")
        
    except Exception as e:
        st.session_state["fetch_error"] = str(e)
        st.session_state["markdown_files"] = None
        st.session_state["image_files"] = None
        st.session_state["repo_meta"] = None


def do_summarize():
    """Summarize markdown files with AI"""
    if not st.session_state["markdown_files"]:
        st.error("❌ No markdown files to summarize. Please fetch documentation first.")
        return
        
    try:
        st.session_state["summary_error"] = None
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))       
        with st.spinner("🤖 Generating AI summaries..."):
            summaries = summarize_markdown_files(
                client, 
                st.session_state["markdown_files"],
                st.session_state.get("image_files")  # Pass image files to summarizer
            )
            
        st.session_state["summaries"] = summaries
        st.success(f"✅ Generated summaries for {len(summaries)} files")
        
    except Exception as e:
        st.session_state["summaries"] = None
        st.session_state["summary_error"] = str(e)


def do_generate_html():
    """Generate HTML and then convert to PDF using .NET API"""
    try:
        if not st.session_state["summaries"]:
            st.error("❌ No summaries available. Please summarize first.")
            return
        
        # Generate HTML content using html_builder
        repo_name = st.session_state["repo_meta"]["repo"]
        author = st.session_state.get("author_input", "Riddhi Shah")
        company = st.session_state.get("company_input", "Women in AI")
        
        html_content = generate_onboarding_html(
            summaries=st.session_state["summaries"],
            repo_meta=st.session_state["repo_meta"],
            author=author,
            company=company,
            markdown_files=st.session_state.get("markdown_files"),
            image_files=st.session_state.get("image_files")
        )
        
        st.session_state["html_content"] = html_content
        
        # Send HTML to .NET API for PDF conversion
        payload = {
            "Html": html_content,
            "FileName": f"{repo_name}_onboarding.pdf"
        }
        
        with st.spinner("Generating PDF with IronPDF..."):
            response = requests.post(
                "http://localhost:5165/api/pdf/generate",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=120
            )
        
        if response.status_code == 200:
            # Store the binary PDF content
            st.session_state["pdf_content"] = response.content
            st.success("✅ PDF generated successfully using IronPDF!")
            st.info(f"PDF size: {len(response.content):,} bytes")
        else:
            st.error(f"❌ PDF generation failed (Status: {response.status_code})")
            st.error(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        st.error("❌ PDF generation timed out. The document may be too large.")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to .NET PDF API. Make sure it's running on localhost:5165")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# ---------------- INPUT ----------------

repo_url = st.text_input(
    "GitHub Repository URL",
    key="repo_input",
    placeholder="https://github.com/user/repo"
)

# Additional inputs for HTML generation
col1, col2 = st.columns(2)
with col1:
    author = st.text_input(
        "Author Name",
        key="author_input", 
        value="Riddhi Shah",
        placeholder="Your name"
    )

with col2:
    company = st.text_input(
        "Company Name", 
        key="company_input",
        value="Bazel Inc.",
        placeholder="Company or organization"
    )

# Check if API key is loaded
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OpenAI API key not found. Please add OPENAI_API_KEY to your .env file")
else:
    st.success("✅ OpenAI API key loaded successfully")

# ---------------- BUTTONS ----------------

st.button("Fetch Documentation", on_click=do_fetch)

st.button(
    "Summarize with AI",
    on_click=do_summarize,
    disabled=st.session_state["markdown_files"] is None
)

st.button(
    "Generate HTML Document",
    on_click=do_generate_html,
    disabled=st.session_state["summaries"] is None
)

# Download button for HTML
if st.session_state["html_content"]:
    st.download_button(
        label="📄 Download HTML Document",
        data=st.session_state["html_content"],
        file_name=f"{st.session_state['repo_meta']['repo']}_onboarding.html",
        mime="text/html"
    )
# PDF Download button
if st.session_state.get("pdf_content"):
    st.download_button(
        label="📄 Download PDF Document",
        data=st.session_state["pdf_content"],
        file_name=f"{st.session_state['repo_meta']['repo']}_onboarding.pdf",
        mime="application/pdf"
    )

# Main documentation expander
with st.expander("📄 Fetched Documentation", expanded=False):
    if st.session_state["fetch_error"]:
        st.error(st.session_state["fetch_error"])
    elif st.session_state["markdown_files"]:
        num_files = len(st.session_state["markdown_files"])
        num_images = len(st.session_state.get("image_files", []))  # Fixed this line
        
        st.info(f"📊 Found {num_files} markdown files and {num_images} images")
        
        # Show images if any
        if num_images > 0:
            st.subheader("🖼️ Images Found")
            for img_path in st.session_state["image_files"]:
                st.text(img_path)
        
        # Show markdown content
        st.subheader("📝 Markdown Files")
        for path, content in st.session_state["markdown_files"].items():
            st.write(f"**{path}**")
            with st.container():
                st.code(content, language="markdown")

# Separate expander for AI Summary
with st.expander("🤖 AI Summary Preview", expanded=False):
    if st.session_state["summary_error"]:
        st.error(st.session_state["summary_error"])
    elif st.session_state["summaries"]:
        for path, summary in st.session_state["summaries"].items():
            st.write(f"**📋 {path}**")
            st.markdown(summary)
            st.divider()  # Add a visual separator

with st.expander("📄 HTML Document Preview", expanded=False):
    if st.session_state["html_error"]:
        st.error(st.session_state["html_error"])
    elif st.session_state["html_content"]:
        st.success("✅ HTML document generated successfully!")
        
        # Show HTML preview in an iframe
        components.html(
            st.session_state["html_content"],
            height=600,
            scrolling=True
        )

