
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

        # Report Section
        st.subheader(f"Report of {today_date}")
        st.write("Below is a comparison of your inputs against the overall average (see Figure 1) and your predicted grade based on your inputs (see Figure 2).")
        st.write("")
        st.write("")

        # Create two columns
        st.markdown("<h5 style='font-size: 20px;'>Deviation From Averages</h5>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        # First column: Visualization
        with col1:
            st.write("Figure 1: Inputs vs. overall average")
            # Radar chart logic here (use your existing radar chart code)

        # Second column: Additional content or prediction
        with col2:
            # Difference table and button logic here (use your existing logic for this)

        # Predicted Grades Section
        st.markdown("<h5 style='font-size: 20px;'>Grade Prediction</h5>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)

        with col3:
            st.write("Figure 2: Predicted probabilities of grades")
            # Prediction chart logic here (use your existing prediction logic)

        with col4:
            st.write("Table 2: Feature importance")
            # Feature importance logic here (use your existing logic)

        # Predicted Grade Summary
        st.write(f"Based on the provided inputs, the model predicts a {max_prob:.1%} likelihood that your grade will be {predicted_grade}. This prediction is derived from an extensive analysis of historical performance data. Each feature contributes differently to predicting your grade. Focus on improving the most impactful ones for better results. Our tests show that the model achieves an accuracy of 91.02%, indicating a strong ability to predict outcomes reliably.")

        st.markdown("---")

        # Save Report Section
        st.subheader("Save Report")
        email = st.text_input("Please enter your email address to save your report.")
        st.write(os.getenv("MAIL_API"))

        # Email submission logic
        if st.button("Submit"):
            if email:
                # Send email logic (use your existing logic here)
                pass
            else:
                st.write("Please enter an email address.")
    except ValueError:
        # Handle error if unpacking fails (e.g., the list doesn't have 12 elements)
        st.error("Error: Incorrect number of responses or malformed data.")
else:
    # Message if the questionnaire has not been completed
    st.warning("Please complete the questionnaire to view your report.")
