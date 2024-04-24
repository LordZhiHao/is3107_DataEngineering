import streamlit as st
import time
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt 
import altair as alt 

# Set the title of the web app
st.title('Singapore Job Market Insights')

# Add a brief description of the project
st.write('Welcome to the Singapore Job Market Insights Web Application! Get personalised job recommendations and explore key trends, skill demand, and salary ranges in the Singapore job market.')

st.divider()

def load_data(load_file_path):
        select_table_query = """SELECT * FROM consolidatedJobs"""
        conn = psycopg2.connect(database="is3107JobsDB", user='is3107Postgres', password='JobsDBProject3107', host='is3107.postgres.database.azure.com', port= '5432')
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(select_table_query)
        result = cursor.fetchall()
        print(result)
        conn.commit()
        conn.close()        
        colnames = ['job_title', 'description', 'company', 'salary_range', 'url']
        pd.DataFrame(result, columns=colnames).to_csv(load_file_path)
        return pd.DataFrame(result, columns=colnames)

def preprocess_job_title(title):
    title = title.strip()  
    return title

def map_company_name(name):
    company_mapping = {
        'SHOPEE SINGAPORE PRIVATE LIMITED': 'Shopee',
        'TIKTOK PTE. LTD.': 'TikTok',
        'Hays Specialist Recruitment Pte Ltd': 'Hays',
        'ComfortDelGro Transportation': 'Comfort Transportation Pte Ltd',
        'THE SOFTWARE PRACTICE PTE. LTD.': 'The Software Practice',
        'Univers Pte Ltd': 'Univers',
        'PERSOLKELLY SINGAPORE PTE. LTD.': 'PERSOLKELLY',
        'PERSOLKELLY Singapore': 'PERSOLKELLY'
    }
    return company_mapping.get(name, name) 

jobs_data = load_data('database.csv')

# Function for displaying job recommendation page
def display_job_recommendation_page():
    st.title('Job Recommendation')
    st.write('Input your resume details and receive personalised job recommendations.')

    # For user to input resume details
    resume_details = st.text_area("Resume Details", key='resume_details_input')

    if st.button("Submit"):
        # Display status indicator while retrieving job recommendations
        with st.spinner("Retrieving job recommendations..."):
            # Load data from the database
            job_data = load_data('database.csv')

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

    #Load data from the database
    job_data = load_data('database.csv')

    # Preprocess and map company names
    job_data['company'] = job_data['company'].apply(map_company_name)

    st.header('Top 10 Companies Hiring')
    st.subheader('Explore the leading employers in Singapore')

    # Top 10 Companies
    top_10_companies = job_data['company'].value_counts().head(10).sort_values(ascending=True)
    top_10_companies_df = pd.DataFrame({'Company': top_10_companies.index, 'Number of Job Postings': top_10_companies.values})

    chart = alt.Chart(top_10_companies_df).mark_bar().encode(
        y=alt.Y('Company:N', sort='-x'),
        x='Number of Job Postings:Q'
    ).properties(
        height=400
    )
    st.altair_chart(chart, use_container_width=True)

    # Preprocess job titles
    job_data['job_title'] = job_data['job_title'].apply(preprocess_job_title)

    st.divider()

    st.header('Popular Job Titles')
    st.subheader('Find out the most popular job titles in Singapore')

    # Most Common 15 Job Titles
    job_title_counts = job_data['job_title'].value_counts().head(10).reset_index()
    job_title_counts.columns = ['Job Title', 'Count']

    chart = alt.Chart(job_title_counts).mark_bar().encode(
        y=alt.Y('Job Title:N', sort='-x'),
        x='Count:Q'
    ).properties(
        height=400
    )
    st.altair_chart(chart, use_container_width=True)

    st.divider()

    st.header('Salary Ranges')
    st.subheader('Explore salary ranges across different industries')

    salary_ranges = job_data['salary_range'].value_counts().head(10).reset_index()
    salary_ranges.columns = ['Salary Range', 'Count']
    salary_ranges = salary_ranges[salary_ranges['Salary Range'] != 'Null']

    chart = alt.Chart(salary_ranges).mark_bar().encode(
        y=alt.Y('Salary Range:N', sort='-x'),
        x='Count:Q'
    ).properties(
        height=400
    )
    st.altair_chart(chart, use_container_width=True)

    st.divider()

    st.header('Custom Tailor Analysis')
    st.subheader('Visualize specific company and job title')

    job_data['company'] = job_data['company'].apply(map_company_name)

    # Create dropdown for selecting company
    selected_company = st.selectbox('Select Company', job_data['company'].unique())
    filtered_data = job_data[job_data['company'] == selected_company]

    # Create dropdown for selecting job title
    selected_job_title = st.selectbox('Select Job Title', filtered_data['job_title'].unique())
    filtered_data = filtered_data[filtered_data['job_title'] == selected_job_title]

    st.write(filtered_data)

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