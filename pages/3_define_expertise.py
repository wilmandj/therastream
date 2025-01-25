"""
Define Expertise Page

This script allows users to specify additional expertise or focus areas for 
the AI therapist. It supports creating, improving, and extending therapist 
expertise prompts using AI responses. It includes functionality to save, load,
and reset expertise data.
"""
import os
import streamlit as st
import json
from langchain.schema import SystemMessage, HumanMessage
from utils.translation_utils import translate_with_openai
from utils.session_utils import initialize_session_state

# Function to get list of JSON files from the specified directory
def get_expert_files(directory):
    return [os.path.splitext(os.path.basename(f))[0] for f in os.listdir(directory) if f.endswith('.json')]

initialize_session_state()

language_toggle = st.sidebar.selectbox("Select Language", ("English", "German"), index=(st.session_state.language!='English'), key='language')
if language_toggle != st.session_state.language:
    st.session_state.language = language_toggle
    
chat = st.session_state.get("chat", None)

if chat is None:
    st.warning("Please connect to OpenAI on the Connect page to access functionality.")
else:
    st.title("🧠 Define Therapist Expertise")

    target_language = 'English' if st.session_state.language == "English" else 'Deutsch'

    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = {"English": "", "German": ""}
        
    if st.session_state.system_prompt[st.session_state.language] == "":
        other_language = "German" if st.session_state.language == "English" else "English"
        if st.session_state.system_prompt[other_language]:
            st.session_state.system_prompt[st.session_state.language] = translate_with_openai(
                chat, st.session_state.system_prompt[other_language], target_language
            )

    st.markdown("#### _Expert_ _Knowledge_")
    expert_knowledge_text_widget = st.empty()
    
    if 'ai_created_expertise' not in st.session_state:
        st.session_state.ai_created_expertise = False
    else:
        expert_knowledge_text_widget.write(st.session_state.system_prompt[st.session_state.language])
    
    with st.form(key='expertise_input'):
        expertise = st.text_area("Enter additional expertise or focus areas for the therapist:")
        create_expertise = st.form_submit_button("Create Expertise")
    
    with st.form(key='feedback_input'):
        feedback = st.text_area("Provide feedback on the current expertise (optional):")
        improve_expertise = st.form_submit_button("Improve Expertise")
        add_to_expertise = st.form_submit_button("Add to Expertise")
    
    if create_expertise and expertise and not st.session_state.ai_created_expertise:
        st.session_state.system_prompt[st.session_state.language] = f"You are an empathetic and knowledgeable therapist with expertise in {expertise}. Provide thoughtful and helpful responses."

    if create_expertise and expertise:
        question = f"Suggest a system prompt for expertise in {expertise}."
        ai_message = chat([
            SystemMessage(content="Suggest a system prompt for expertise in this topic."),
            HumanMessage(content=question)
        ])
        st.session_state.system_prompt[st.session_state.language] = ai_message.content
        expert_knowledge_text_widget.write(st.session_state.system_prompt[st.session_state.language])
        st.session_state.ai_created_expertise = True
        st.success("Created Expertise")
    
    if st.session_state.ai_created_expertise:
        if improve_expertise and feedback:
            improve_question = f"Given the feedback '{feedback}', improve the expertise: {st.session_state.system_prompt[st.session_state.language]}"
            ai_message = chat([
                SystemMessage(content=st.session_state.system_prompt[st.session_state.language]),
                HumanMessage(content=improve_question)
            ])
            st.session_state.system_prompt[st.session_state.language] = ai_message.content
            #st.write(f"Improved Expertise: {ai_message.content}")
            expert_knowledge_text_widget.write(st.session_state.system_prompt[st.session_state.language])
            st.success("Updated Expertise")

        
        if add_to_expertise and feedback:
            add_question = f"Based on the feedback '{feedback}', suggest additional expertise to complement: {st.session_state.system_prompt[st.session_state.language]}"
            ai_message = chat([
                SystemMessage(content=st.session_state.system_prompt[st.session_state.language]),
                HumanMessage(content=add_question)
            ])
            st.session_state.system_prompt[st.session_state.language] += "\n\n" + ai_message.content
            #st.write(f"Extended Expertise: {st.session_state.system_prompt[st.session_state.language]}")
            expert_knowledge_text_widget.write(st.session_state.system_prompt[st.session_state.language])
            st.success("Extended Expertise")
    
    col1, col2 = st.columns(2)

    with col1:
        filename = st.text_input("Enter filename for Expert Knowledge:")
        if st.button("Save Expert Knowledge"):
            if filename:
                # Prepare the content for download
                filepath = os.path.join("content", "expert_knowledge", f"{filename}_Expert_Knowledge.json")
                # Use st.download_button to let users download the prepared file
                st.download_button(
                    label="Download Expert Knowledge",
                    data=st.session_state.system_prompt[st.session_state.language],
                    file_name=filepath,
                    mime="application/json",
                )
                st.success("Click the download button to save the expert knowledge to your local machine!")

    with col2:    
        uploaded_file = st.file_uploader("Choose a file to load Expert Knowledge", type="json")
        if uploaded_file is not None:
            try:
                # Clear the existing conversation and load the new one
                data = json.load(uploaded_file)
                st.session_state.system_prompt[st.session_state.language] = data.get("Expert_Knowledge", "")
                st.success("Expert Knowledge loaded!")
                # Update the displayed conversation
                expert_knowledge_text_widget.write(st.session_state.system_prompt[st.session_state.language])
            except Exception as e:
                st.error(f"An error occurred: {e}")

        # Get the available files from the directory
        expert_files = get_expert_files(os.path.join("content", "expert_knowledge"))
        if expert_files:
            selected_file_name = st.selectbox("Select an Predefined Expert Knowledge", [ f for f in expert_files], index=None )
            # If a file is selected, proceed to load it
            if selected_file_name:
                selected_file_path = os.path.join("content", "expert_knowledge", selected_file_name) + ".json"
        
                # Read the selected file and process it
                try:
                    with open(selected_file_path, 'r') as file:
                        data = json.load(file)
                        # Assuming st.session_state.system_prompt and language are already defined
                        st.session_state.system_prompt[st.session_state.language] = data.get("Expert_Knowledge", "")
                        st.success("Expert Knowledge loaded!")
                        # Display the loaded expert knowledge
                        expert_knowledge_text_widget.write(st.session_state.system_prompt[st.session_state.language])
        
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            
        if st.button("Reset Expertise"):
            st.session_state.system_prompt[st.session_state.language] = ""
            expert_knowledge_text_widget.write("")
            st.session_state.ai_created_expertise = False
            st.success("Expertise reset successfully.")