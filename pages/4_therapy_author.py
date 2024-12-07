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
from utils.session_utils import initialize_session_state

initialize_session_state()

chat = st.session_state.get("chat", None)

if chat is None:
    st.warning("Please connect to OpenAI on the Connect page to access functionality.")
else:
    st.title("📚 Create Book Content")

    if "conversation" not in st.session_state:
        st.session_state.conversation = {"therapy author": {"English": [], "German": []}}

    current_language = st.session_state.language
    other_language = "German" if current_language == "English" else "English"

    if not st.session_state.conversation["therapy author"][current_language]:
        if st.session_state.conversation["therapy author"][other_language]:
            st.session_state.conversation["therapy author"][current_language] = translate_conversation(
                chat, st.session_state.conversation["therapy author"][other_language], current_language
            )

    current_conversation = st.session_state.conversation["therapy author"][current_language]

    for message in current_conversation:
        if message["role"] == "user":
            st.write(f"You: {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"Therapy Author: {message['content']}")

    question = st.text_input("Your question or follow-up for the AI Therapy Author:")

    if st.button("Ask") and question:
        if not current_conversation:
            st.session_state.conversation["therapy author"][current_language].append(
                {"role": "system", "content": st.session_state.system_prompt[current_language]}
            )

        st.session_state.conversation["therapy author"][current_language].append(
            {"role": "user", "content": question}
        )

        ai_message = chat([
            SystemMessage(content=st.session_state.system_prompt[current_language]),
            HumanMessage(content=question)
        ])
        
        st.session_state.conversation["therapy author"][current_language].append(
            {"role": "assistant", "content": ai_message.content}
        )

        st.write(f"Therapy Author: {ai_message.content}")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        filename = st.text_input("Enter filename for therapy author conversation:")
        if st.button("Save Therapy Author Conversation"):
            if filename:
                filepath = os.path.join("content", "therapy_author_conversations", f"{filename}_therapy_author_conversation.json")
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "w") as f:
                    json.dump(st.session_state.conversation["therapy author"][current_language], f)
                st.success(f"Therapy author conversation saved to {filepath}!")
        
        st.download_button(
            label="Download Therapy Author Conversation",
            data=json.dumps(st.session_state.conversation["therapy author"][current_language]),
            file_name="therapy_author_conversation.json",
            mime="application/json",
        )

    with col2:
        uploaded_file = st.file_uploader("Choose a file to load therapy author conversation", type="json")
        if uploaded_file is not None:
            try:
                st.session_state.conversation["therapy author"][current_language] = json.load(uploaded_file)
                st.success("Therapy author conversation loaded!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    with col3:
        if st.button("Reset Conversation"):
            if st.checkbox("Confirm reset"):
                st.session_state.conversation["therapy author"][current_language] = []
                st.success("Conversation reset successfully.")
