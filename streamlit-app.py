import streamlit as st


sidebar = st.sidebar.selectbox(
    "Choose a page:",
    ["Home", "Questionnaire", "GitHub API"]
)

# Fragebogen-Daten speichern
if 'responses' not in st.session_state:
    st.session_state.responses = []
 
# Home-Seite
if sidebar == "Home":
    st.title("Welcome to GradeBoost! 🚀")
    st.header("Assess and boost your semester performance")
    st.markdown("""
    *Dear Student,*
    *We warmly welcome you to our website. Enter relevant factors and calculate your provisional grade for the semester.*
    *Good luck! 🍀*
    """)


# Fragebogen-Seite
elif sidebar == "Questionnaire":
    st.title("Questionnaire")
    st.write("Answer the following questions:")
 
    # Fragebogen mit verschiedenen Eingaben
    age = st.slider("1. How old are you?", 15, 18, 16)
    average_time = st.slider("2. How many hours per week do you study on average?", 0, 25, 12)
    tutoring = st.radio("3. Have you received tutoring?", ["Yes", "No"])
    absences = st.radio("4. How many days were you absent?", ["0-5 days", "6-10 days", "11-15 days", "16-20 days", "21-25 days", "more than 25 days"])
    performance_as = st.select_slider("5. Rate your academic performance:", ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0"])
    ex_activities = st.radio("6. Do you participate in extracurricular activities?", ["Yes", "No"])
 
    # Zusätzliche Auswahl bei extracurricular activities
    if ex_activities == "Yes":
        spec_ex_activities = st.multiselect("Which activities?", ["Sports", "Music", "Volunteering", "Other"])
        if "Other" in spec_ex_activities:
            other_activity = st.text_input("Specify other activities:")
 
    support = st.select_slider("7. Rate the support from your parents:", ["No support", "Low", "Moderate", "High", "Very high"])
    parental_degree = st.radio("8. What is the highest education level your parents completed?", ["No degree", "High School", "Bachelor's", "Master's", "PhD"])


import streamlit as st
import plotly.express as px
import pandas as pd


# Define average values (as in your provided example)
categories = [
    "Age", 
    "Parental Education", 
    "Study Time Weekly", 
    "Absences", 
    "Parental Support"
]
average_values = [16.46864548, 1.746237458, 9.771991919, 14.54138796, 2.122073579]

# Streamlit inputs for user data
st.title("Netzdiagram: Compare Your Inputs to the Average")

# Create a list of the user's values
user_values = [age, parental_degree, average_time, absences, support]

# Duplicate the first value to close the radar chart
categories += [categories[0]]
user_values += [user_values[0]]
average_values += [average_values[0]]

# Create the radar chart using Plotly
fig = px.line_polar(
    r=[*user_values, *average_values], 
    theta=categories,
    line_close=True
)

# Customize the radar chart
fig.update_layout(
    polar=dict(
        bgcolor="white",  # Background of the radar chart itself
    ),
)

# Set the fill color of the enclosed areas for both user input and average values
fig.update_traces(
    fill='toself',  # Fills the area inside the radar chart
    fillcolor="rgba(255, 99, 71, 0.4)",  # User input fill color (light red)
    line_color="red",  # User input outline color
    name="Your Inputs"
)

# Add the average values as a separate trace
fig.add_trace(
    px.line_polar(
        r=average_values,
        theta=categories,
        line_close=True
    ).data[0]
)
fig.update_traces(
    fill='toself',  # Fill the average area with a transparent color
    fillcolor="rgba(70, 130, 180, 0.3)",  # Average fill color (light blue)
    line_color="blue",  # Average outline color
    name="Average"
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)
