"""
Therapist Assistant Conversation Page

This script facilitates conversation with an AI therapist. Users can input 
questions or follow-ups, and the AI therapist responds based on the configured 
expertise. It includes options to save, load, and reset conversations.
"""
import os
import streamlit as st
import json
from langchain.schema import SystemMessage, HumanMessage
from utils.translation_utils import translate_conversation
from utils.session_utils import *

page = "therapist"

initialize_session_state()

chat = st.session_state.get("chat", None)

if chat is None:
    st.warning("Please connect to OpenAI on the Connect page to access functionality.")
else:
    st.title("💬 Therapist Assistant")

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
    display_conversation(conversation_text_widget, page, "AI Therapist")
    
    # Input for new messages
    if len( [ msg for msg in st.session_state.conversation[page][st.session_state.language] if msg["role"] == "assistant" ] ) == 0:
        st.markdown("## Ask Question: ")
    else:
        st.markdown("## Ask Further Question: ")

    with st.form(key='chat_input'):
        chat_input = st.text_input("Your Message")
        submit_button = st.form_submit_button("Submit")
        
    if submit_button:
        st.session_state.conversation[page][st.session_state.language].append({ "role": "user", "content": chat_input })
        continue_conversation(chat,page)
        display_conversation(conversation_text_widget, page, "AI Therapist")
            
    col1, col2, col3 = st.columns(3)

    with col1:

        filename = st.text_input("Enter filename for therapist conversation:")
        if st.button("Save Therapist Conversation"):
            if filename:
                # Prepare the content for download
                conversation_json = json.dumps(st.session_state.conversation[page][current_language])
                
                filepath = os.path.join("content", "therapist_conversations", f"{filename}_therapist_conversation.json")

                # Use st.download_button to let users download the prepared file
                st.download_button(
                    label="Download Therapist Conversation",
                    data=conversation_json,
                    file_name=filepath,
                    #file_name=f"{filename}_therapist_conversation.json",
                    mime="application/json",
                )
                st.success("Click the download button to save the conversation to your local machine!")

    with col2:
        uploaded_file = st.file_uploader("Choose a file to load therapist conversation", type="json")
        if uploaded_file is not None:
            try:
                # Clear the existing conversation and load the new one
                st.session_state.conversation[page][current_language] = json.load(uploaded_file)
                st.success("Therapist conversation loaded!")
                # Update the displayed conversation
                conversation_text_widget.write("")
                display_conversation(conversation_text_widget, page, "AI Therapist")
            except Exception as e:
                st.error(f"An error occurred: {e}")
            
            #try:
            #    st.session_state.conversation[page][current_language] = json.load(uploaded_file)
            #    st.success("Therapist conversation loaded!")
            #    for message in st.session_state.conversation[page][current_language]:
            #        if message["role"] == "user":
            #            st.write(f"You: {message['content']}")
            #        elif message["role"] == "assistant":
            #            st.write(f"Therapist: {message['content']}")
            #except Exception as e:
            #    st.error(f"An error occurred: {e}")

    with col3:
        if st.button("Reset Conversation"):
            st.session_state.conversation[page][st.session_state.language] = []
            conversation_text_widget.write("")
            st.success("Conversation reset successfully.")
