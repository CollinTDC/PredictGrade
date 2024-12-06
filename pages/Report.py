
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from joblib import load

# Initialize session state for responses
if 'responses' not in st.session_state:
    st.session_state.responses = None  # Default to None if not filled out yet

# Display report section only if responses are available
if st.session_state.responses:
    try:
        # Retrieve responses from session state
        age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, performance = st.session_state.responses

    except ValueError:
        # Handle error if unpacking fails (e.g., the list doesn't have 12 elements)
        st.error("Error: Incorrect number of responses or malformed data.")
else:
    # Message if the questionnaire has not been completed
    st.warning("Please complete the questionnaire to view your report.")
