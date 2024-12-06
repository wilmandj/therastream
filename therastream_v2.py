"""
Streamlit application entry point for Therastream.

This script sets up the main page configuration and initializes session state
for conversation and language selection. It provides a sidebar for navigation
and displays a welcome message on the home page.
"""

import streamlit as st
import os

st.set_page_config(
    page_title="Therastream Home Page",
    page_icon="🧘",
)

st.title("Therastream")

st.write("# Welcome to Therastream, the Application to assist your therapy needs! 🧘")

st.sidebar.success("Select an option.")

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

language_toggle = st.radio("Select Language", ("English", "German"), index=0)
if language_toggle != st.session_state.language:
    st.session_state.language = language_toggle

st.session_state.chat = None