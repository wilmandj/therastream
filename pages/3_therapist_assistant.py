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

initialize_session_state()

chat = st.session_state.get("chat", None)

if chat is None:
    st.warning("Please connect to OpenAI on the Connect page to access functionality.")
else:
    st.title("💬 Therapist Assistant")

    if "conversation" not in st.session_state:
        st.session_state.conversation = {"therapist": {"English": [], "German": []}}

    current_language = st.session_state.language
    other_language = "German" if current_language == "English" else "English"
    
    if not st.session_state.conversation["therapist"][current_language]:
        if st.session_state.conversation["therapist"][other_language]:
            st.session_state.conversation["therapist"][current_language] = translate_conversation(
                chat, st.session_state.conversation["therapist"][other_language], current_language
            )

    current_conversation = st.session_state.conversation["therapist"][current_language]

    # Display existing conversation
    st.markdown("#### _Conversation_")
    conversation_text_widget = st.empty()
    display_conversation(conversation_text_widget, "therapist", "AI Therapist")
    
    # Input for new messages
    if len( [ msg for msg in st.session_state.conversation["therapist"][st.session_state.language] if msg["role"] == "assistant" ] ) == 0:
        st.markdown("## Ask Question: ")
    else:
        st.markdown("## Ask Further Question: ")
    chat_input = st.text_input("Your Message", key='chat_input')
    
    if st.button("Send"):
        if chat_input:
            st.session_state.conversation["therapist"][st.session_state.language].append({ "role": "user", "content": chat_input })
            continue_conversation(chat,"therapist")
            display_conversation(conversation_text_widget, "therapist", "AI Therapist")
            
#    for message in current_conversation:
#        if message["role"] == "user":
#            st.write(f"You: {message['content']}")
#        elif message["role"] == "assistant":
#            st.write(f"Therapist: {message['content']}")

#    question = st.text_input("Your question or follow-up for the AI Therapist:")

#    if st.button("Ask") and question:
#        if not current_conversation:
#            st.session_state.conversation["therapist"][current_language].append(
#                {"role": "system", "content": st.session_state.system_prompt[current_language]}
#            )

#        st.session_state.conversation["therapist"][current_language].append(
#            {"role": "user", "content": question}
#        )

#        ai_message = chat([
#            SystemMessage(content=st.session_state.system_prompt[current_language]),
#            HumanMessage(content=question)
#        ])
        
#        st.session_state.conversation["therapist"][current_language].append(
#            {"role": "assistant", "content": ai_message.content}
#        )

#        st.write(f"Therapist: {ai_message.content}")

    col1, col2, col3 = st.columns(3)

    with col1:
        filename = st.text_input("Enter filename for therapist conversation:")
        if st.button("Save Therapist Conversation"):
            if filename:
                filepath = os.path.join("content", "therapist_conversations", f"{filename}_therapist_conversation.json")
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "w") as f:
                    json.dump(st.session_state.conversation["therapist"][current_language], f)
                st.success(f"Therapist conversation saved to {filepath}!")
        
        st.download_button(
            label="Download Therapist Conversation",
            data=json.dumps(st.session_state.conversation["therapist"][current_language]),
            file_name="therapist_conversation.json",
            mime="application/json",
        )

    with col2:
        uploaded_file = st.file_uploader("Choose a file to load therapist conversation", type="json")
        if uploaded_file is not None:
            try:
                st.session_state.conversation["therapist"][current_language] = json.load(uploaded_file)
                st.success("Therapist conversation loaded!")
                for message in st.session_state.conversation["therapist"][current_language]:
                    if message["role"] == "user":
                        st.write(f"You: {message['content']}")
                    elif message["role"] == "assistant":
                        st.write(f"Therapist: {message['content']}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    with col3:
        if st.button("Reset Conversation"):
            st.session_state.conversation["therapist"][st.session_state.language] = []
            conversation_text_widget.write("")
            st.success("Conversation reset successfully.")
