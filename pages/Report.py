
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from joblib import load


st.set_page_config(page_title="Report", layout="wide")

st.title("Analysis of Results")


st.markdown("---")

import requests

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

    # Categories and Min/Max values
    categories = [
        "Age", 
        "Parental Education", 
        "Weekly Study Time", 
        "Absences", 
        "Parental Support",
        "Tutoring",
        "GPA",
        "Sports",
        "Music",
        "Volunteering",
        "Extracurricular Activities"
    ]

    # Define min and max values for each category
    min_values = {
        "Age": 15, 
        "Parental Education": 0, 
        "Weekly Study Time": 0, 
        "Absences": 0, 
        "Parental Support": 0,
        "Tutoring": 0,
        "GPA": 1,
        "Sports": 0,
        "Music": 0,
        "Volunteering": 0,
        "Extracurricular Activities": 0
    }

    max_values = {
        "Age": 18, 
        "Parental Education": 4, 
        "Weekly Study Time": 25, 
        "Absences": 30, 
        "Parental Support": 4,
        "Tutoring": 1,
        "GPA": 6,
        "Sports": 1,
        "Music": 1,
        "Volunteering": 1,
        "Extracurricular Activities": 1
    }

    # Average values for comparison (you can adjust these based on your data)
    average_values = [16.46864548, 1.746237458, 9.771991919, 14.54138796, 2.122074, 0.301421, 4, 0.303512, 0.196906, 0.157191, 0.383361]

    if st.session_state.responses:
        try:
            # Retrieve responses from session state
            age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, performance = st.session_state.responses
        except ValueError:
            # Handle error if unpacking fails (e.g., the list doesn't have 12 elements)
            st.write("Error: Incorrect number of responses or malformed data.")
    else:
        st.write("Please fill out the questionnaire first.")


    # User's values based on their inputs
    user_values = [age, parental_degree_numeric, average_time, absences, support_numeric, tutoring_numeric, performance, sports, music, volunteering, extracurricular]

    # Normalize the user values and the average values
    def normalize(value, category):
        return (value - min_values[category]) / (max_values[category] - min_values[category])

    # Apply normalization
    normalized_user_values = [normalize(value, category) for value, category in zip(user_values, categories)]
    normalized_average_values = [normalize(value, category) for value, category in zip(average_values, categories)]

    # Close the radar chart by adding the first category again
    categories += [categories[0]]
    normalized_user_values += [normalized_user_values[0]]
    normalized_average_values += [normalized_average_values[0]]

    # Create DataFrames for both user inputs and average values
    df_user = pd.DataFrame({
        'Category': categories,
        'Value': normalized_user_values,
        'Type': ['Your Inputs'] * len(categories)
    })

    df_average = pd.DataFrame({
        'Category': categories,
        'Value': normalized_average_values,
        'Type': ['Average'] * len(categories)
    })

    # Combine both DataFrames
    df_combined = pd.concat([df_average, df_user])

    # Plot radar chart using Plotly
    fig = px.line_polar(
        df_combined, 
        r='Value', 
        theta='Category', 
        color='Type', 
        line_close=True
    )

    # Customize radar chart appearance
    fig.update_layout(
        polar=dict(
            bgcolor="white",  
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            ),
            angularaxis=dict(
                visible=True
            )
        ),
    )

    # Set fill color for user input and average areas
    fig.update_traces(
        fill='toself',
        fillcolor="rgba(180, 180, 180, 0.4)",  
        line_color="gray",  
        selector=dict(name="Average")
    )

    fig.update_traces(
        fill='toself',
        fillcolor="rgba(225, 130, 180, 0.4)",  
        line_color="red",  
        selector=dict(name="Your Inputs")
    )

    # Display chart
    st.plotly_chart(fig, use_container_width=True)

