import streamlit as st
#from langchain_groq import ChatGroq

# Initialize the ChatGroq LLM
# llm = ChatGroq(
#     groq_api_key="",
#     model_name="llama3-8b-8192",
#     temperature=0,
# )
from openai import OpenAI
# headers={
#     "authorization": st.secrets["API_key"],
#     "Content-type": "application/json"
# }
Api_key = st.secrets['api_key']
id=st.secrets['link']
client = OpenAI(
    base_url=id,
    api_key=Api_key,
)
# Streamlit App
st.title("Paragraph Writing Assessment")

st.write("Enter your paragraph below and press **Evaluate** to get writing quality scores!")

# Input Text Box
user_input = st.text_area("Enter your paragraph here:", height=200)

# Button to evaluate
if st.button("Evaluate"):
    if user_input.strip():
        st.write("**Evaluating... Please wait.**")
        try:
            # Query the LLM
            prompt = (
                f"Evaluate the following paragraph for writing quality across various parameters "
                f"such as Clarity, Grammar, Engagement, Vocabulary, Organization, Tone, Contextuality, "
                f"Sentence Structure, Creativity, and Word Count. Provide scores out of 5 in a nice presentable table format.\n\n"
                f"Paragraph:\n{user_input}"
            )
            completion = client.chat.completions.create(
            model="meta-llama/llama-3.2-11b-vision-instruct:free",
            messages=[
                        {"role": "system", "content": "You are a helpful assistant for evaluting the user paragraph."},
                        {"role": "user", "content": prompt},
                    ]
                )
            st.write("### Assessment Report")
            st.write(completion.choices[0].message.content)
        except Exception as e:
            st.error(f"Error during evaluation: {e}")
    else:
        st.warning("Please enter a paragraph to evaluate.")
