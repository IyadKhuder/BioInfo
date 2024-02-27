# Importing libraries:
import requests
import pandas as pd
import warnings
from iyad_pck.list_utils import import_csv_as_list, save_list_to_csv

# Mute all warning messages
warnings.filterwarnings("ignore")

dirPath = "Data/HMGULA2/"
EBI_Domain = "https://www.ebi.ac.uk/mi/impc/solr/"
param_query_exp = "experiment/select?q=parameter_stable_id:"

HMGULA_keys = import_csv_as_list(f"{dirPath}HMGULA_keys_list.csv")

# save_list_to_csv(HMGULA_keys, f"{dirPath}/HMGULA_keys_list.csv")
    
filter_q = "phenotyping_center,biological_sample_group,zygosity,pipeline_name,pipeline_stable_id"
filter_q += ",sex,procedure_name,procedure_stable_id,parameter_name,parameter_stable_id"
filter_q += ",observation_type,data_point,strain_name,genetic_background,date_of_experiment"
filter_q += ",specimen_id,observation_type,discrete_point,sub_term_name,sub_term_id"

recordCounter = 0
batch = 5000
paramsDataExp_LA = {}
fileSize = 20000
fileSN = 1
paramsData_list_of_dicts = []
keysn = 0
for param_key in HMGULA_keys:
    page = 1
    keysn += 1
    print("- - - - - - - - - -- - - - - - - - - -")
    print(f"                Param #{keysn}:")
    print(f"= = = = = = {param_key} = = = = = = ")
    potentialData = True
    # While loop to iterate through pages
    while potentialData:
        start_index = (page - 1) * batch
        apiURL_Exp = f"{EBI_Domain}{param_query_exp}{param_key}&rows={batch}&wt=json&start={start_index}"
        apiURL_Exp += f"&fl={filter_q}"
        responseExp = requests.get(apiURL_Exp, verify=False)
        print(f"A new loop of 'while' with start_index: {start_index}")
        print(f"page: {page}")
        print(f"apiURL_Exp: {apiURL_Exp}")

        if responseExp.status_code == 200:
            # Parse the JSON response
            dataLoad = responseExp.json()
            if dataLoad.get("response", {}).get("docs"):
                usefulData = dataLoad["response"]["docs"]
                
                for dItem in usefulData:
                    if dItem['biological_sample_group']=='control':
                        dItem['url_page'] = page
                        paramsData_list_of_dicts.append(dItem)
                        recordCounter += 1
                        print(f"recordCounter: {recordCounter}")
                        if recordCounter >= fileSize:
                            paramsDataExp_LA = pd.DataFrame(paramsData_list_of_dicts)
                            new_column_order = ['parameter_stable_id', 'phenotyping_center', 'biological_sample_group']
                            new_column_order.extend(['pipeline_name', 'pipeline_stable_id', 'procedure_name', 'procedure_stable_id'])
                            new_column_order.extend(['specimen_id','strain_name', 'genetic_background', 'date_of_experiment'])
                            new_column_order.extend(['observation_type','discrete_point','sub_term_name','sub_term_id', 'url_page'])

                            # Reindex the DataFrame with the new column order
                            paramsDataExp_LA = paramsDataExp_LA.reindex(columns=new_column_order)

                            # Save the DataFrame to a CSV file
                            file_name = f"{dirPath}/HMGULA_{fileSN}.csv"
                            paramsDataExp_LA.to_csv(file_name, index=False)
                            fileSN += 1
                            recordCounter = 0
                            paramsData_list_of_dicts = []
    
                if recordCounter >= fileSize:
                    paramsDataExp_LA = pd.DataFrame(paramsData_list_of_dicts)
                    # Save the DataFrame to a CSV file
                    file_name = f"{dirPath}/HMGULA_{fileSN}.csv"
                    paramsDataExp_LA.to_csv(file_name, index=False)
                    fileSN += 1
                    recordCounter = 0
                    paramsData_list_of_dicts = []


                page += 1

            else:
                potentialData = False
                
        else:
            print(f"Error fetching data for parameter {param_key}: {responseExp.status_code}")
            potentialData = False

