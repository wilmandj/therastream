"""
Therapy Author Content Creation Page

This script enables users to engage with an AI therapy author to create book 
content or related material. It supports conversation management, including 
saving, loading, and resetting interactions.
"""
import os
import streamlit as st
import json
from langchain.schema import SystemMessage, HumanMessage
from utils.translation_utils import translate_conversation
from utils.session_utils import *

page = "therapy author"

initialize_session_state()

chat = st.session_state.get("chat", None)

if chat is None:
    st.warning("Please connect to OpenAI on the Connect page to access functionality.")
else:
    st.title("📚 Create Book Content")

    if "conversation" not in st.session_state:
        st.session_state.conversation = {page: {"English": [], "German": []}}

    current_language = st.session_state.language
    other_language = "German" if current_language == "English" else "English"

    if not st.session_state.conversation[page][current_language]:
        if st.session_state.conversation[page][other_language]:
            st.session_state.conversation[page][current_language] = translate_conversation(
                chat, st.session_state.conversation[page][other_language], current_language
            )

    current_conversation = st.session_state.conversation[page][current_language]

    # Display existing conversation
    st.markdown("#### _Conversation_")
    conversation_text_widget = st.empty()
    display_conversation(conversation_text_widget, page, "AI Therapy Author")
    
    # Input for new messages
    if len( [ msg for msg in st.session_state.conversation[page][st.session_state.language] if msg["role"] == "assistant" ] ) == 0:
        st.markdown("## Ask Question: ")
    else:
        st.markdown("## Ask Further Question: ")

    with st.form(key='chat_input'):
        chat_input = st.text_input("Your Request")
        submit_button = st.form_submit_button("Submit")
        
    if submit_button:
        st.session_state.conversation[page][st.session_state.language].append({ "role": "user", "content": chat_input })
        continue_conversation(chat,page)
        display_conversation(conversation_text_widget, page, "AI Therapy Author")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        filename = st.text_input("Enter filename for therapy author conversation:")
        if st.button("Save Therapy Author Conversation"):
            if filename:
                filepath = os.path.join("content", "therapy_author_conversations", f"{filename}_therapy_author_conversation.json")
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "w") as f:
                    json.dump(st.session_state.conversation[page][current_language], f)
                st.success(f"Therapy author conversation saved to {filepath}!")
        
        st.download_button(
            label="Download Therapy Author Conversation",
            data=json.dumps(st.session_state.conversation[page][current_language]),
            file_name="therapy_author_conversation.json",
            mime="application/json",
        )

    with col2:
        uploaded_file = st.file_uploader("Choose a file to load therapy author conversation", type="json")
        if uploaded_file is not None:
            try:
                st.session_state.conversation[page][current_language] = json.load(uploaded_file)
                st.success("Therapy author conversation loaded!")
                for message in st.session_state.conversation[page][current_language]:
                    if message["role"] == "user":
                        st.write(f"You: {message['content']}")
                    elif message["role"] == "assistant":
                        st.write(f"Therapy Author: {message['content']}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    with col3:
        if st.button("Reset Conversation"):
            st.session_state.conversation[page][st.session_state.language] = []
            conversation_text_widget.write("")
            st.success("Conversation reset successfully.")
            