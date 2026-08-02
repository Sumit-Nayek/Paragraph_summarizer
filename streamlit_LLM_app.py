import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
from docx import Document

# Load local environment variables from .env
load_dotenv()

# --- 1. RESOLVE API KEY ---
nvidia_api_key = st.secrets.get("NVIDIA_API_KEY") or os.getenv("NVIDIA_API_KEY")

# --- 2. STREAMLIT UI CONFIGURATION ---
st.set_page_config(
    page_title="AI Paragraph Summarizer (NVIDIA NIM)",
    page_icon="⚡",
    layout="centered"
)

st.title("⚡ AI Paragraph Summarizer")
st.caption("Powered by NVIDIA NIM API & Llama Models")

# --- 3. HELPER FUNCTIONS FOR FILE PARSING ---
def extract_text_from_pdf(file) -> str:
    """Extracts text from an uploaded PDF file using pypdf."""
    reader = PdfReader(file)
    extracted_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text.append(text)
    return "\n".join(extracted_text)

def extract_text_from_docx(file) -> str:
    """Extracts text from an uploaded Word (.docx) file using python-docx."""
    doc = Document(file)
    extracted_text = [paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()]
    return "\n".join(extracted_text)

def extract_text_from_txt(file) -> str:
    """Extracts text from an uploaded plain text (.txt) file."""
    return file.read().decode("utf-8")


# --- 4. SIDEBAR CONTROLS ---
st.sidebar.header("🚀 Speed & Model Settings")

# Model Mode Selector (Fast vs. Deep)
model_mode = st.sidebar.radio(
    "Select Inference Mode:",
    ["⚡ Fast Mode (Llama 3.1 8B)", "🧠 Deep Mode (Llama 3.3 70B)"],
    help="Fast Mode gives sub-second responses; Deep Mode provides higher reasoning and detail."
)

if "Fast Mode" in model_mode:
    selected_model = "meta/llama-3.1-8b-instruct"
else:
    selected_model = "meta/llama-3.3-70b-instruct"

# Generation Hyperparameters
st.sidebar.markdown("---")
st.sidebar.header("🎛️ Hyperparameters")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.2, 0.1)
max_tokens = st.sidebar.slider("Max Summary Tokens", 50, 1000, 250, 50)

# Check for API Key presence
if not nvidia_api_key:
    st.error("⚠️ NVIDIA API Key not found. Please set `NVIDIA_API_KEY` in Streamlit Secrets or your `.env` file.")
    st.stop()

# --- 5. INITIALIZE OPENAI CLIENT POINTING TO NVIDIA NIM ---
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=nvidia_api_key
)

# --- 6. STREAMING GENERATOR FUNCTION ---
def generate_summary_stream(text: str, model: str, temp: float, tokens: int):
    """Generator function that streams tokens from NVIDIA NIM API in real time."""
    response_stream = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert paragraph summarizer. "
                    "Summarize the provided text into a concise, well-structured "
                    "paragraph capturing all key points."
                )
            },
            {
                "role": "user",
                "content": f"Please summarize the following text:\n\n{text}"
            }
        ],
        temperature=temp,
        max_tokens=tokens,
        stream=True
    )

    for chunk in response_stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# --- 7. MAIN INPUT (FILE UPLOAD OR MANUAL TEXT) ---
st.subheader("1. Input Document or Text")

# File Uploader
uploaded_file = st.file_uploader(
    "Upload a document (.pdf, .docx, .txt):",
    type=["pdf", "docx", "txt"]
)

extracted_text = ""

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            extracted_text = extract_text_from_docx(uploaded_file)
        elif uploaded_file.name.endswith(".txt"):
            extracted_text = extract_text_from_txt(uploaded_file)
            
        st.success(f"Successfully loaded '{uploaded_file.name}'!")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Text area pre-filled with uploaded file text or manual input
input_text = st.text_area(
    "Or edit/paste your text below:",
    value=extracted_text,
    height=220,
    placeholder="Enter long text or upload a file above..."
)

# --- 8. GENERATION LOGIC ---
st.subheader("2. Summary Output")

if st.button("Generate Real-Time Summary", type="primary"):
    if not input_text.strip():
        st.warning("Please upload a valid file or enter text before generating a summary.")
    else:
        try:
            st.write_stream(
                generate_summary_stream(
                    text=input_text,
                    model=selected_model,
                    temp=temperature,
                    tokens=max_tokens
                )
            )
        except Exception as e:
            st.error(f"An error occurred while calling NVIDIA NIM API: {e}")
