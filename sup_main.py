import streamlit as st
from sup_analysis import ana
from sup_predection import pred
st.set_page_config(page_title='Superstore')

st.header("Superstore Sales Predictions & Analytics")
sel = st.sidebar.radio("Select a Page",('Analysis', 'Predection'))

if sel=='Analysis':
    ana()
elif sel=='Predection':
    pred()