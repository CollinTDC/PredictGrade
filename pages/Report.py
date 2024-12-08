
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from joblib import load
import requests
import os

st.set_page_config(page_title="Report", layout="wide")

st.title("Analysis of Results")
st.markdown("---")


# API to display current date, which is relevant if the student wants to track the progress of his predicted grades throughout the semester.

url = "http://worldtimeapi.org/api/timezone/Etc/UTC"

# This sends an HTTP-request to the URL in order to extract the actual date. If the request isn't succesful, an error message is displayed.
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

# If statement to display report section only if responses from the questionnaire are available
if st.session_state.responses:
    try:
        # Retrieve saved responses of the following questions from session state
        age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, performance = st.session_state.responses

        # Title of the report that will be displayed. Today's date will be extracted through the aforementioned API.
        # The radar-chart will display the saved responses from the questionnaire and compare the responses to the overall average of each factor.
        st.subheader(f"Report of {today_date}")
        st.write("Below is a comparison of your inputs against the overall average (see Figure 1) and your predicted grade based on your inputs (see Figure 2).")
        st.write("")
        st.write("")
        st.markdown("<h5 style='font-size: 20px;'>Deviation From Averages</h5>", unsafe_allow_html=True)

        # Generate a table with 2 columns
        col1, col2 = st.columns(2)

        with col1:

            st.write("Figure 1: Inputs vs. overall average")

            # Initialize session state for responses
            if 'responses' not in st.session_state:
                st.session_state.responses = None  # Default to None if not filled out yet

            # Radar chart logic
            try:
                if st.session_state.responses:
                    try:
                        # Retrieve responses from session state
                        age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, performance = st.session_state.responses
                    except ValueError:
                        # Handle error if unpacking fails (e.g., the list doesn't have 12 elements)
                        st.error("Error: Incorrect number of responses or malformed data.")
                        st.stop()  # Stop execution if the responses are malformed

                    # User's values based on their inputs
                    user_values = [age, parental_degree_numeric, average_time, absences, support_numeric, tutoring_numeric, performance, sports, music, volunteering, extracurricular]





                    # Define categories (these are based on the questions in the questionnaire) and Min/Max values
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
                else:
                    st.warning("Please fill out the questionnaire first.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")


        with col2:

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


            # Initialize session state for button click
            if 'show_table' not in st.session_state:
                st.session_state['show_table'] = False

            # Button
            if st.button("Table 1: Differences between inputs and average values"):
                st.session_state['show_table'] = not st.session_state['show_table']

            if st.session_state['show_table']:
                st.table(df_differences.set_index('Feature'))
            else:
                st.info("Click the button to display the table.")



        st.markdown("<h5 style='font-size: 20px;'>Grade Prediction</h5>", unsafe_allow_html=True)


        # Here, we again create two colums that will be displayed side by side.
        # The columns represent the data that is subsequently used to create a pie chart.
        col3, col4 = st.columns(2)

        # We start working in the left column (col3)
        with col3:
            # The title of the chart is added for increased overview.
            st.write("Figure 2: Predicted probabilities of grades")

            # This if-statement is added to check check if the user has completed the questionnaire and the responses are saved in session state.
            if st.session_state.responses:
                try:
                    # Here, we try to retrieve responses from session state.
                    # Each variable correspondends to a specific question in the questionnaire.
                    age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, performance = st.session_state.responses

                    # We define a function in order to convert swiss grades to US grades (4-scale-GPA) to comply with our API.
                    
                    def swiss_to_us_gpa(swiss_grade):
                        return 2 + ((swiss_grade - 1) / 5) * 2

                    swiss_grade = performance  # Example Swiss grade
                    us_gpa = swiss_to_us_gpa(swiss_grade) # Here, the conversion ultimately takes place

                    scaler = load('scaler.pkl')  # Make sure to load the correct scaler (used during training)

                    # Step 1: We create a new input data array for predictions
                    # The model expects 12 features, so we ensure all features are included
                    new_data = np.array([
                        [age, gender_numeric, parental_degree_numeric, average_time, absences, tutoring_numeric, support_numeric, extracurricular, sports, music, volunteering, us_gpa]
                    ])

                    # Step 2: The scaling to new data is applied(using the previously fitted scaler)
                    new_data_scaled = scaler.transform(new_data)  # Use transform to scale new data without fitting again

                    # Step 3: If the pre-trained model is saved, we load define a new function to load it
                    # The model file is reassembled from chunks
                    def reassemble_file(output_file, chunk_files):
                        with open(output_file, 'wb') as output:
                            for chunk_file in chunk_files:
                                with open(chunk_file, 'rb') as file:
                                    output.write(file.read())

                    # This is the list of model file chunks used to reassemble the model file
                    chunk_files = [
                        'random_forest_model.pkl.part0',
                        'random_forest_model.pkl.part1',
                        # Add other parts if applicable
                    ]
                    # The reassembly takes place to create the full model file
                    reassemble_file('random_forest_model.pkl', chunk_files)

                    # Our pre-trained random forest model is loaded
                    model = load('random_forest_model.pkl')  # Make sure to load the correct model

                    # Step 4: The random forest model is used to predict grades based on the scaled input data
                    predictions = model.predict(new_data_scaled)
                    probabilities = model.predict_proba(new_data_scaled)

                    # Step 5: The grades are mapped to new values: 0 -> 6, 1 -> 5, 2 -> 4, 3 -> 3, 4 -> 2
                    # Grades are mapped for better readability and more user-friendliness
                    grade_mapping = {0: "5.5-6", 1: "4.5-5", 2: 4, 3: "3-4", 4: "1-3"}

                    # Step 6: To increase contrast and ultimately user-friendliness, custom colors for the pie chart are defined
                    color_palette = ['#a3f0a3', '#c9f7c9', '#f4e1a1', '#f8b4b4', '#ff7373']  # The color palette ranges from light green to pastel red

                    # Step 7: The predictions and probabilities are used to create pie charts
                    import plotly.graph_objects as go

                    # Ultimately, we use plotly to create our pie chart
                    for i, (prediction, prob) in enumerate(zip(predictions, probabilities)):
                        
                        # Here, we map labels to grades to provide the user with better readability
                        mapped_labels = [f'Grade: {grade_mapping[j]}' for j in range(len(prob))]

                        # We find the grade with the highest probability according to data gathered in the questionnaire
                        max_prob_index = prob.argmax()  # Index of the highest probability
                        max_prob = prob[max_prob_index]  # The highest probability value
                        predicted_grade = grade_mapping[max_prob_index]  # The corresponding grade

                        # Now, we display the message with the highest probability grade
                        # Subsequently, the pie chart is created with the predicted probabilities per grade
                        fig = go.Figure(data=[go.Pie(
                            labels=mapped_labels,
                            values=prob,
                            textinfo='label+percent',
                            marker=dict(colors=color_palette),
                            hoverinfo='label+percent'
                        )])

                        # Now, the layout for better aesthetics
                        # Again, this is for increased user-friendliness
                        fig.update_layout(
                            showlegend=False,
                            height=380,  # Adjust the height of the chart
                            width=380,   # Adjust the width of the chart
                            margin=dict(t=20, b=20, l=20, r=20)  # Set margins for a cleaner look
                        )

                        # Now, the Plotly pie chart is displayed in Streamlit
                        st.plotly_chart(fig, use_container_width=True)


                # If something goes wrong, an error message is displayed.
                except Exception as e:
                    st.error(f"Error loading model or making predictions: {e}")
            else:
                st.warning("Please complete the questionnaire first!")


        # Now, we work in the right column (col4)
        with col4: 
            # This dictionary contains the features (input variables) used in the model and their corresponding importance 
            # The percentages show how much each feature contributes to the model's predictions
            # For example, the 'GPA' feature contributes 46.36%, which means it's the most important factor for the prediction,
            # 'Gender' on the orher hand only contributes 2.35%, making it less significant in the model's decision-making process
            data = {
                'Feature': ['Age', 'Gender', 'ParentalEducation', 'StudyTimeWeekly', 'Absences', 
                            'Tutoring', 'ParentalSupport', 'Extracurricular', 'Sports', 'Music', 
                            'Volunteering', 'GPA'],
                'Importance (%)': [4.71, 2.35, 4.61, 6.88, 19.69, 2.68, 6.28, 2.03, 2.01, 1.37, 1.02, 46.36]
            }

            # The data is converted into a DataFrame


            # If the button is clicked, session state is initialized
            if 'show_table1' not in st.session_state:
                st.session_state['show_table1'] = False

            # This button allows the user to toggle the visibility of the "Feature Importance" table.
            # If 'show_table1' is True, the table is shown; if False, the table is hidden.
            # This provides an interactive way for the user to view or hide the table as needed.
            if st.button("Table 2: Feature Importance"):
                st.session_state['show_table1'] = not st.session_state['show_table1']

            if st.session_state['show_table1']:
                # The data is converted into a data frame and also sorted by importance (%) in descending order
                df = pd.DataFrame(data)
                df_sorted = df.sort_values(by='Importance (%)', ascending=False)

                # Here, the DataFrame is formatted to display one decimal point for easier readability
                df_formatted = df_sorted.set_index('Feature').style.format("{:.1f}", subset=['Importance (%)'])

                # Ultimately, the formatted table is displayed in Streamlit
                st.table(df_formatted)

            else:
                # The user is informed that he can click the button to display the full table
                # The table is not displayed by default for aesthetic reasons
                st.info("Click the button to display the table.")

        # Now, we display the final prediction and explain how the prediction is calculated
        # This is tho show the user that the grade prediction is not random, but based on his data
        st.write(f"Based on the provided inputs, the model predicts a {max_prob:.1%} likelihood that your grade will be {predicted_grade}. This prediction is derived from an extensive analysis of historical performance data. Each feature contributes differently to predicting your grade. Focus on improving the most impactful ones for better results. Our tests show that the model achieves an accuracy of 91.02%, indicating a strong ability to predict outcomes reliably.")


    # If something goes wrong, the user is provided with an error message
    except ValueError:
        # Handle error if unpacking fails (e.g., the list doesn't have 12 elements)
        st.error("Error: Incorrect number of responses or malformed data.")

