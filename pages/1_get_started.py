# Import necessary libraries
import streamlit as st

# Function to read the README file
def read_markdown_file():
    with open("README.md", "r", encoding="utf-8") as file:
        return file.read()

# Main function to render the README
def main():
    # Set the page title
    st.set_page_config(page_title="README Viewer", layout="wide")

    # Read and display the markdown content
    readme_content = read_markdown_file()
    st.markdown(readme_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()