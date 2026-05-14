## The solo problem f this reposiratory is that it need groq API key run
import streamlit as st
#from langchain_groq import ChatGroq

from openai import OpenAI
Api_key= st.secrets['api_key']
id=st.secrets['link']
client = OpenAI(
    base_url=id,
    api_key=Api_key,
)
# Streamlit App
st.title("Scientific paper summarizer")

st.write("Enter your paragraph below or Upload your scientific paper")

# Input Text Box
user_input = st.text_area("Enter your paragraph here:", height=200)

# Button to evaluate
if st.button("Summarize"):
    if user_input.strip():
        st.write("**Processing... Please wait.**")
        try:
            # Query the LLM
            prompt = (
                f"Sumarise the uploaded documents with refference"
                f"such as Clarity, Grammar, Engagement, Vocabulary, Organization, Tone, Contextuality, "
                f"Sentence Structure, Research domain, type of model used ,Creativity, and Scientific contribution. Provide scores out of 5 in a nice presentable table format.\n\n"
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
