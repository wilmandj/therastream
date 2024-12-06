# utils/translation_utils.py
from langchain.schema import SystemMessage, HumanMessage

def translate_with_openai(chat_instance, content, target_language):
    prompt = f"Translate the following text to {target_language}:\n\n{content}"
    response = chat_instance([
        SystemMessage(content="Translate text"),
        HumanMessage(content=prompt)
    ])
    return response.content

def translate_conversation(chat_instance, conversation, target_language):
    translated_conversation = []
    for message in conversation:
        translated_content = translate_with_openai(chat_instance, message["content"], target_language)
        translated_conversation.append({
            "role": message["role"],
            "content": translated_content
        })
    return translated_conversation