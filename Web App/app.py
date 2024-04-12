import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import seaborn as sns


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
    data['company'].value_counts().head(10).sort_values(ascending=True).plot(kind='barh', color='lightblue')
    plt.xlabel('Frequency')
    plt.ylabel('Company')
    plt.title('Top 10 Companies Hiring')
    st.pyplot(plt)

    # st.header('Job Description Insights')
    # st.subheader('Discover prevalent keywords used by employers for job descriptions')

    # # Convert all job descriptions to lowercase
    # data['description'] = data['description'].astype(str).str.lower()

    # # Tokenization and removal of punctuation
    # data['description'] = data['description'].apply(lambda x: ' '.join(word_tokenize(x.translate(str.maketrans('', '', string.punctuation)))))

    # # Remove stopwords
    # stop_words = set(stopwords.words('english'))
    # data['description'] = data['description'].apply(lambda x: ' '.join([word for word in word_tokenize(x) if word not in stop_words]))

    # # Concatenate all job descriptions into a single string
    # concatenated_descriptions = ' '.join(data['description'])

    # wordcloud = WordCloud(width=800, height=400).generate(concatenated_descriptions)
    # plt.figure(figsize=(10, 5))
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')
    # st.pyplot(plt)

    st.header('Popular Job Titles')
    st.subheader('Find out the most popular job titles in Singapore')

    plt.figure(figsize=(12, 8))
    data['job title'].value_counts().head(15).sort_values(ascending=True).plot(kind='barh', color='lightblue')
    plt.xlabel('Frequency')
    plt.ylabel('Job Title')
    plt.title('Top 15 Job Titles')
    st.pyplot(plt)

    st.header('Salary Ranges')
    st.subheader('Explore salary ranges across different industries')

    plt.figure(figsize=(12, 8))
    data['salary range'].value_counts().head(10).sort_values(ascending=True).plot(kind='barh', color='lightblue')
    plt.xlabel('Frequency')
    plt.ylabel('Salary Range')
    plt.title('Top 10 Common Salary Range')
    st.pyplot(plt)

    st.divider()

    st.header('Tailor Your Analysis')
    st.subheader('Customize your view and delve deeper into the Singapore job market data')

    # Get unique companies and job titles
    unique_companies = data['company'].unique()

    # Create selectbox for company
    selected_companies = st.multiselect('Select Companies', unique_companies)

    # Filter job titles based on selected company
    if selected_companies:
        filtered_data = data[(data['company'].isin(selected_companies)) & (data['salary range'].notna())]

        # Get unique job titles from filtered data
        unique_job_titles = filtered_data['job title'].unique()

        # Create multiselect for job titles
        selected_job_titles = st.multiselect('Select Job Titles', unique_job_titles)

        # Filter data based on selected job titles
        if selected_job_titles:
            filtered_data = filtered_data[filtered_data['job title'].isin(selected_job_titles)]

            # Update visualizations based on filtered data
            # Example: Update bar chart for salary ranges
            plt.figure(figsize=(12, 8))
            ax = filtered_data['salary range'].value_counts().head(10).plot(kind='barh', color='lightblue')
            plt.xlabel('Frequency')
            plt.ylabel('Salary Range')
            plt.title(f'Salary Range for Selected Job Titles at Selected Companies')

            # Add text annotations to the bars
            for i, (index, value) in enumerate(filtered_data['salary range'].value_counts().head(10).items()):
                title = filtered_data['job title'].iloc[i]
                company = filtered_data['company'].iloc[i]
                ax.text(value + 0.1 * value, i, f'{title} ({company})', color='black', va='center')

            st.pyplot(plt)
    
    # st.header('Compare Salary Ranges Across Companies')
    # st.subheader('Visualize the distribution of salary ranges for a specific job title across different companies')

    # # Get unique job titles with at least two different companies
    # job_titles_with_multiple_companies = data.groupby('job title')['company'].nunique()
    # valid_job_titles = job_titles_with_multiple_companies[job_titles_with_multiple_companies > 1].index

    # # Create selectbox for job title
    # selected_job_title = st.selectbox('Select Job Title For Comparison', valid_job_titles)

    # # Filter data based on selected job title and non-empty salary ranges
    # filtered_data = data[(data['job title'] == selected_job_title) & (data['salary range'].notna())]

    # # Create a box plot or violin plot to compare salary ranges across different companies
    # plt.figure(figsize=(12, 8))
    # sns.boxplot(x='salary range', y='company', data=filtered_data, palette='coolwarm')
    # plt.xlabel('Salary Range')
    # plt.ylabel('Company')
    # plt.title(f'Salary Range for {selected_job_title} Across Different Companies')
    # st.pyplot(plt)

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