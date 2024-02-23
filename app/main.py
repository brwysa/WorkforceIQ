import json
from app.utils.watsonx_hr_fin import WatsonXModel
from app.utils.kpi_predictor import *
import os 
import json
from docx import Document

base_path = os.path.dirname(__file__)
# base_path = './'
print(base_path)
wx  =  WatsonXModel()

#FUNCTION UNTUK UPLOAD
def docx_table_to_json(docx_path):
    # Load the document
    doc = Document(docx_path)
    job_details = {
        "Title": "",
        "JobResponsibilities": []
    }
    
    # Iterate through tables
    is_title_row = True 

    for table in doc.tables:
        for row in table.rows:
            for i, cell in enumerate(row.cells):
                text = cell.text.strip()
                if is_title_row:
                    if i == 0 and text == 'Title position':
                        continue
                    job_details["Title"] += text 
                else:  # Assuming the rest are job responsibilities
                    if i == 0 and text.startswith('Job Responsibility'):
                        continue
                    if text.startswith('Job Summary'):
                        continue
                    job_details["JobResponsibilities"].append(text)

        is_title_row = False

    return job_details

def process_folder(folder_path, dep_name):
    all_jobs = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.docx'):
            full_path = os.path.join(folder_path, file_name)
            job_json = docx_table_to_json(full_path)
            all_jobs.append(job_json)
    
    # Save or process all_jobs JSON array as needed
    UPLOAD_FOLDER = os.path.join(base_path, 'user_files/realtime/upload/result')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER) 
    with open(os.path.join(base_path, "user_files/realtime/upload/result", f"{dep_name}.json"), "w") as json_file:
        json.dump(all_jobs, json_file, indent=4)

# Example usage

    
####### GEN AI HR ##################################
def genai_hr_initiate(dep_to_test):
    load_goals  = './user_files/job_resp/goal.json'
    with open(load_goals, "r") as json_file:
        com_goals= json.load(json_file)
    load_data =  f'./user_files/job_resp/{dep_to_test}/{dep_to_test}_job_output.json'
    with open(load_data, "r") as json_file:
        input_data = json.load(json_file)
    if dep_to_test == 'finance':
        run_model = wx.finance_optimized_org(load_goals, input_data)
    elif dep_to_test=='operation':
        run_model = wx.operation_optimized_org(load_goals, input_data)
    elif dep_to_test=='sales_marketing':
        run_model = wx.sales_marketing_optimized_org(load_goals, input_data)
    elif dep_to_test=='sales_platform':
        run_model = wx.sales_platform_optimized_org(load_goals, input_data)
    elif dep_to_test=='sales_support':
        run_model = wx.sales_support_optimized_org(load_goals, input_data)
    elif dep_to_test=='tech':
        run_model = wx.tech_optimized_org(load_goals, input_data)
    else:
        print('please choose right parameters')
    #logic to make it can be add to json: logic start
    #Logic end
    model_to_json = wx.json_converter(load_goals, run_model)
    json_result = json.loads(model_to_json)
    output_file_path = f"./user_files/final_result/{dep_to_test}_ideal.json"
    # Write the JSON data to the output file
    with open(output_file_path, "w") as output_file:
        json.dump(json_result, output_file, indent=4)

    #Create skill mapping
    dep_skill = wx.skill_mapping(input_data, load_goals)
    skill_result = json.loads(dep_skill)
    # output_file_path_skill = f"./user_files/skill_map/{dep_to_test}_skillset.json"

    data_file_path_skill = os.path.join(base_path, "skill_map", f"{dep_to_test}_skillset.json")
    with open(data_file_path_skill, 'w') as output_file:
    # with open(output_file_path_skill, "w") as output_file:
        json.dump(skill_result, output_file, indent=4)
    
    return output_file_path

def load_avail_data(dep_to_run, div_name, base_path):
    #Load new Responsibility
    
    data_file_path_ideal = os.path.join(base_path, "user_files/final_result", f"{dep_to_run}_ideal.json")
    with open(data_file_path_ideal, 'r') as f:
        data = json.load(f)

    # Store each result in separate variables
    departments = []
    recommendations = data['recommendation']
    # note = data['note']


    # Extract department names and recommended job responsibilities
    for department in data["departments"]:
        if department["name"] == div_name:
            recommend_job = department["recommendedJobResponsibilities"]
            try:
                reasoning = department['reasoning']
            except:
                reasoning = None

    # Load Skill Map
    data_file_path_skill = os.path.join(base_path, "user_files/skill_map", f"{dep_to_run}_skillmap.json")
    with open(data_file_path_skill, 'r') as f:
        skill_map_json = json.load(f)
    try:
        skill_map = skill_map_json[div_name]
    except:
        skill_map = None
    try:
        return div_name, recommend_job, reasoning, recommendations, skill_map
    except:
        return recommendations

