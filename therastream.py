import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

messages = {}
agents = ["therapist","therapy author"]
for agent in agents:
    messages[agent] = []
st.session_state.conversation = messages

# Function to initialize OpenAI API
def initialize_openai(api_key):
    os.environ["OPENAI_API_KEY"] = api_key

# Function to create a chat instance
def create_chat_instance(api_key):
    return ChatOpenAI(
        openai_api_key=api_key,
        model='gpt-4o'
    )

# Streamlit application
def main():
    st.title("Therastream")

    # 1. API Key
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    if api_key:
        initialize_openai(api_key)
        chat = create_chat_instance(api_key)
        st.session_state.chat = chat
        st.success("Connected to OpenAI!")

    # Initialize session state for conversation and system prompt
    if 'conversation' not in st.session_state:
        st.session_state.conversation = {}
        st.session_state.conversation["therapist"] = []
        st.session_state.conversation["therapy author"] = []
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = ""

    # 2. Additional expertise for the therapist
    st.header("Therapist Expertise")
    expertise = st.text_area("Enter additional expertise or focus areas for the therapist:")
    if expertise:
        st.session_state.system_prompt = f"You are an empathetic and knowledgeable therapist with expertise in {expertise}. Provide thoughtful and helpful responses."

    # 2. a. Ask an AI Therapist
    
    st.header("Ask an AI Therapist")
    question = st.text_input("Your question for the AI Therapist:")
    if st.button("Ask") and question and st.session_state.system_prompt:
        # Initial message setup
        messages["therapist"] = [
            SystemMessage(content=st.session_state.system_prompt),
            HumanMessage(content=question)
        ]
        ai_message = chat(messages["therapist"])
        messages["therapist"].append(ai_message)
        st.session_state.conversation["therapist"].extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": ai_message.content}
        ])
        st.write(ai_message.content)

    # 2. b. Follow-up questions
    st.header("Follow-up Conversation")
    follow_up = st.text_input("Your follow-up question:")
    if st.button("Ask Follow-up") and follow_up:
        messages["therapist"].append(HumanMessage(content=follow_up))
        ai_message = chat(messages["therapist"])
        messages["therapist"].append(ai_message)
        st.session_state.conversation["therapist"].extend([
            {"role": "user", "content": follow_up},
            {"role": "assistant", "content": ai_message.content}
        ])
        st.write(ai_message.content)

    # 3. a. Create Book Content
    st.header("Create Book Content")
    book_topic = st.text_input("Enter a topic for your book:")
    if st.button("Generate Book Content") and book_topic:
        book_prompt = f"You are an expert self-help author. Summarize the topic '{book_topic}' for a self-help book."
        messages["therapy author"] = [
            SystemMessage(content=st.session_state.system_prompt),
            HumanMessage(content=book_prompt)
        ]
        book_content_message = chat(messages["therapy author"])
        messages["therapy author"].append(book_content_message)
        st.session_state.conversation["therapy author"].extend([
            {"role": "user", "content": book_prompt},
            {"role": "assistant", "content": book_content_message.content}
        ])
        st.write(book_content_message.content)

    # 3. b. Follow-up feedback
    st.header("Feedback on Book Content")
    feedback = st.text_area("Provide your feedback on the suggested content:")
    if st.button("Submit Feedback") and feedback:
        feedback_prompt = f"The user provided the following feedback on the book content: {feedback}. Update the content accordingly."
        messages["therapy author"].append(HumanMessage(content=feedback_prompt))
        feedback_response = chat(messages["therapy author"])
        messages["therapy author"].append(feedback_response)
        st.session_state.conversation["therapy author"].extend([
            {"role": "user", "content": feedback_prompt},
            {"role": "assistant", "content": feedback_response.content}
        ])
        st.write(feedback_response.content)

    # 4. Save content
    if st.button("Save Conversation"):
        with open("conversation.json", "w") as f:
            json.dump(st.session_state.conversation, f)
        st.success("Conversation saved!")

    # 5. Load content
    if st.button("Load Conversation"):
        try:
            with open("conversation.json", "r") as f:
                st.session_state.conversation = json.load(f)
            st.success("Conversation loaded!")
        except FileNotFoundError:
            st.error("No saved conversation found.")

    # 6. Reset content
    if st.button("Reset Conversation"):
        st.session_state.conversation = []
        st.success("Conversation reset!")

if __name__ == "__main__":
    main()
    