# Second column: Additional content or prediction
with col2:

    import pandas as pd
    import streamlit as st
    st.write("Table 1: Differences between inputs and average values")

    # Average values (replace with your actual average values)
    average_values = [
        16.46864548,  # Age
        1.746237458,  # Parental Education
        9.771991919,  # Weekly Study Time
        14.54138796,  # Absences
        2.122074,     # Parental Support
        0.301421,     # Tutoring
        4,            # GPA
        0.303512,     # Sports
        0.196906,     # Music
        0.157191,     # Volunteering
        0.383361      # Extracurricular Activities
    ]

    # Categories corresponding to the average values
    categories = [
        "Age", 
        "Parental Education", 
        "Weekly Study Time", 
        "Absences", 
        "Parental Support",
        "Tutoring",
        "GPA",
        "Sports",
        "Music",
        "Volunteering",
        "Extracurricular Activities"
    ]

    # Assuming `age`, `parental_degree_numeric`, `average_time`, etc. are defined elsewhere in your code

    # Example inputs (replace with actual values from your user input)
    user_input_values = [
        age,  # Age
        parental_degree_numeric,  # Parental Education
        average_time,  # Weekly Study Time
        absences,  # Absences
        support_numeric,  # Parental Support
        tutoring_numeric,  # Tutoring
        performance,  # GPA
        sports,  # Sports
        music,  # Music
        volunteering,  # Volunteering
        extracurricular  # Extracurricular Activities
    ]

    # Calculate the differences from the average
    differences = [user_input_values[i] - average_values[i] for i in range(len(user_input_values))]

    # Create a DataFrame for displaying the differences
    df_differences = pd.DataFrame({
        "Feature": categories,
        "Difference from Average": differences
    })

    # Display the differences in a table on Streamlit
    st.table(df_differences.set_index('Feature'))

