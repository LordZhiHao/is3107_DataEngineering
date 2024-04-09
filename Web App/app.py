import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string


# Set the title of the web app
st.title('Singapore Job Market Insights')

# Add a brief description of the project
st.write('Welcome to the Singapore Job Market Insights Web Application! Get personalised job recommendations and explore key trends, skill demand, and salary ranges in the Singapore job market.')

st.divider()

# Function to read CSV data
def read_csv_data(file_path):
    data = pd.read_csv(file_path)
    return data

csv_file_path = r"C:\Users\jorda\Downloads\IS3107\is3107_DataEngineering\consolidated.csv"

data = read_csv_data(csv_file_path)

# Function for displaying job recommendation page
def display_job_recommendation_page():
    st.title('Job Recommendation')
    st.write('Input your resume details and receive personalised job recommendations.')

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

    st.header('Top 10 Companies Hiring')
    st.subheader('Discover the companies with the highest number of job listings in the Singapore job market')

    plt.figure(figsize=(12, 8))
    data['company'].value_counts().head(10).plot(kind='bar', color='lightblue')
    plt.xlabel('Company')
    plt.ylabel('Frequency')
    plt.title('Top 10 Companies Hiring')
    st.pyplot(plt)

    st.header('Job Description Insights')
    st.subheader('Discover prevalent keywords used by employers for job descriptions')

    # Convert all job descriptions to lowercase
    data['description'] = data['description'].astype(str).str.lower()

    # Tokenization and removal of punctuation
    data['description'] = data['description'].apply(lambda x: ' '.join(word_tokenize(x.translate(str.maketrans('', '', string.punctuation)))))

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    data['description'] = data['description'].apply(lambda x: ' '.join([word for word in word_tokenize(x) if word not in stop_words]))

    # Concatenate all job descriptions into a single string
    concatenated_descriptions = ' '.join(data['description'])

    wordcloud = WordCloud(width=800, height=400).generate(concatenated_descriptions)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)

    st.header('Popular Job Titles')
    st.subheader('Find out the most popular job titles in Singapore')

    plt.figure(figsize=(12, 8))
    data['job title'].value_counts().head(15).plot(kind='bar', color='lightblue')
    plt.xlabel('Job Title')
    plt.ylabel('Frequency')
    plt.title('Top 15 Job Titles')
    st.pyplot(plt)

    st.header('Salary Ranges')
    st.subheader('Explore salary ranges across different industries')

    plt.figure(figsize=(12, 8))
    data['salary range'].value_counts().head(10).plot(kind='bar', color='lightblue')
    plt.xlabel('Salary Range')
    plt.ylabel('Frequency')
    plt.title('Top 10 Common Salary Range')
    st.pyplot(plt)


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