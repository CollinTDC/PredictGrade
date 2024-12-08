import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from joblib import load
import plotly.express as px
from streamlit_extras.switch_page_button import switch_page

#(API Reference/Configuration - Streamlit Docs)
st.set_page_config(page_title="Home", layout="wide")

#Session state to track and save responses
#This code checks if the key 'responses' exists in 'st.session_state'.
#If it doesn't, it initializes it as an empty list. This ensures that 'responses' is available for storing data during the session.
#(API Reference/Caching and state - Streamlit Docs)
if 'responses' not in st.session_state:
    st.session_state.responses = []

#Title, Header and Markdown containing strings to welcome users to our Web-Application. 
#At the bottom of the page, a button to navigate directly to the questionnaire is displayed, making the platform userfriendly to navigate.
#(API Reference/Text elements - Streamlit Docs)
st.title("Welcome to GradeBoost! 🚀")
st.header("Analyse and boost your semester performance")
st.markdown("""
*Dear Students and Teachers,*

*We warmly welcome you to our website. This website is designed for students aged 15 to 18 and their teachers living in Switzerland.*
*GradeBoost helps you identify areas where performance may be below average compared to others and provides valuable insights*
*and personalised tips to address these challenges.*
*Our mission is to guide you in continuously improving your performance and achieving a successful semester.*
*Good luck! 🍀*
""")

#(API Reference/Input Widgets/Navigation and pages - Streamlit Docs)
if st.button("Go to Questionnaire"):
    switch_page("questionnaire")