def load_data(dep_to_test, div_name, generate_new = 'no'):
    dep_to_test = dep_to_test.lower().replace(" ", "_")
    if generate_new == 'Yes':
        result = genai_hr_initiate(dep_to_test=dep_to_test)
        return result
    else:
        try:
            div_name, recommend_job, reasoning, recommendations, skill_map = load_avail_data(dep_to_run=dep_to_test, div_name = div_name, base_path = base_path)
            return div_name, recommend_job, reasoning, recommendations, skill_map
        except:
            recommendations = load_avail_data(dep_to_run=dep_to_test, div_name = div_name, base_path = base_path)
            return recommendations

def load_asis_data(dep_to_test, div_name):
    dep_to_run = dep_to_test.lower().replace(" ", "_")
    
    if 'sale' in dep_to_run:
        data_file_path_assist = os.path.join(base_path, "user_files/job_resp/sales", f"{dep_to_run}_jobs_output.json")
        with open(data_file_path_assist, 'r') as f:
            data = json.load(f)
    else:
        data_file_path_lainnya = os.path.join(base_path, f"user_files/job_resp/{dep_to_run}", f"{dep_to_run}_jobs_output.json")
        with open(data_file_path_lainnya, 'r') as f:
            data = json.load(f)

    department_data = next((job for job in data if job['department'] == div_name), None)
    print(f'department data: {department_data}')
    try:
        return department_data['JobResponsibilities']
    except:
        return None

def get_div_names(dep_name):
    dep_to_run = dep_name.lower().replace(" ", "_")
    data_file_path= os.path.join(base_path, f"user_files/final_result/{dep_to_run}_ideal.json")
    with open(data_file_path, 'r') as f:
        data = json.load(f)
    ideal_division_names = [division['name'] for division in data['departments']]

    if 'sale' in dep_to_run:
        data_file_path_assist = os.path.join(base_path, "user_files/job_resp/sales", f"{dep_to_run}_jobs_output.json")
        with open(data_file_path_assist, 'r') as f:
            data = json.load(f)
    else:
        data_file_path_lainnya = os.path.join(base_path, f"user_files/job_resp/{dep_to_run}", f"{dep_to_run}_jobs_output.json")
        with open(data_file_path_lainnya, 'r') as f:
            data = json.load(f)
    asis_division_names = []
    for item in data:
        asis_division_names.append(item["department"])
    print(asis_division_names)
    return ideal_division_names, asis_division_names


#Realtime not needed 
def genai_hr_initiate(dep_name, div_name, com_goal):
    div_data_to_load = "/Users/muhammadfadlyhidayat/Documents/ibm/Watsonx/Working_Project/14rd_abc/Tahap_2/abc_GenAI/app/user_files/job_resp/finance/finance_jobs_output.json"
    # div_data_to_load = os.path.join(base_path, f"user_files/realtime/upload", f"{dep_name}_jobs_output.json")
    with open(div_data_to_load, "r") as json_file:
        original_data = json.load(json_file)
    department = None
    for department in original_data:
        if department['department'] == div_name:
            selected_department = department
    another_dep = [department for department in original_data if department['department'] != div_name]
    wx = WatsonXModel()
    print('Process ideal')
    ideal_job_resp = wx.job_responsibilities_model(goal=com_goal,job_respons_actual = selected_department["JobResponsibilities"], another_job_resp = another_dep,  div_name=div_name)
    reasoning = wx.reasoning(goal=com_goal,division_name=div_name, actual_job_responsibilites = selected_department["JobResponsibilities"], ideal_job_resp=ideal_job_resp)
    print('Process recom')
    recommendation = wx.recommendation(goal=com_goal,department_name=dep_name, division_name=div_name, actual_job_responsibilites= selected_department["JobResponsibilities"], ideal_job_resp=ideal_job_resp, reasoning=reasoning)
    print('Process skillmap')
    skill_map = wx.skill_mapping_realtime(job_resp_ideal=ideal_job_resp ,goal_input=com_goal, div_name = div_name)
    final_result = {"name":div_name, 
                    "recommendedJobResponsibilities": recommendation,
                     "reasoning":reasoning,
                     "skill_map":skill_map}
    json_data = json.dumps(final_result)

    # Store JSON string to a file
    div_data_to_load = os.path.join(base_path, f"user_files/realtime/result/{dep_name}", f"{div_name}_jobs_output.json")
    with open(div_data_to_load, "w") as json_file:
         json_file.write(json_data)
        
    return ideal_job_resp

#----------------------------------------------------------------------------------
#                                   Model Raihan
#----------------------------------------------------------------------------------
def get_gap(dep_name, div_name, goal = None, input_jobdesk = None, input_ideal_jobdesk = None, is_rerun = 'No'):
    dep_name = dep_name.lower().replace(" ", "_")
    if is_rerun =='No':
        div_data_to_load = os.path.join(base_path, f"user_files/gap_analysis/{dep_name}", f"{dep_name}_gap.json")
        with open(div_data_to_load, 'r') as f:
            data = json.load(f)
        try:
            get_result = data[div_name]
        except:
            get_result = None
    elif is_rerun =='Yes':
        job_gap_wx = wx.job_gap(goal, input_jobdesk, input_ideal_jobdesk)
        get_result = job_gap_wx
    else:
        pass
    return get_result

