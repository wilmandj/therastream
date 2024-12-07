"""

Streamlit application entry point for Therastream.

This script sets up the main page configuration and initializes session state
for conversation and language selection. It provides a sidebar for navigation
and displays a welcome message on the home page.
"""

import streamlit as st
import os
from utils.session_utils import initialize_session_state

st.set_page_config(
    page_title="Therastream Home Page",
    page_icon="🧘",
)

initialize_session_state()

st.title("Therastream")

st.write("# Welcome to Therastream, the Application to assist your therapy needs! 🧘")

st.sidebar.success("Select an option above.")

st.sidebar.radio("Select Language", ("English", "German"), index=0, key='language')

st.session_state.chat = None