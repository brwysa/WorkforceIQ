#This is a Module to predict KPI 
#Akan terdapat dua cara dalam melakukan prediksi, dengan TimeSeries dan Dengan watsonx
# from dotenv import load_dotenv
import json
import plotly.io as pio
# Import IBMGen Library 
# from langchain.chains.conversation.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
# from langchain.llms.base import LLM
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationChain
# Import lang Chain Interface object
# from langChainInterface import LangChainInterface
# Import system libraries
# import os
# Import streamlit for the UI 
# import streamlit as st
import re
from ibm_watson_machine_learning.foundation_models import Model
# import docx
import pandas as pd
from app.utils.watsonx_hr_fin import WatsonXModel
import pandas as pd 
import numpy as np 
import plotly.express as px
import os

# Load environment vars
# load_dotenv()
base_path = os.path.dirname(__file__)



def interpolate_functions(df_all):
    #Interpolate Null Data
    df_all_2 = df_all.copy()
    df_all_2['Revenue'] = df_all_2['Revenue'].replace(0, np.nan)
    df_all_2['Sales Quantity'] = df_all_2['Sales Quantity'].replace(0, np.nan)
    df_all_2['Customers'] = df_all_2['Customers'].replace(0, np.nan)

    # Group by 'Department' and apply interpolation
    df_all_2['Revenue'] = df_all_2.groupby('Department')['Revenue'].apply(lambda x: x.interpolate(method ='linear', limit_direction ='backward'))
    df_all_2['Sales Quantity'] = df_all_2.groupby('Department')['Sales Quantity'].apply(lambda x: x.interpolate(method ='linear', limit_direction ='backward'))
    df_all_2['Customers'] = df_all_2.groupby('Department')['Customers'].apply(lambda x: x.interpolate(method ='linear', limit_direction ='backward'))
    return df_all_2

def remapping_restructure_funct(df_all_2):
    #Pembatasan Data
    df_all_cat_1 = df_all_2[(df_all_2['YearMonth'] >= '2020-01') & (df_all_2["YearMonth"]<='2020-12')]
    df_all_cat_2 = df_all_2[(df_all_2['YearMonth'] >= '2022-01') & (df_all_2["YearMonth"]<='2022-12')]
    #Remapping Data
    mapper_to_change_1 = {"Strategic Partnerships":"Finance Director",
                    "Business Development":"Finance",
                    "Channel Sales":"Legal",
                    "Customer Success":"Customer Management",
                    "E-commerce Sales":"Human Capital",
                    "Enterprise Sales":"Operations Excellence",
                    "Inside Sales":"Premium Care",
                    "International Sales":"Supply Chain",
                    "Key Accounts":"Data",
                    "Outside Sales":"Developer",
                    "Retail Sales":"Head of Infrastructure & Technical Support",
                    "Sales Analytics":"Software Quality",
                    "Sales Support":"Campaign",
                    "Sales Training":"Creative Designer Marketing",
                    "Sales Enablement":"Platform Designer",
                    "Sales Engineering":"Platform Engineer",
                    "Sales Operations":"Product Manager",
                    "Account Management":"Researcher"
                    }
    #For Data Two
    mapper_to_change_2 = {"Strategic Partnerships":"Activation",
                        "Business Development":"Creative Designer",
                        "Channel Sales":"Head of Sales Excellence",
                        "Customer Success":"Head of Sales Support",
                        "E-commerce Sales":"Head of Sales",
                        "Sales Administration":"Planner",
                        "Inside Sales":"Promotion",
                        "International Sales":"Sales Admin",
                        "Key Accounts":"Sales Analytics",
                        "Outside Sales":"Sales Community",
                        "Retail Sales":"Sales Digital",
                        "Sales Analytics":"Sales Director",
                        "Sales Enablement":"Sales Marketplace",
                        "Sales Engineering":"Sales Trading",
                        "Account Management":"Head of Regional Sale",
                        "Sales Operations":"Brand",
                        "Sales Support":"Partnership Marketing",
                        "Sales Training":"Performance Marketing",
                        "Enterprise Sales":"Head of Marketing"}
    df_all_cat_1['Department'] = df_all_cat_1['Department'].replace(mapper_to_change_2)
    df_all_cat_2['Department'] = df_all_cat_2['Department'].replace(mapper_to_change_1)
    #Remapping Waktu
    df_all_cat_1['YearMonth'] = pd.to_datetime(df_all_cat_1['YearMonth'])
    df_all_cat_1['YearMonth'] = df_all_cat_1['YearMonth'] + pd.DateOffset(years=3)
    df_all_cat_1['YearMonth'] = df_all_cat_1['YearMonth'].dt.strftime('%Y-%m')
    df_all_cat_2['YearMonth'] = pd.to_datetime(df_all_cat_2['YearMonth'])
    df_all_cat_2['YearMonth'] = df_all_cat_2['YearMonth'] + pd.DateOffset(years=1)
    df_all_cat_2['YearMonth'] = df_all_cat_2['YearMonth'].dt.strftime('%Y-%m')
    #Get Specific Data
    df_part_1 = df_all_cat_1[df_all_cat_1['YearMonth']<='2023-09'][['Department','YearMonth','Revenue']]
    df_part_2 = df_all_cat_2[df_all_cat_2['YearMonth']<='2023-09'][['Department','YearMonth','Revenue']]
    #Get Data to Model
    df_part_1['Revenue'] = df_part_1['Revenue'].round(2)
    df_part_2['Revenue'] = df_part_2['Revenue'].round(2)
    return df_all_cat_1, df_all_cat_2, df_part_1, df_part_2