st.markdown("<h5 style='font-size: 20px;'>Grade Prediction</h5>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.write("Figure 2: Predicted probabilities of grades")

    if st.session_state.responses:
        try:
            # Retrieve responses from session state
            age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, performance = st.session_state.responses

            def swiss_to_us_gpa(swiss_grade):
                return 2 + ((swiss_grade - 1) / 5) * 2

            swiss_grade = performance  # Example Swiss grade
            us_gpa = swiss_to_us_gpa(swiss_grade)

            scaler = load('scaler.pkl')  # Make sure to load the correct scaler (used during training)

            # Correct the new_data to have 12 features in each row
            new_data = np.array([
                [age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, us_gpa]
                # Add more rows for prediction if needed
            ])

            # Step 2: Apply the scaling to new data (using the previously fitted scaler)
            new_data_scaled = scaler.transform(new_data)  # Use transform to scale new data without fitting again

            # Step 3: Load the pre-trained model (if it's saved)
            def reassemble_file(output_file, chunk_files):
                with open(output_file, 'wb') as output:
                    for chunk_file in chunk_files:
                        with open(chunk_file, 'rb') as file:
                            output.write(file.read())

            chunk_files = [
                'random_forest_model.pkl.part0',
                'random_forest_model.pkl.part1',
                # Add other parts if applicable
            ]
            reassemble_file('random_forest_model.pkl', chunk_files)

            model = load('random_forest_model.pkl')  # Make sure to load the correct model

            # Step 4: Make predictions using the trained model
            predictions = model.predict(new_data_scaled)
            probabilities = model.predict_proba(new_data_scaled)

            # Step 6: Mapping grades to new values: 0 -> 6, 1 -> 5, 2 -> 4, 3 -> 3, 4 -> 2
            grade_mapping = {0: "5.5-6", 1: "4.5-5", 2: 4, 3: "3-4", 4: "1-3"}

            # Step 7: Custom color palette: white -> gray -> red
            color_palette = ['#a3f0a3', '#c9f7c9', '#f4e1a1', '#f8b4b4', '#ff7373']  # From light green to pastel red

            # Step 8: Output the predictions and probabilities and create pie charts
            import plotly.graph_objects as go

            # Create the pie chart using Plotly
            for i, (prediction, prob) in enumerate(zip(predictions, probabilities)):
                
                # Map the grade labels
                mapped_labels = [f'Grade: {grade_mapping[j]}' for j in range(len(prob))]

                # Get the highest probability and the corresponding grade
                max_prob_index = prob.argmax()  # Index of the highest probability
                max_prob = prob[max_prob_index]  # The highest probability value
                predicted_grade = grade_mapping[max_prob_index]  # The corresponding grade

                # Display the message with the highest probability grade
                # Create the pie chart
                fig = go.Figure(data=[go.Pie(
                    labels=mapped_labels,
                    values=prob,
                    textinfo='label+percent',
                    marker=dict(colors=color_palette),
                    hoverinfo='label+percent'
                )])

                # Update the layout for better aesthetics
                fig.update_layout(
                    showlegend=False,
                    height=380,  # Adjust the height of the chart
                    width=380,   # Adjust the width of the chart
                    margin=dict(t=20, b=20, l=20, r=20)  # Set margins for a cleaner look
                )

                # Display the Plotly pie chart in Streamlit
                st.plotly_chart(fig, use_container_width=True)


        except Exception as e:
            st.error(f"Error loading model or making predictions: {e}")
    else:
        st.warning("Please complete the questionnaire first!")


with col4: 
    st.write("Table 2: Feature importance")
    # Feature importances data
    data = {
        'Feature': ['Age', 'Gender', 'ParentalEducation', 'StudyTimeWeekly', 'Absences', 
                    'Tutoring', 'ParentalSupport', 'Extracurricular', 'Sports', 'Music', 
                    'Volunteering', 'GPA'],
        'Importance (%)': [4.71, 2.35, 4.61, 6.88, 19.69, 2.68, 6.28, 2.03, 2.01, 1.37, 1.02, 46.36]
    }

    # Convert the data into a DataFrame
    df = pd.DataFrame(data)

    # Sort the DataFrame by 'Importance (%)' in descending order
    df_sorted = df.sort_values(by='Importance (%)', ascending=False)
    st.table(df_sorted.set_index('Feature'))  # Set 'Feature' as the index and remove default index display

# Display the table in Streamlit without the index

st.write(f"Based on the provided inputs, the model predicts a {max_prob:.1%} likelihood that your grade will be {predicted_grade}. This prediction is derived from an extensive analysis of historical performance data. Each feature contributes differently to predicting your grade. Focus on improving the most impactful ones for better results. Our tests show that the model achieves an accuracy of 91.02%, indicating a strong ability to predict outcomes reliably.")




st.markdown("---")

st.subheader("Save Report")
# Display the email input field
email = st.text_input("Please enter your email address to save your report.")

import os

st.write(os.getenv("MAIL_API"))
# Display the button
if st.button("Submit"):
    if email:

        import os
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        # SendGrid API-Key
        SENDGRID_API_KEY = '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'  # Auf SendGrid generierter API-Key
        
        # Funktion, um eine E-Mail zu senden
        def send_email(user_email, note):
            message = Mail(
                from_email='gradeboostapp@gmail.com',  # Absenderadresse
                to_emails=email,
                subject='Deine prognostizierte Note',
                html_content=f'''<strong>Deine prognostizierte Note beträgt: {note}</strong>
                            <br><br>
                            Danke, dass du GradeBoost🚀 nutzt!'''
            )
            try:
                sg = SendGridAPIClient('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')
                response = sg.send(message)
                st.write(f"E-Mail erfolgreich gesendet! Status Code: {response.status_code}")
            except Exception as e:
                st.write(f"Fehler beim Senden der E-Mail: {e}")
        
        # Mail wird gesendet, indem die Funktion aufgerufen wird
        send_email(email, {predicted_grade})

    else:
        st.write("Please enter an email address.")
