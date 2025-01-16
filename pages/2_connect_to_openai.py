"""
Connect to OpenAI Page

This script allows users to connect to the OpenAI API by providing an API key. 
It initializes a chat instance for further interaction and saves the API key 
for future sessions.
"""

import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from utils.session_utils import initialize_session_state

# Function to get OpenAI key from file:
def getkey(keyfile, dir_keys, default_envar=None):
    try:
        with open(os.path.join(dir_keys, keyfile + '.key'), 'r') as f:
            lines = f.readlines()
            for line in lines:
                if len(line.strip()) > 0:
                    envvar, value = line.split(':')
                    value = value.strip()
                    os.environ[envvar] = value
    except:
        envvar = default_envar
        os.environ[envvar] = ""

# Function to initialize OpenAI API
def initialize_openai(api_key):
    os.environ["OPENAI_API_KEY"] = api_key

# Function to create a chat instance
def create_chat_instance(api_key, model="gpt-4o"):
    return ChatOpenAI(
        openai_api_key=api_key,
        model=model
    )

st.title("🔗 Connect to OpenAI")

initialize_session_state()

# 1. API Key
home = os.environ["HOME"]
dir_keys = home + '/keys'
os.makedirs(dir_keys, exist_ok=True)
getkey("openai", dir_keys, default_envar="OPENAI_API_KEY")
    
api_key = st.text_input("Enter OpenAI API Key", os.environ.get("OPENAI_API_KEY", ""), type="password")

model_options = ["gpt-4o", "gpt-3.5-turbo", "gpt-3", "gpt-4"]
selected_model = st.selectbox("Select OpenAI Model", model_options, index=0)

if api_key:
    initialize_openai(api_key)
    chat = create_chat_instance(api_key, model=selected_model)
    st.session_state.chat = chat
    st.success("Connected to OpenAI with model: " + selected_model)

    # Save the new API key to the default key file
    with open(os.path.join(dir_keys, 'openai.key'), 'w') as f:
        f.write(f"OPENAI_API_KEY: {api_key}")
        st.success("API Key saved successfully!")