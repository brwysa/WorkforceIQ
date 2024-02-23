import os
import json
# from dotenv import load_dotenv
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

import json

# from dotenv import load_dotenv


# load_dotenv()
# Yang BENER 
# api_key = os.environ["WX_API_KEY"]
# ibm_cloud_url = os.environ["WX_IBM_CLOUD_URL"]
# project_id = os.environ["WX_PROJECT_ID"]
# if api_key is None or ibm_cloud_url is None or project_id is None:
#     raise Exception("Ensure you copied the .env file that you created earlier into the same directory as this notebook")
# else:
#     creds = {
#         "url": ibm_cloud_url,
#         "apikey": api_key
#     }


#BUAT COBA COBA
# Load environment vars
# from dotenv import load_dotenv
# load_dotenv()

# Define credentials 
# api_key = os.getenv("API_KEY", None)
# ibm_cloud_url = os.getenv("IBM_CLOUD_URL", None)
# project_id = os.getenv("PROJECT_ID", None)
# serp_api_key = os.getenv("SERP_API_KEY",None)
api_key = os.environ["WX_API_KEY"]
ibm_cloud_url = os.environ["WX_IBM_CLOUD_URL"]
project_id = os.environ["WX_PROJECT_ID"]


if api_key is None or ibm_cloud_url is None or project_id is None:
    print("Ensure you copied the .env file that you created earlier into the same directory as this notebook")
else:
    creds = {
        "url": ibm_cloud_url,
        "apikey": api_key 
    }

