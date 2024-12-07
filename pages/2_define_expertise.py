"""
Define Expertise Page

This script allows users to specify additional expertise or focus areas for 
the AI therapist. It supports creating, improving, and extending therapist 
expertise prompts using AI responses. It includes functionality to save, load,
and reset expertise data.
"""

import streamlit as st
import json
from langchain.schema import SystemMessage, HumanMessage
from utils.translation_utils import translate_with_openai
from utils.session_utils import initialize_session_state

initialize_session_state()

chat = st.session_state.get("chat", None)

if chat is None:
    st.warning("Please connect to OpenAI on the Connect page to access functionality.")
else:
    st.title("🧠 Define Therapist Expertise")

    target_language = 'English' if st.session_state.language == "English" else 'Deutsch'
    
    # Ensure system_prompt is stored for both languages
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = {"English": "", "German": ""}
        
    if st.session_state.system_prompt[st.session_state.language] == "":
        other_language = "German" if st.session_state.language == "English" else "English"
        if st.session_state.system_prompt[other_language]:
            st.session_state.system_prompt[st.session_state.language] = translate_with_openai(
                chat, st.session_state.system_prompt[other_language], target_language
            )

    expertise = st.text_area("Enter additional expertise or focus areas for the therapist:")
    feedback = st.text_area("Provide feedback on the current expertise (optional):")

    if 'ai_created_expertise' not in st.session_state:
        st.session_state.ai_created_expertise = False

    if expertise and not st.session_state.ai_created_expertise:
        st.session_state.system_prompt[st.session_state.language] = f"You are an empathetic and knowledgeable therapist with expertise in {expertise}. Provide thoughtful and helpful responses."

    if st.button("Create Expertise") and expertise:
        question = f"Suggest a system prompt for expertise in {expertise}."
        ai_message = chat([
            SystemMessage(content="Suggest a system prompt for expertise in this topic."),
            HumanMessage(content=question)
        ])
        st.session_state.system_prompt[st.session_state.language] = ai_message.content
        st.write(f"Suggested Expertise: {ai_message.content}")
        st.session_state.ai_created_expertise = True
    
    if st.session_state.ai_created_expertise:
        if st.button("Improve Expertise") and feedback:
            improve_question = f"Given the feedback '{feedback}', improve the expertise: {st.session_state.system_prompt[st.session_state.language]}"
            ai_message = chat([
                SystemMessage(content=st.session_state.system_prompt[st.session_state.language]),
                HumanMessage(content=improve_question)
            ])
            st.session_state.system_prompt[st.session_state.language] = ai_message.content
            st.write(f"Improved Expertise: {ai_message.content}")
        
        if st.button("Add to Expertise") and feedback:
            add_question = f"Based on the feedback '{feedback}', suggest additional expertise to complement: {st.session_state.system_prompt[st.session_state.language]}"
            ai_message = chat([
                SystemMessage(content=st.session_state.system_prompt[st.session_state.language]),
                HumanMessage(content=add_question)
            ])
            st.session_state.system_prompt[st.session_state.language] += " " + ai_message.content
            st.write(f"Extended Expertise: {st.session_state.system_prompt[st.session_state.language]}")

    col1, col2, col3 = st.columns(3)

    with col1:
        filename = st.text_input("Enter filename for Expert Knowledge:")
        if st.button("Save Expert Knowledge"):
            if filename:
                filepath = os.path.join("content", "expert_knowledge", f"{filename}_Expert_Knowledge.json")
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath, "w") as f:
                    json.dump({"Expert_Knowledge": st.session_state.system_prompt[st.session_state.language]}, f)
                st.success(f"Expert Knowledge saved to {filepath}!")

    with col2:    
        uploaded_file = st.file_uploader("Choose a file to load Expert Knowledge", type="json")
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                st.session_state.system_prompt[st.session_state.language] = data.get("Expert_Knowledge", "")
                st.success("Expert Knowledge loaded!")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    with col3:
        if st.button("Reset Expertise"):
            st.session_state.system_prompt[st.session_state.language] = ""
            st.success("Expertise reset successfully.")
