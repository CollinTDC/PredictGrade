import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(page_title="Questionnaire", layout="wide")

# Title and disclaimer how the questionnaire is structured.
st.title("Questionnaire")
st.write("To calculate your grade for the upcoming semester, please complete the questionnaire.")
st.write("The questionnaire is divided into the following four sections:")
st.write(" - Personal Information")
st.write(" - Academic Information")
st.write(" - Activities")
st.write(" - Parental Support & Education")

st.write("*Filling out the questionnaire will take approximately 5 to 10 minutes.*")

st.markdown("---")

# First section: Personal Information to extract first relevant data for the subsequent grade calculation.
st.subheader("Personal Information")
gender = st.radio("1. What is your gender?", ["Male", "Female"])
gender_mapping = {"Male": 0, "Female": 1}
gender_numeric = gender_mapping[gender]

# Because our target group are students between 15 and 18 years, the slider can be used to select an age in that range. Default is 15.
age = st.slider("2. How old are you?", 15, 18, 15)

# Second section: Academic Information to get data about the average study time per week, absences, tutoring, as well as the current GPA of the student.
st.subheader("Academic Information")
# Slider for the selection of the average study time per week. Default is 0, values between 0-25 hours can be selected.
average_time = st.slider("3. On average, how many hours per week do you study outside of the classroom? ⚠️ *Please use the last 6 months of school as a reference!*", 0, 25, 0)

# Slider to determine the number of days the student was absent from school in the last 6 months. Default is 0, values between 0-30 days can be chosen.
# The space of 6 months was chosen because this gives us an adequate indicator about how often a student usually misses class.
absences = st.slider("4. How many days were you absent from school in the last 6 months?", 0, 30, 0)

# Yes/No question with radio buttons to get to know if the student claimed tutoring in the last 6 months.
tutoring = st.radio("5. Have you received any tutoring in the last 6 months? Parental support is not included", ["Yes","No"])
tutoring_mapping = {"Yes": 1, "No": 0}
tutoring_numeric = tutoring_mapping[tutoring]

# Slider to get to know about the students GPA. Grades between 1 and 6 can be chosen, the step size is defined at 0.05.
# The GPA represents our questionnaire's most relevant input factor for the grade calculation.
performance = st.slider("6. What is your current grade? ⚠️ *You can use your average grade from the last semester as a reference!*", min_value=1.0, max_value=6.0, step=0.05)

# Third section: Activities besides school. This helps us in order to extract more than just school-related data.
# Multiselector to select all extracurricular activities one participates in.
st.subheader("Extracurricular Activities")
activities = st.multiselect(
    "7. Which activities do you participate in? ⚠️ *You can choose up to 4!*",
    ["Sports", "Music", "Volunteering", "Other Extracurricular Activities (Theatre, Arts, etc.)"]
)
sports = int("Sports" in activities)
music = int("Music" in activities)
volunteering = int("Volunteering" in activities)
extracurricular = int("Extracurricular Activities" in activities)

# Fourth section: Questions about Parental Support & Education, which also has influence on the students performance in school.
# Selectbox to rate the support the student gets from his parents regarding academic purposes. Ranging from No support to Very high support.
# The chosen support level will then be mapped to numbers. This is to make the grade calculation and data visualization easier to implement.
st.subheader("Parental Support & Education")
support = st.selectbox(
    "8. Rate the support from your parents:", 
    ["No support", "Low", "Moderate", "High", "Very high"]
)
support_mapping = {"No support": 0, "Low": 1, "Moderate": 2, "High": 3, "Very high": 4}
support_numeric = support_mapping[support]

# Radio buttons to determine the parents highest achieved degree.
# Again, the selected option is mapped to numbers for data analysis and visualization.
parental_degree = st.radio(
    "9. What is the highest education level your parents completed? ⚠️ *If your parents have different levels of education, please indicate the higher level of education!*", 
    ["No degree", "High School/Apprenticeship", "Bachelor's", "Master's", "PhD"]
)
degree_mapping = {"No degree": 0, "High School": 1, "Bachelor's": 2, "Master's": 3, "PhD": 4}
parental_degree_numeric = degree_mapping[parental_degree]

# Save inputs in order to make a prediction about the students grade.
st.session_state.responses = [
    age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, 
    support_numeric, extracurricular, sports, music, volunteering, performance
]

if st.button("Get results"):
    switch_page("Report")
