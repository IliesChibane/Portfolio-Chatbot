from dotenv import load_dotenv
load_dotenv()  # Loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure the Generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo", layout="wide")

# Add custom CSS for the chat popup
st.markdown(
    """
    <style>
    .chat-popup {
        position: fixed;
        bottom: 0;
        right: 0;
        border: 3px solid #f1f1f1;
        z-index: 9;
        width: 100%;
        max-width: 600px;
    }
    .chat-container {
        max-height: 300px;
        overflow-y: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Chat popup UI
with st.expander("Chat with Gemini", expanded=True):
    st.markdown('<div class="chat-popup">', unsafe_allow_html=True)
    st.subheader("Gemini LLM Application")

    # Display chat history
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Input for user query
    input = st.text_input("Type your message here:", key="input")
    submit = st.button("Send")

    if submit and input:
        response = get_gemini_response(input)
        st.session_state['chat_history'].append(("You", input))
        st.subheader("Response")
        for chunk in response:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

    st.markdown('</div>', unsafe_allow_html=True)
