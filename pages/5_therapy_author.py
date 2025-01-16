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

language_toggle = st.sidebar.selectbox("Select Language", ("English", "German"), index=(st.session_state.language!='English'), key='language')
if language_toggle != st.session_state.language:
    st.session_state.language = language_toggle
    
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
    
    col1, col2 = st.columns(2)

    with col1:
        filename = st.text_input("Enter filename for therapy author conversation:")
        if st.button("Save Therapy Author Conversation"):
            if filename:
                # Prepare the content for download
                conversation_json = json.dumps(st.session_state.conversation[page][current_language])
                filepath = os.path.join("content", "therapy_author_conversations", f"{filename}_therapist_conversation.json")
                # Use st.download_button to let users download the prepared file
                st.download_button(
                    label="Download Therapy Author Conversation",
                    data=conversation_json,
                    file_name=filepath,
                    mime="application/json",
                )
                st.success("Click the download button to save the conversation to your local machine!")

    with col2:
        uploaded_file = st.file_uploader("Choose a file to load therapy author conversation", type="json")
        if uploaded_file is not None:
            try:
                # Clear the existing conversation and load the new one
                st.session_state.conversation[page][current_language] = json.load(uploaded_file)
                st.success("Therapy author conversation loaded!")
                # Update the displayed conversation
                conversation_text_widget.write("")
                display_conversation(conversation_text_widget, page, "AI Therapy Author")
            except Exception as e:
                st.error(f"An error occurred: {e}")

        if st.button("Reset Conversation"):
            st.session_state.conversation[page][st.session_state.language] = []
            conversation_text_widget.write("")
            st.success("Conversation reset successfully.")
            