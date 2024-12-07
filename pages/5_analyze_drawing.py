"""
Analyze Drawing Page

This script facilitates the upload and analysis of drawings by interpreting 
them as expressions of the subject's subconscious mind. It combines image 
captions with system prompts for psychological analysis and displays AI 
responses.

**Image Analysis:**
   - The image analysis now saves images to a local directory and uses image URLs for processing.
"""

import streamlit as st
import os
from PIL import Image
from langchain.schema import SystemMessage, HumanMessage
import base64
from io import BytesIO
from utils.session_utils import initialize_session_state

initialize_session_state()

chat = st.session_state.get("chat", None)

if chat is None:
    st.warning("Please connect to OpenAI on the Connect page to access functionality.")
else:
    st.title("🎨 Analyze Drawing")

    # Create content directories
    content_dir = "content"
    images_dir = os.path.join(content_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    # Step 1: Upload an image
    uploaded_file = st.file_uploader("Upload an image (e.g., jpg, png)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Drawing", use_column_width=True)

        # Save image to local directory
        image_path = os.path.join(images_dir, uploaded_file.name)
        image.save(image_path)

        # Use image URL for analysis
        image_url = f"/content/images/{uploaded_file.name}"
        
        # Step 2: Provide a caption/description
        caption = st.text_input("Provide a caption or description for the image:")
        
        # Step 3: Analyze the image and caption
        if st.button("Analyze Drawing"):
            if caption:
                # Combine system prompts
                current_prompt = st.session_state.system_prompt[st.session_state.language]
                analysis_prompt = (
                    f"""{current_prompt} You are an expert in psychological analysis. 
                    Interpret the drawing as an expression of the subject's subconscious mind. 
                    Analyze the drawing and caption to provide insights into the subject's state of mind.
                    Make sure to pay attention to - and highlight - elements in the drawing which emphasize 
                    and which go beyond the content of the caption.
                    """
                )
                
                # Prepare AI request
                ai_message = chat([
                    SystemMessage(content=analysis_prompt),
                    HumanMessage(content=f"Image Caption: {caption}\nImage URL: {image_url}")
                ])
                
                # Step 4: Display AI response
                st.write(f"AI Analysis: {ai_message.content}")
            else:
                st.warning("Please provide a caption for the image.")
