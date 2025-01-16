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
import base64
from io import BytesIO
from openai import OpenAI  # Updated import
from utils.session_utils import initialize_session_state

initialize_session_state()

language_toggle = st.sidebar.selectbox("Select Language", ("English", "German"), index=(st.session_state.language!='English'), key='language')
if language_toggle != st.session_state.language:
    st.session_state.language = language_toggle

chat = st.session_state.get("chat", None)

if chat is None:
    st.warning("Please connect to OpenAI on the Connect page to access functionality.")
else:
    st.title("🎨 Analyze Drawing")

    # Step 1: Upload an image
    uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png', 'bmp', 'gif'])

    # Step 2: Set maximum dimension for resizing
    max_dimension = st.number_input("Set maximum dimension for resizing (default is 512)", min_value=1, value=512)

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            # Convert to JPEG if necessary
            if image.format not in ['JPEG', 'JPG']:
                st.write(f"Converting {image.format} to JPEG format...")
                image = image.convert("RGB")  # Convert to RGB before saving as JPEG
                img_bytes = BytesIO()
                image.save(img_bytes, format='JPEG')
                img_bytes.seek(0)  # Rewind the file pointer to the beginning
                image = Image.open(img_bytes)
        
            # Resize image while maintaining aspect ratio
            max_size = (max_dimension, max_dimension)
            image.thumbnail(max_size, Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS

            try:
                st.image(image, caption="Uploaded Drawing", use_container_width=True)
            except:
                # old version:
                st.image(image, caption="Uploaded Drawing", use_column_width=True)
                
            # Convert image to base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    
            # Step 2: Provide a caption/description
            caption = st.text_input("Provide a caption or description for the image:")
            
            # Step 3: Analyze the image and caption
            if st.button("Analyze Drawing"):
                if caption:
                    # Prepare the request to OpenAI API
                    try:
                        # Initialize OpenAI client
                        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
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
                        
                        # Use the updated OpenAI client method
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {
                                    "role": "system",
                                    "content": analysis_prompt
                                },
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": f"Analyze this drawing and caption: {caption}"},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                    ]
                                }
                            ]
                        )
                        
                        # Step 4: Display AI response
                        st.write(f"AI Analysis: {response.choices[0].message.content}")
                    except Exception as e:
                        st.error(f"An error occurred during the analysis: {e}")
                else:
                    st.warning("Please provide a caption for the image.")

        except Exception as e:
            st.error(f"Error processing the image: {e}")
    
    else:
        st.write("Please upload an image file to proceed.")