#Run This two times 
def json_converter(df):
    json_data = {}
    for _, row in df.iterrows():
        department = row['Department']
        if department not in json_data:
            json_data[department] = {}
        json_data[department][str(row['YearMonth'])] = row['Revenue']

    result = [{k: [v]} for k, v in json_data.items()]

    return result

#Run two times
def generate_result(json_data):
    wx = WatsonXModel()
    result_list = []
    for i in range(len(json_data)):
        print(i)
        name = list(json_data[i].keys())[0]
        value = json_data[i][name]
        print(value)
        print(f'Process Running for Departement {name}')
        result = wx.revenue_generator(value)
        result = re.sub(r"\n\n","",result)
        result = re.sub(r"\n", "", result)
        result_json= {name:result}
        result_string = f"{result_json}"
        pattern = r'"'
        json_like_string_no_quotes = re.sub(pattern, '', result_string)
        json_string = json_like_string_no_quotes.replace("'", '"')
        # print(json_string)
        json_string = json.loads(json_string)
        result_list.append(json_string)
        print(result_list)
    return result_list



# Iterate over the list of JSON objects

def redf_result(result_list):
    reshaped_data = []
    for department_data in result_list:
        for department, values in department_data.items():
            for month, value in values.items():
                # Append each row as a dictionary to the reshaped_data list
                reshaped_data.append({'Department': department, 'YearMonth': month, 'Revenue_Predicted': value})

    # Convert reshaped_data to a DataFrame
    df = pd.DataFrame(reshaped_data)
    return df


#Generate Original Result
#Iterate it
def ori_pred_combiner(df_all_cat_1, df_new_predicted_1):
    ori_comb_1 = df_all_cat_1[(df_all_cat_1['YearMonth']>='2023-10') & (df_all_cat_1['YearMonth']<='2023-12')]
    merged_df_1 = pd.merge(df_new_predicted_1, ori_comb_1, on=['Department', 'YearMonth'], how='inner')
    df_all_cat_1['Revenue_Predicted'] = df_all_cat_1['Revenue']
    final_1 = pd.concat([df_all_cat_1[df_all_cat_1['YearMonth']<'2023-10'], merged_df_1])
    final_1['KPI_Achieved_Ori'] = np.where(final_1['Revenue']>=final_1['Revenue Goal'],'Yes','No')
    final_1['KPI_Achieved_Predict'] = np.where(final_1['Revenue_Predicted']>=final_1['Revenue Goal'],'Yes','No')
    return final_1



