import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env if running locally
load_dotenv()

# --- 1. API KEY RESOLUTION ---
# Checks Streamlit Secrets first (for Cloud), then environment variables (for Local)
nvidia_api_key = st.secrets.get("NVIDIA_API_KEY") or os.getenv("NVIDIA_API_KEY")

# --- 2. STREAMLIT UI SETUP ---
st.set_page_config(
    page_title="AI Paragraph Summarizer (NVIDIA NIM)",
    page_icon="📝",
    layout="centered"
)

st.title("📝 AI Paragraph Summarizer")
st.caption("Powered by NVIDIA NIM API & Llama-3.3-70B-Instruct")

# Sidebar for controls
st.sidebar.header("Summarizer Settings")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.2, 0.1)
max_tokens = st.sidebar.slider("Max Summary Tokens", 50, 1000, 250, 50)

# Check for API Key
if not nvidia_api_key:
    st.error("⚠️ NVIDIA API Key not found. Please set `NVIDIA_API_KEY` in Streamlit Secrets or your `.env` file.")
    st.stop()

# --- 3. INITIALIZE OPENAI CLIENT POINTING TO NVIDIA NIM ---
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=nvidia_api_key
)

# --- 4. MAIN INPUT & SUMMARIZATION LOGIC ---
input_text = st.text_area(
    "Paste your paragraph or text here:",
    height=250,
    placeholder="Enter long text or paragraphs you want to summarize..."
)

if st.button("Summarize Paragraph", type="primary"):
    if not input_text.strip():
        st.warning("Please enter some text before generating a summary.")
    else:
        with st.spinner("Generating summary using NVIDIA NIM..."):
            try:
                response = client.chat.completions.create(
                    model="meta/llama-3.3-70b-instruct",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a professional text summarizer. "
                                "Summarize the provided text into a concise, well-structured "
                                "paragraph capturing all key points."
                            )
                        },
                        {
                            "role": "user",
                            "content": f"Please summarize the following text:\n\n{input_text}"
                        }
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                summary = response.choices[0].message.content
                
                st.subheader("Summary Result:")
                st.success(summary)
                
            except Exception as e:
                st.error(f"An error occurred while calling NVIDIA NIM API: {e}")