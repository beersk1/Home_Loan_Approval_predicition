import streamlit as st
import os 

script_directory = os.path.dirname(__file__)
html_file_path = os.path.join(script_directory, "..", "my_report.html")

# Read the HTML content from the file
with open(html_file_path, "r",encoding="utf-8") as file:
    
    html_content = file.read()



# Display the HTML content
st.components.v1.html(html_content, width=1000, height=1500)