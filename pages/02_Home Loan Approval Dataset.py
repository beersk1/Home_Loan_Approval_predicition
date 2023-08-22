import streamlit as st 
import pandas as pd
import os 

st.set_page_config(layout="wide")

script_directory = os.path.dirname(__file__)
df_file_path = os.path.join(script_directory, "..", "homeloanapproval.csv")


df = pd.read_csv(df_file_path)
def color_cells(val):
    if val == 'Y':
        return 'color: green'
    elif val == 'N':
        return 'color: red'
    else:
        return ''

styled_df = df.style.applymap(color_cells)

st.dataframe(styled_df,width = None,height = None)