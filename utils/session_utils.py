# session_utils.py

import streamlit as st
from langchain.schema import SystemMessage, HumanMessage, AIMessage

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

    if 'chat_input' not in st.session_state:
        st.session_state.chat_input = ""

def bold(string):
    return f"**{string}**" 

# Function to display the conversation
def display_conversation(widget, page, ai_role):
    if len(st.session_state.conversation[page][st.session_state.language])==0:
        widget.write("")
    else:
        display = []
        for index, message in enumerate(st.session_state.conversation[page][st.session_state.language]):
            if message["role"] == "user":
                display.append( f"""**You:** {message['content']}""" )
            elif message["role"] == "assistant":
                display.append( f"""**{ai_role}**: {message['content']}""" )
        widget.write("\n\n".join(display))

def continue_conversation(chat, page):
    messages_langchain = [SystemMessage(content=st.session_state.system_prompt[st.session_state.language])]
    for message in st.session_state.conversation[page][st.session_state.language]:
        if message["role"] == "user":
            messages_langchain.append( HumanMessage(content=message["content"]) )
        elif message["role"] == "assistant":
            messages_langchain.append( AIMessage(content=message["content"]) )
        else:
            print (f"""Error: Conversation contains message with role = {message['role']}""")
            return
    ai_response = chat(messages_langchain)
    st.session_state.conversation[page][st.session_state.language].append( {"role": "assistant", "content": ai_response.content } )
