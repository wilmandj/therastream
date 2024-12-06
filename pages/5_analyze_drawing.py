"""
Analyze Drawing Page

This script facilitates the upload and analysis of drawings by interpreting 
them as expressions of the subject's subconscious mind. It combines image 
captions with system prompts for psychological analysis and displays AI 
responses.

**Image Analysis:**
   - The image analysis appears to only utilize captions, with the actual image data not being processed meaningfully. This is noted in the comments but should be addressed for complete functionality.

"""

import streamlit as st
import os
from PIL import Image
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.messages import HumanMessage as HumanMessage_core
import base64
from io import BytesIO

chat = st.session_state.get("chat", None)

if chat is None:
    st.warning("Please connect to OpenAI on the Connect page to access functionality.")
else:
    st.header("Analyse Drawing")

    # Step 1: Upload an image
    uploaded_file = st.file_uploader("Upload an image (e.g., jpg, png)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Drawing", use_column_width=True)

        # Check and resize image if necessary
        max_size = (512, 512)  # Define a maximum size for the model
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image = image.resize(max_size, Image.LANCZOS)  # Use LANCZOS for high-quality downsampling
            st.info(f"Image resized to {max_size} for processing.")
        
        # Convert image to base64 string
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Step 2: Provide a caption/description
        caption = st.text_input("Provide a caption or description for the image:")
        
        # Step 3: Analyze the image and caption
        if st.button("Analyze Drawing"):
            if caption:
                # Combine system prompts
                language_toggle = st.radio("Select Language", ("English", "German"), index=0)
                current_prompt = st.session_state.system_prompt[language_toggle]
                analysis_prompt = (
                    f"""{current_prompt} You are an expert in psychological analysis. 
                    Interpret the drawing as an expression of the subject's subconscious mind. 
                    Analyze the drawing and caption to provide insights into the subject's state of mind.
                    Make sure to pay attention to - and highlight - elements in the drawing which emphasize 
                    and which go beyond the content of the caption.
                    """
                )
                
                # Prepare AI request
                # Note: currently not actually analysing the image itself, just the caption. Needs a url
                ai_message = chat([
                    SystemMessage(content=analysis_prompt),
                    HumanMessage(content=f"Image Caption: {caption}\nImage Data: {img_str}")
                ])
                
                # Step 4: Display AI response
                st.write(f"AI Analysis: {ai_message.content}")
            else:
                st.warning("Please provide a caption for the image.")