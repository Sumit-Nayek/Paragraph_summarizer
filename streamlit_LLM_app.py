import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

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

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.header("🚀 Speed & Model Settings")

# Model Mode Selector (Fast vs. Deep)
model_mode = st.sidebar.radio(
    "Select Inference Mode:",
    ["⚡ Fast Mode (Llama 3.1 8B)", "🧠 Deep Mode (Llama 3.3 70B)"],
    help="Fast Mode gives sub-second responses; Deep Mode provides higher reasoning and detail."
)

# Map human-readable selection to NVIDIA NIM model IDs
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

# --- 4. INITIALIZE OPENAI CLIENT POINTING TO NVIDIA NIM ---
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=nvidia_api_key
)

# --- 5. STREAMING GENERATOR FUNCTION ---
def generate_summary_stream(text: str, model: str, temp: float, tokens: int):
    """
    Generator function that streams tokens from NVIDIA NIM API in real time.
    """
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
        stream=True  # Enables real-time streaming
    )

    for chunk in response_stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# --- 6. MAIN INPUT & DISPLAY LOGIC ---
input_text = st.text_area(
    "Paste your paragraph or text here:",
    height=220,
    placeholder="Enter long text or paragraphs you want to summarize..."
)

if st.button("Generate Real-Time Summary", type="primary"):
    if not input_text.strip():
        st.warning("Please enter some text before generating a summary.")
    else:
        st.subheader("Summary Result:")
        try:
            # st.write_stream consumes the generator and renders tokens instantly
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
