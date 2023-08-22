import streamlit as st

# Read the HTML content from the file
with open(r".\my_report.html", "r") as file:
    html_content = file.read()

# Display the HTML content
st.components.v1.html(html_content, width=1000, height=1500)