def kpi_predictor():
    data_sources = os.path.join(base_path, "user_files/first_improvement", "data_sum_per_region_date_all_dept.csv")

    df_all = pd.read_csv(data_sources)
    #Interpolate Data
    df_interpolated = interpolate_functions(df_all)
    #Remapping Data
    df_full_structure_a, df_full_structure_b, df_structure_a, df_structure_b = remapping_restructure_funct(df_interpolated)
    #Json Converter
    json_structure_a= json_converter(df_structure_a)
    json_structure_b = json_converter(df_structure_b)
    #Run Model
    generated_result_json_a = generate_result(json_structure_a)
    generated_result_json_b = generate_result(json_structure_b)
    #Regenerate to DF
    new_df_a = redf_result(generated_result_json_a)
    new_df_b = redf_result(generated_result_json_b)
    #Final Table
    final_1 = ori_pred_combiner(df_full_structure_a, new_df_a)
    final_2 = ori_pred_combiner(df_full_structure_b, new_df_b)
    final_combined = pd.concat([final_1, final_2], ignore_index=True)
    output_file = os.path.join(base_path, "user_files/final_result", "final_combined_result.csv")

    final_combined.to_csv(output_file, index=False)
    return final_combined

def mape(actual, forecast, merged_df_1):
    """
    Calculate Mean Absolute Percentage Error (MAPE).
    
    Parameters:
        actual (array-like): Array containing the actual values.
        forecast (array-like): Array containing the forecasted (predicted) values.
        
    Returns:
        float: MAPE value
    """
    actual, forecast = np.array(actual), np.array(forecast)
    np.mean(np.abs((actual - forecast) / actual)) * 100
    mape_per_department_1 = merged_df_1.groupby('Department').apply(lambda x: mape(x['Revenue'], x['Revenue_Predicted']))
    mape_dict = {dep_name: score for dep_name, score in mape_per_department_1.items()}
    mape_json = json.dumps(mape_dict)
    return mape_json

def plot_data(div_name):
    plot_data_sources = os.path.join(base_path, "final_combined_result.csv")
    final_1 = pd.read_csv(plot_data_sources)
    # Filter data for the current department
    department_data = final_1[final_1['Department'] == div_name]
    
    # Create line plot for the current department
    fig = px.line(department_data, x='YearMonth', y=['Revenue_Predicted', 'Revenue'], 
                color_discrete_map={'Revenue_Predicted': 'green', 'Revenue': 'blue'},  # Set colors for lines
                title=f'{div_name} Revenue and Predicted Revenue', width=1200)  # Set width of the plot
    
    # Show the plot for the current department
    fig.update_xaxes(tickmode='array', tickvals=final_1['YearMonth'].unique(), ticktext=final_1['YearMonth'].unique())  # Set x-axis ticks to show all months
    # fig.show()
    # Save the figure as an image file
    plot_png = os.path.join(base_path,"..", "static", "plot.png")
    image_path = plot_png # Change the path as needed
    pio.write_image(fig, image_path)

    import plotly
    # Convert plot to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # graphJSON = fig.to_json
    return graphJSON

def ratio_kpi_generator(df):
    # Convert 'YearMonth' column to datetime type
    df['YearMonth'] = pd.to_datetime(df['YearMonth'])

    # Filter data for the year 2023
    df_2023 = df[(df['YearMonth'] >= pd.to_datetime('2023-01-01')) & (df['YearMonth'] <= pd.to_datetime('2023-12-31'))]

    # Group by department and calculate KPI Achieved for each month
    results = {}
    for department, group in df_2023.groupby('Department'):
        kpi_achieved = []
        for _, row in group.iterrows():
            achieved = "Yes" if row['Revenue'] >= row['Revenue_Goals'] else "No"
            kpi_achieved.append(achieved)
        results[department] = kpi_achieved

    # Calculate the ratio of "Yes" to the total months for each department
    ratio_results = {}
    for department, kpi_achieved in results.items():
        ratio = kpi_achieved.count("Yes") / len(kpi_achieved)
        ratio_results[department] = ratio

    # Write the results to a JSON file
    write_result = os.path.join(base_path, "user_files/final_result", "kpi_results.json")
    with open(write_result, 'w') as f:
        json.dump(ratio_results, f, indent=4)

    return ratio_results