class WatsonXModel:
    def __init__(
        self,
        creds=creds,
        project_id=project_id,
        model_name="meta-llama/llama-2-70b-chat",
        model_params = {
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.MAX_NEW_TOKENS: 3000,
            #GenParams.TEMPERATURE: 0.75,
            GenParams.REPETITION_PENALTY: 1,
            #GenParams.TOP_K: 1,
            #GenParams.RANDOM_SEED: 362,
            #GenParams.STOP_SEQUENCES: ["\n\n "],
        }
    ):
        model = Model(
            model_id=model_name,
            params=model_params,
            credentials=creds,
            project_id=project_id
        )

        self.model = model

    def sales_platform_optimize_org(self,goal,job_sales_platform, div_name):       
        model = self.model

        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"check in this data {job_sales_platform} is there any job responsibility in one department that is same with any other department.\n"\
                "If there is job responsibility in one department that is same with any other department. generate a recommendation to make the job responsibility distinct and effective."\
                "Make the recommendation per point in department that has same jobdesk and modified version of it."\
                "if it needed generate which job desk that need to cut or merge because of the job desk to differentiate and the reason behind it."\
                f"Generate recommended job responsibilities per point for 'division': {div_name}"\
                "[/INST]\n"\
                "Output:"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response


    def sales_marketing_optimized_org(self,goal,job_sales_marketing):       
        model = self.model

        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"check in this data {job_sales_marketing} is there any job responsibility in one department that is same with any other department.\n"\
                "If there is job responsibility in one department that is same with any other department. generate a recommendation to make the job responsibility distinct and effective."\
                "Make the recommendation per point in department that has same jobdesk and modified version of it."\
                "if it needed generate which job desk that need to cut or merge because of the job desk to differentiate and the reason behind it."\
                "Generate the output per point with department and recommended job responsibilities as keys."\
                "do not generate again the input job responsibility as an output."\
                "do not generate the answear in json."\
                "Also generate the reason behind every decision you made."\
                "[/INST]\n"\
                "Output:"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response

    
    @staticmethod
    def sales_support_optimized_org(goal,job_sales_support, creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 4000,
            "min_new_tokens": 1,
            "repetition_penalty": 1,
            #"Temperature" : 0.7
            # "stop_sequences": [""]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"check in this data {job_sales_support} is there any job responsibility in one department that is same with any other department.\n"\
                "If there is job responsibility in one department that is same with any other department. generate a recommendation to make the job responsibility distinct and effective."\
                "Make the recommendation per point in department that has same jobdesk and modified version of it."\
                "if it needed generate which job desk that need to cut or merge because of the job desk to differentiate and the reason behind it."\
                "Generate the output per point with department and recommended job responsibilities as keys."\
                "do not generate again the input job responsibility as an output."\
                "[/INST]\n"\
                "Output:"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response


    def tech_optimized_org(self,goal,job_tech):
        model = self.model
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"check in this data {job_tech} is there any job responsibility in one department that is same with any other department.\n"\
                "If there is job responsibility in one department that is same with any other department. generate a recommendation to make the job responsibility distinct and effective."\
                "Make the recommendation per point in department that has same jobdesk and modified version of it."\
                "if it needed generate which job desk that need to cut or merge because of the job desk to differentiate and the reason behind it."\
                "Generate the output per point with department and recommended job responsibilities as keys."\
                "do not generate again the input job responsibility as an output."\
                "do not generate the answear in json."\
                "Also generate the reason behind every decision you made."\
                "[/INST]\n"\
                "Output:"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response

    @staticmethod
    def operation_optimized_org(goal,job_operation, creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 4050,
            "min_new_tokens": 1,
            "repetition_penalty": 1,
            #"Temperature" : 0.7
            # "stop_sequences": [""]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"check in this data {job_operation} is there any job responsibility in one department that is same with any other department.\n"\
                "If there is job responsibility in one department that is same with any other department. generate a recommendation to make the job responsibility distinct and effective."\
                "Make the recommendation per point in department that has same jobdesk and modified version of it."\
                "if it needed generate which job desk that need to cut or merge because of the job desk to differentiate and the reason behind it."\
                "Generate the output per point with department and recommended job responsibilities as keys."\
                "do not generate again the input job responsibility as an output."\
                "do not generate the answear in json."\
                "[/INST]\n"\
                "Output:"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response

    def finance_optimized_org(self,goal,job_finance):
       
        model=self.model
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"check in this data {job_finance} is there any job responsibility in one department that is same with any other department.\n"\
                "If there is job responsibility in one department that is same with any other department. generate a recommendation to make the job responsibility distinct and effective."\
                "Make the recommendation per point in department that has same jobdesk and modified version of it."\
                "if it needed generate which job desk that need to cut or merge because of the job desk to differentiate and the reason behind it."\
                "Generate the output per point with department and recommended job responsibilities as keys."\
                "do not generate again the input job responsibility as an output."\
                "do not generate the answear in json."\
                "[/INST]\n"\
                "Output:"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response

#--------------------------- Revenue Predictor --------------------------------------------
    @staticmethod
    def revenue_generator(df, creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 100,
            "min_new_tokens": 1,
            "repetition_penalty": 1,
            "stop_sequences": ["\n\n"]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"{df} is a dataset of a company.\n"\
                "Predict the next one month revenue based on the data provided.\n"\
                "Please give the answear only the value of the prediction.\n"\
                "[/INST]\n"\
                "Output:"
                

        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response
 
    # Notes : use the code below to identified the unique for every department
    # dep_name = df_new['Department'].unique().tolist()
    # df_per_team = pd.DataFrame()
    # result_list = []
    # for i in dep_name:
    #     print(f'Process Running for Departement{i}')
    #     df_per_team = df_new[df_new['Department']==i]
    #     result = revenue_generator(df_per_team, i)
    #     result_json = {i:result}
    #     print(result_json)
    #     result_list.append(result_json)
    
    #     print(f'Process Complete for Departement {i}')

    # result_list    

#---------------------- Revenue Growth generator --------------------

    @staticmethod
    def rev_change_percentage(last_revenue,pred_revenue, creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "min_new_tokens": 1,
            "repetition_penalty": 1,
            #"Temperature" : 0.7
            # "stop_sequences": [""]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"{last_revenue} is the last revenue data of a company.\n"\
                f"{pred_revenue} is a prediction of a company revenue for the coming month. \n"\
                f"Calculate the revenue growth from {last_revenue} with {pred_revenue}.\n"\
                "[/INST]\n"\
                "Output:"

        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response
    
    @staticmethod
    def revenue_generator(df, creds=creds, project_id=project_id):
        parameters_comply = {
                    "decoding_method": "greedy",
                    "max_new_tokens": 80,
                    "min_new_tokens": 1,
                    "repetition_penalty": 1.1,
                    "stop_sequences": ["}\n\n"]
                }
        granite = 'ibm/granite-20b-5lang-instruct-rc'
        falcon = "ibm/falcon-40b-8lang-instruct"
        flanul = "google/flan-ul2"
        llama = "meta-llama/llama-2-70b-chat"
        model_sim = Model(
                model_id=llama,
                params=parameters_comply,
                credentials=creds,
                project_id=project_id)
        
        model = model_sim
        template = "<[INST] «SYS»\n"\
                    "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible\n"\
                    "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                    "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                    "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                    "If you don't know the answer to a question, please don't share false information.\n"\
                    "«/SYS»\n"\
                    f"Data to Analyze: {df} .\n"\
                    "Develop an advanced FORECASTING model to do a time-series to ACCURATELY predict the next three month Revenue for month '2023-10','2023-11','2023-12' based on given 'Data to Analyze'.\n"\
                    "Dont give explanation and make the answer concat separate the monthly result ONLY format like this \{'2023-10':12,'2023-11':12,'2023-12':12\} .\n"\
                    "[/INST]\n"\
                    "Output:\n\n"\
                    
        generated_response = model.generate_text(prompt=template)
        generated_response 
        return generated_response
    
#--------------- best 2 and worst 2 department based on KPI -----------------------    
    @staticmethod
    def best_worst(dept_ratio_kpi, creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 700,
            "min_new_tokens": 1,
            "repetition_penalty": 1,
            "Temperature" : 0.7
            # "stop_sequences": [""]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"{dept_ratio_kpi} is the KPI achieved ratio of a company's sales department\n"\
                "Generate insight for 2 the best ratio department and Generate insight for 2 the worst ratio department."\
                "Generate the indicator that make 2 best department successful and the indicator that make 2 worst department unsuccessful"\
                "[/INST]\n"\
                "Output:"

        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response


#-------------------------------- Skill Maping -------------------------------------
    @staticmethod
    def skill_mapping(job_input,goal_input, creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 3000,
            "min_new_tokens": 1,
            "repetition_penalty": 1,
            #"Temperature" : 0.7
            "stop_sequences": ["}\n\n"]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal_input} as consideration"\
                f"generate skill set that is necessary for department in {job_input}."\
                "do not generate again the input job responsibility as an output."\
                "generate the answear in json with key : department, skill set and the reason behind it for every department reason."\
                "[/INST]\n"\
                "Output:"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response
    #make sure put the goal first in the function skill(goal,job_input) 
#--------------------------------- json converter ---------------------------------
    
    @staticmethod
    def json_converter(goal, job_input,  creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 3000,
            "min_new_tokens": 1,
            "repetition_penalty": 1,
            #"Temperature" : 0.7
            # "stop_sequences": [""]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"this is the string {job_input} that we want to conver to json."\
                "make sure the key is key : departments , key : division , key : recommended_job_responsibilities, key : Recommendations"\
                "[/INST]\n"\
                "Output:"
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response
    
    @staticmethod
    def json_converter(file_to_convert ,goal, creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 3000,
            "min_new_tokens": 1,
            "repetition_penalty": 1,
            "stop_sequences": ["}\n\n"]

            #"Temperature" : 0
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"this is the string {file_to_convert} that we want to convert to json."\
                "make sure to generate valid JSON Format where the key is key : departments , key : division , key : recommended_job_responsibilities, key : Recommendations"\
                "[/INST]\n"\
                "Output:"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response
    

    #   {"dep_name": [{"div_name":"Finance",
    #      "JobsResp":"aaaaa",
    #      "Reason":"aaa",
    #      "Skillset":"aaa"}  ,{},{}]} 

#---------------------------------Final Step 2 -----------------------------------------------#
    #skilset
    @staticmethod
    def skill_mapping_realtime(div_name, job_resp_ideal ,goal_input, creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "min_new_tokens": 1,
            "repetition_penalty": 1
            #"Temperature" : 0.7
            # "stop_sequences": ["\n\n"]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal_input} as consideration"\
                f"generate skill set that is necessary for this division with this 'Job Responsibility': {job_resp_ideal}."\
                f"Only Generate skill set that needed based on this Job Responsibilities for division :{div_name} to make the can achieve company goal."\
                "[/INST]\n"\
                "Output:\n\n"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)
        return generated_response
    
    #job_responsibilities
    @staticmethod
    def job_responsibilities_model(goal,job_respons_actual, another_job_resp,  div_name,creds = creds, project_id = project_id):       
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 2000,
            "min_new_tokens": 1,
            "repetition_penalty": 1
            #"Temperature" : 0.7
            # "stop_sequences": ["\n\n"]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"check in this 'Job resposibilities data for division:{div_name}': {job_respons_actual} and there are another job resposibilities in this department: {another_job_resp} is there any job responsibility in one department that is same redundant.\n"\
                "If there is job responsibility in main division that is same with any other division. generate a recommendation to make the job responsibility distinct and effective."\
                "Make the recommendation per point in department that has same jobdesk and modified version of it."\
                "if it needed generate which job desk that need to cut or merge because of the job desk to differentiate."\
                f"Generate recommended job responsibilities per point for 'division': {div_name}"\
                "Please make sure you analyze every single point from this job responsibilities make your answer concise and only show updated .\n"\
                "[/INST]\n"\
                "Output:\n\n"
        generated_response = model.generate_text(prompt=template)
        return generated_response
    
    #reasoning
    @staticmethod
    def reasoning(goal,division_name, actual_job_responsibilites, ideal_job_resp, creds = creds, project_id = project_id):       
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "min_new_tokens": 1,
            "repetition_penalty": 1
            #"Temperature" : 0.7
            # "stop_sequences": ["\n\n"]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"I have this 'division name': {division_name}\n"\
                f"I have 'actual Job Responsibilites' as : {actual_job_responsibilites}, I also have ideal job responsibilities created by you (watsonx):{ideal_job_resp}\n"\
                "Give us the reason why you created this ideal job resposibilites\n"\
                "[/INST]\n"\
                "Output:\n\n"
        generated_response = model.generate_text(prompt=template)
        return generated_response
    
    @staticmethod
    def recommendation(goal,department_name, division_name, actual_job_responsibilites, ideal_job_resp, reasoning, creds = creds, project_id = project_id):       
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 1000,
            "min_new_tokens": 1,
            "repetition_penalty": 1
            #"Temperature" : 0.7
            # "stop_sequences": ["\n\n"]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"I have this 'department name': {department_name}\n"\
                f"I have this 'division name': {division_name}\n"\
                f"I have 'actual Job Responsibilites' as : {actual_job_responsibilites}, I also have ideal job responsibilities created by you (watsonx):{ideal_job_resp}\n"\
                f"I also have actual job responsibilites for anpother division in this department"\
                f"You also create reasons behind your generated ideal job resposibilities{reasoning}\n"\
                "By provided data please generate recommendation for the whole department\n"\
                "[/INST]\n"\
                "Output:\n\n"
        generated_response = model.generate_text(prompt=template)
        return generated_response
    
    #------------------------------- Job Gap and Skill Gap -----------------------
    @staticmethod
    def job_gap(goal, input_jobdesk, input_ideal_jobdesk, creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 3000,
            "min_new_tokens": 1,
            "repetition_penalty": 1,
            #"Temperature" : 0.7
            #"stop_sequences": ["\n\n"]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"generate the response with {goal} as consideration"\
                f"this is a result you generated {input_jobdesk} based on {input_ideal_jobdesk}."\
                "Generate job gap analysis for data provided."\
                "Please generate the answear point by point."\
                "do not generate any recommendation and note."\
                "[/INST]\n"\
                "Output:"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response

    @staticmethod
    def skill_gap(goal,input_jobdesk,input_ideal_jobdesk, creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 3000,
            "min_new_tokens": 1,
            "repetition_penalty": 1,
            #"Temperature" : 0.7
            #"stop_sequences": ["\n\n"]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"this is a result you generated {input_jobdesk} based on {input_ideal_jobdesk}."\
                "Generate skill gap analysis for data provided."\
                "Please generate the answear point by point."\
                "do not generate any recommendation and note."\
                "[/INST]\n"\
                "Output:"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response

    @staticmethod
    def asis_ideal_job_diff(goal,input_jobdesk,input_ideal_jobdesk, creds = creds, project_id = project_id):
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 3000,
            "min_new_tokens": 1,
            "repetition_penalty": 1,
            #"Temperature" : 0.7
            #"stop_sequences": ["\n\n"]
        }
        llama2 = "meta-llama/llama-2-70b-chat"
        model = Model(
                model_id=llama2,
                params=parameters,
                credentials=creds,
                project_id=project_id)
        
        template = "<[INST] «SYS»\n"\
                "while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content.\n"\
                "Please ensure that your responses are socially unbiased and positive in nature.\n"\
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct.\n"\
                "If you don't know the answer to a question, please don't share false information.\n"\
                "«/SYS»\n"\
                f"Generate the response with {goal} as consideration"\
                f"this is a result you generated {input_jobdesk} based on {input_ideal_jobdesk}."\
                f"What specific change was made, transitioning {input_jobdesk} to {input_ideal_jobdesk}."\
                "Please generate the answear point by point."\
                "Do not generate any recommendation and note."\
                "[/INST]\n"\
                "Output:"
 #make a few shot
        # Generate text using the model
        generated_response = model.generate_text(prompt=template)

    # Return the results directly as JSON
        return generated_response