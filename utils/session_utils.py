# session_utils.py

import streamlit as st

def initialize_session_state():
    # Initialize session state for conversation and system prompt
    if 'conversation' not in st.session_state:
        st.session_state.conversation = {
            "therapist": {"English": [], "German": []},
            "therapy author": {"English": [], "German": []}
        }
        
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = {"English": "", "German": ""}
        
    if 'language' not in st.session_state:
        st.session_state.language = "English"