#------------------------------------------------------------------------------------
#                                   FLASK APP
#------------------------------------------------------------------------------------
from flask import Flask, render_template, request, session, redirect, url_for
import re

app = Flask(__name__)
# Define the initial route to render the template

from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'IBMECOMMERCE123132'

# Define a function to clean up the input text
def clean_text(text):
    # Remove leading/trailing whitespace and newlines
    text = text.strip()
    # Replace periods with full stops
    text = text.replace(".", ". ")
    # Capitalize the first letter of each sentence
    return text.capitalize()

# Process Category Form

@app.route('/process_category', methods=['POST'], endpoint="process_category_form")
def process_category_form():
    selected_category = request.form.get('category')
    session['selected_category'] = selected_category
    ideal_div_names, asis_div_names = get_div_names(session['selected_category'])
    combined_div_names = asis_div_names + [item for item in ideal_div_names if item not in asis_div_names]
    return render_template('index.html', combined_div_names = combined_div_names, ideal_div_names=ideal_div_names, asis_div_names=asis_div_names)

    # Add your logic for category form processing
    print(f'\n\n\n\Category Name:{selected_category}\n\n\n\n\n\n\n')
    return render_template('index.html', selected_category=selected_category)

# Process Division Form
@app.route('/process_division', methods=['POST'], endpoint="process_division_form")
def process_division_form():
    selected_division = request.form.get('division')
    session['selected_division'] = selected_division

    try:
        div_name, recommend_job, reasoning, recommendations, skill_map =  load_data(session['selected_category'], session['selected_division'])
        skill_map = [f"{i+1}. {category}" for i, category in enumerate(skill_map)]
    except:
        recommendations = load_data(session['selected_category'], session['selected_division'])
        # Set other variables to None or appropriate default values
        div_name = None
        recommend_job = None
        reasoning = None
        skill_map = None

    asis_job = load_asis_data(session['selected_category'], session['selected_division'])
    print(session['selected_category'])
    

    graphJSON = plot_data(selected_division)
    try:
        cleaned_recommend_job = [job.replace("'", "") for job in recommend_job]
    except:
        cleaned_recommend_job = None

    string_recommendations = str(recommendations).replace("'", "").replace("[", "").replace("]", "")

    ideal_div_names, asis_div_names = get_div_names(session['selected_category'])
    combined_div_names = asis_div_names + [item for item in ideal_div_names if item not in asis_div_names]
    print("\n\n\n\n",combined_div_names)
    job_gap = get_gap(session["selected_category"], session["selected_division"])
    return render_template('index.html', combined_div_names = combined_div_names, string_recommendations = string_recommendations, jobgap = job_gap, ideal_div_names=ideal_div_names, asis_div_names=asis_div_names, selected_division=selected_division, recommend_job=cleaned_recommend_job, skill_map=skill_map, recommendations=recommendations, reasoning=reasoning, graphJSON = graphJSON, asis_job= asis_job)

@app.route('/reset_session', methods=['POST'])
def reset_session():
    session.pop('selected_category', None)
    session.pop('selected_division', None)
    return redirect(url_for('home'))

UPLOAD_FOLDER = os.path.join(base_path, 'user_files/realtime/upload/trash')
if not os.path.exists(UPLOAD_FOLDER):
    print("hello")
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = []
    if 'files[]' in request.files:
        files = request.files.getlist('files[]')
        for file in files:
            # Handle each file (save, process, etc.)
            file_path = os.path.join(base_path, "user_files/realtime/upload/trash", f"{file.filename}")
            file.save(file_path)
            uploaded_files.append(file_path)
            print("File saved at:", file_path)  # Print the absolute path where each file is saved
        folder_path = os.path.join(base_path, "user_files/realtime/upload/trash")
        process_folder(folder_path, session["selected_category"])
        return render_template("index.html", message="File uploaded succesfully")
    else:
        return render_template("index.html", message="File failed to upload")

@app.route('/save_job', methods=['POST'])
def save_job():
    job = request.form['job']
    action = request.form['action']
    
    # Determine the filename based on the action
    filename = f"{session['selected_division']}_{action}.json"
    filepath = os.path.join(base_path, f'user_files/reinforcement/{session["selected_category"]}')
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    # Load existing data from the file, or create an empty list if the file doesn't exist
    try:
        with open(f"{filepath}/{filename}", 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    # Append the new job to the data
    data.append(job)

    # Write the updated data back to the file
    with open(f"{filepath}/{filename}", 'w') as f:
        json.dump(data, f, indent=4)
    return render_template("index.html")
    
# Initial route to render the template
@app.route('/')
def home():
    session.pop('selected_category', None)
    session.pop('selected_division', None)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

