
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from joblib import load

st.set_page_config(page_title="Report", layout="wide")

st.title("Analysis of Results")
st.markdown("---")


# api to display current date

url = "http://worldtimeapi.org/api/timezone/Etc/UTC"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    data = response.json()
    today_date = data.get("datetime", "").split("T")[0]

except requests.RequestException as e:
    print(f"An error occurred while fetching the date: {e}")
except ValueError:
    print("Error decoding JSON response. Please check the API response format.")



# Initialize session state for responses
if 'responses' not in st.session_state:
    st.session_state.responses = None  # Default to None if not filled out yet

# Display report section only if responses are available
if st.session_state.responses:
    try:
        # Retrieve responses from session state
        age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, performance = st.session_state.responses

        st.subheader(f"Report of {today_date}")
        st.write("Below is a comparison of your inputs against the overall average (see Figure 1) and your predicted grade based on your inputs (see Figure 2).")
        st.write("")
        st.write("")
    except ValueError:
        # Handle error if unpacking fails (e.g., the list doesn't have 12 elements)
        st.error("Error: Incorrect number of responses or malformed data.")
else:
    # Message if the questionnaire has not been completed
    st.warning("Please complete the questionnaire to view your report.")
