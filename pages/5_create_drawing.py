import streamlit as st
from streamlit_drawable_canvas import st_canvas
import os
from PIL import Image
import io

# Set up the page configuration
st.set_page_config(page_title="Create Drawing", page_icon="🎨")

st.title("Create and Save Your Drawing")

# Create a sidebar for the drawing tools
stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Stroke color hex: ", "#000000")
bg_color = st.sidebar.color_picker("Background color hex: ", "#ffffff")
drawing_mode = st.sidebar.selectbox(
    "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform")
)
realtime_update = st.sidebar.checkbox("Update in realtime", True)

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    update_streamlit=realtime_update,
    height=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

# Save the drawing as an image file
filename = st.text_input("Enter filename for image:")
if canvas_result.image_data is not None and filename:
    # Convert the drawing to an image
    image = Image.fromarray(canvas_result.image_data)
    buffer = io.BytesIO()
    image.save(buffer,format="PNG")
    byte_data = buffer.getvalue()
    filepath = os.path.join("content", "images", filename) +  '.png'
    # Use st.download_button to let users download the prepared file
    st.download_button(
        label="Download Image",
        data=byte_data,
        file_name=filepath,
        mime="application/json",
    )
    st.success("Click the download button to save the image to your local machine!")
else:
    st.error("No drawing to save!")

st.write("Use the tools in the sidebar to create your drawing. When you're ready, click 'Download Image' to save your artwork.")