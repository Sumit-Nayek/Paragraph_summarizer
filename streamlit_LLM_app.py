import streamlit as st
#from langchain_groq import ChatGroq

# Initialize the ChatGroq LLM
# llm = ChatGroq(
#     groq_api_key="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",
#     model_name="llama3-8b-8192",
#     temperature=0,
# )

# Streamlit App
st.title("Paragraph Writing Assessment")

st.write("Enter your paragraph below and press **Evaluate** to get writing quality scores!")

# Input Text Box
user_input = st.text_area("Enter your paragraph here:", height=200)

# Button to evaluate
if st.button("Evaluate"):
    if user_input.strip():
        st.write("**Evaluating... Please wait.**")
#         try:
#             # Query the LLM
#             prompt = (
#                 f"Evaluate the following paragraph for writing quality across various parameters "
#                 f"such as Clarity, Grammar, Engagement, Vocabulary, Organization, Tone, Contextuality, "
#                 f"Sentence Structure, Creativity, and Word Count. Provide scores out of 5 in a table format.\n\n"
#                 f"Paragraph:\n{user_input}"
#             )
#             response = llm.invoke(prompt)
#             st.write("### Assessment Report")
#             st.write(response.content)
        # except Exception as e:
        #     st.error(f"Error during evaluation: {e}")
    else:
        st.warning("Please enter a paragraph to evaluate.")
