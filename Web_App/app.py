import streamlit as st
import time
import pandas as pd
import psycopg2

# Set the title of the web app
st.title('Singapore Job Market Insights')

# Add a brief description of the project
st.write('Welcome to the Singapore Job Market Insights Web Application! Get personalised job recommendations and explore key trends, skill demand, and salary ranges in the Singapore job market.')

st.divider()

# Function for loading data from the database
def load_data(load_file_path='test.csv'):
    select_table_query = """SELECT * FROM consolidatedJobs"""
    conn = psycopg2.connect(database="is3107JobsDB", user='is3107Postgres', password='JobsDBProject3107', host='is3107.postgres.database.azure.com', port='5432')
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(select_table_query)
    result = cursor.fetchall()
    conn.close()
    colnames = ['job_title', 'description', 'company', 'salary_range']
    pd.DataFrame(result, columns=colnames).to_csv(load_file_path)
    return pd.DataFrame(result, columns=colnames)

# Function for displaying job recommendation page
def display_job_recommendation_page():
    st.title('Job Recommendation')
    st.write('Input your resume details and receive personalised job recommendations.')

    # Load data from the database
    job_data = load_data()

    # Display job data to the user
    st.write(job_data)

    # For user to input resume details
    resume_details = st.text_area("Resume Details", key='resume_details_input')

    if st.button("Submit"):
        # Display status indicator while retrieving job recommendations
        with st.spinner("Retrieving job recommendations..."):
            # Simulate time-consuming process
            time.sleep(5)

            # Run NLP and ML models to process user input and return job results
            # ...


            # Display job recommendations to the user
            st.write("Job recommendations retrieved successfully!")

            # Clear the text area after submit button is clicked
            # ...


# Function for displaying dashboard page
def display_dashboard_page():
    st.title('Dashboard')
    st.write('Visualisations and insights about the Singapore job market.')

    st.header('Job Trends')
    st.subheader('Explore the latest job trends in Singapore')

    # Add visualizations and insights on job trends
    # ... 

    st.header('Skill Demand')
    st.subheader('Discover in-demand skills across industries')

    # Add visualizations and insights on job trends
    # ... 

    st.header('Popular Job Titles')
    st.subheader('Find out the most popular job titles in Singapore')

    # Add visualizations and insights on job trends
    # ... 

    st.header('Salary Ranges')
    st.subheader('Explore salary ranges across different industries')

    # Add visualizations and insights on job trends
    # ... 

# Create navigation sidebar
st.sidebar.title('Singapore Job Market Insights')
page = st.sidebar.radio('Navigation', ['Job Recommendation', 'Dashboard'])

st.sidebar.write(""" 
                 ## About
                 The Singapore Job Market Insights is an interface designed to enable users to explore the job landscape in Singapore comprehensively, gaining insights into job trends, skill demand, salary ranges, and popular job titles across industries. 
                   
                 This serves as a valuable resource for job seekers, hiring managers, and career planners, providing them with real-time market dynamics to make informed decisions.
                 """)

# Display selected page
if page == 'Job Recommendation':
    display_job_recommendation_page()
elif page == 'Dashboard':
    display_dashboard_page()