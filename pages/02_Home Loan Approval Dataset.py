import streamlit as st 
import pandas as pd 

df = pd.read_csv(r".\homeloanapproval.csv")
def color_cells(val):
    if val == 'Y':
        return 'color: green'
    elif val == 'N':
        return 'color: red'
    else:
        return ''

styled_df = df.style.applymap(color_cells)

st.dataframe(styled_df,width = None,height = None)