import os
import json
import streamlit as st

import yfinance as yf
from millify import millify
import plotly.express as px
import json
from streamlit_extras.add_vertical_space import add_vertical_space


def save_department_data(department_name, date, folder_path):
    data = {'company_name': department_name, 'date': date.strftime('%Y-%m-%d'), 'folder_path': folder_path}

    # Specify the folder location where the JSON file will be stored
    json_file_path = os.path.join('data', 'department_data.json')

    # Ensure the "data" folder exists
    os.makedirs('data', exist_ok=True)

    # Read existing data from JSON file
    if os.path.isfile(json_file_path):
        with open(json_file_path, 'r') as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Append new data to existing data
    existing_data.append(data)

    # Write updated data back to JSON file
    with open(json_file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)

def get_existing_company_names():
    try:
        with open('data/department_data.json', 'r') as f:
            company_data = json.load(f)
        return [entry['company_name'] for entry in company_data]
    except Exception as e:
        print(f"Error: {e}")
        return []

# Function to get existing company names and their corresponding folder paths from company_data.json
def get_existing_company_info():
    try:
        with open('data/department_data.json', 'r') as f:
            company_data = json.load(f)
        return {entry['company_name']: entry['folder_path'] for entry in company_data}
    except Exception as e:
        print(f"Error: {e}")
        return {}

# Use the function to get existing company names and folder paths


# Function to get folder path based on company name
def get_folder_path(company_name):
    existing_company_info = get_existing_company_info()
    return existing_company_info.get(company_name, "Folder path not found")
# kpi_data_json = "Data from 2017 untill 2022"

# def get_department_data_json_name():
#     return kpi_data_json

# def fetch_existing_department(json_file):
#     department_data = {}

#     if os.path.exists(json_file):
#         with open(json_file, "r") as f:
#             department_data = json.load(f)

#     return list(department_data.keys())


# def get_department_data(department_name, json_file):
#     with open(json_file, "r") as f:
#         department_data = json.load(f)

#     return department_data[department_name]


# def set_session_variables(company_name, company_data, _st):
#     _st.session_state["selected_company"] = company_name
#     _st.session_state["docx_pathfile"] = company_data["docx_path"]
#     _st.session_state["xlsx_path"] = company_data["xlsx_path"]
#     _st.session_state["folder_path"] = company_data["folder_path"]
