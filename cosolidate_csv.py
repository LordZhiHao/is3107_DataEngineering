import pandas as pd
import numpy as np

def rename_and_filter_columns(df, mapping):
    renamed_columns = {}
    for new_name, old_names in mapping.items():
        for old_name in old_names:
            if old_name in df.columns:
                renamed_columns[old_name] = new_name
                break  # Stop looking once we find the first match
        if new_name not in renamed_columns.values():  # Check if the new_name is not yet in the renamed_columns
            df[new_name] = np.nan  # If a column is missing, create it with all null values
    # Rename the columns and re-order based on the mapping dictionary keys to ensure consistency
    return df.rename(columns=renamed_columns)[list(mapping.keys())]

def consolidate():
    mapping_dict = {
        "job title": ["Designation", "Job Title", "titles", "title"],
        "description": ["Job Description", "teasers", "description"],
        "company": ["Company", "companies", "company"],
        "salary range": ["Allowance / Remuneration", "Salary", "salaries"]
    }
    # read csv
    internsg_df = pd.read_csv('InternSg_WebScraping/internSG_jobs.csv')
    indeed_df = pd.read_csv('Indeed_WebScraping/indeed_jobs_modified.csv')
    jobstreet_df = pd.read_csv('JobStreet_WebScraping/jobstreet_jobs_data.csv')
    linkedin_dir = 'LinkedIn_WebScraping/'
    linkedin_DA = pd.read_csv(linkedin_dir + 'dataAnalyst_jobs.csv')
    linkedin_DS =  pd.read_csv(linkedin_dir + 'dataScientist_jobs.csv')
    linkedin_MLE = pd.read_csv(linkedin_dir + 'machineLearningEngineer_jobs.csv')
    # consolidate 3 linkedin files
    linkedin_df = pd.concat([linkedin_DA, linkedin_DS, linkedin_MLE]).reset_index(drop=True).drop_duplicates()
    
    internsg_df_new = rename_and_filter_columns(internsg_df, mapping_dict)
    indeed_df_new = rename_and_filter_columns(indeed_df, mapping_dict)
    jobstreet_df_new = rename_and_filter_columns(jobstreet_df, mapping_dict)
    linkedin_df_new = rename_and_filter_columns(linkedin_df, mapping_dict)
    consolidated_df = pd.concat([internsg_df_new,indeed_df_new,jobstreet_df_new,linkedin_df_new])
    consolidated_df = consolidated_df[consolidated_df['description'].notnull()]
    consolidated_df.to_csv('consolidated.csv',index=False)

consolidate()