# If the questionnaire has not been completed correctly, the user is informed that all questions must be answered in order to get a report
else:
    st.warning("Please complete the questionnaire to view your report.")


st.markdown("---")

st.subheader("Save Report")
# Display the email input field where the user can write his preferred email-adress.
# We want to send a email with the user's predicted grade so that he/she can track the progress of the predicted grades over the semester.
# The API being used here is from SendGrid, which is a service for sending emails.
# The URL of the API is not written directly in the code.
# Instead, the SendGrid Python library (SendGridAPIClient) takes care of this.
# The library sends the request to the SendGrid URL "https://api.sendgrid.com/v3/mail/send" in the background.
# We only need to provide the API key and the email details, and the library handles the rest.
email = st.text_input("Please enter your email address to save your report.")

st.write(os.getenv("MAIL_API"))
# The 'Submit' button is displayed.
# As soon as the user wants to receive the mail with the predicted grade, he/she can press the 'Submit' button.
# This triggers the delivery of the email through the SendGrid API.
if st.button("Submit"):
    if email:

        # Here, we import the SendGridAPIClient class from the SendGrid python library.
        # This is needed for the subsequent dispatch of the email via SendGrid API.
        # Additionally, the Mail class from the helper modules of SendGrid is imported.
        # The Mail class is used to create an email message.
        # It can be used to define the sender, recipient, subject, and content of the email that is sent.
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        # The SendGrid API-Key is retrieved from an environment variable.
        # Environment variables are stored in the operating system.
        # This way, the API key is not written directly in the code.
        # This was necessary because SendGrid would delete the API-Key if it was exposed publicly.
        # The API-Key will be stored in the streamlit cloud and will be retrieved from there in order to successfully send the email.
        SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")  
        
        # Here, a new function in order to send the email is defined.
        # It contains information about the sending email address, the receiver, subject and content of the email.
        def send_email(user_email, note):
            message = Mail(
                from_email='gradeboostapp@gmail.com',  # The mail is sent from our own GradeBoost email-address.
                to_emails=email,
                subject='Deine prognostizierte Note',
                html_content=f'''<strong>Deine prognostizierte Note beträgt: {note}</strong>
                            <br><br>
                            Danke, dass du GradeBoost🚀 nutzt!'''
            )
            try:
                # The API-Key is used to create an instance of the SendGrid API.
                sg = SendGridAPIClient(SENDGRID_API_KEY)
                
                # The send method is called to send the email with all the information stored in the variable message.
                response = sg.send(message)

                # If the email is sent succesfully, the following message is displayed.
                # If the email can't be sent, an error message is displayed.
                st.write(f"E-Mail erfolgreich gesendet! Status Code: {response.status_code}")
            except Exception as e:
                st.write(f"Fehler beim Senden der E-Mail: {e}")
        
        # The email function is called and triggers the dispatch of the email.
        send_email(email, predicted_grade)

    else:
        st.write("Please enter an email address.")

