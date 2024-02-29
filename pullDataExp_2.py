import requests
import pandas as pd
from iyad_pck.list_utils import import_csv_as_list
import warnings

# Mute all warning messages
warnings.filterwarnings("ignore")

dirPath = "Data/HMGULA4/"
EBI_Domain = "https://www.ebi.ac.uk/mi/impc/solr/"
param_query_exp = "experiment/select?q=parameter_stable_id:"

HMGULA_keys = import_csv_as_list(f"{dirPath}HMGULA_keys_list.csv")

filter_q = (
    "phenotyping_center,biological_sample_group,zygosity,pipeline_name,pipeline_stable_id,"
    "sex,procedure_name,procedure_stable_id,parameter_name,parameter_stable_id,"
    "data_point,strain_name,genetic_background,date_of_experiment,"
    "specimen_id,category,observation_type,discrete_point,sub_term_name,sub_term_id"
)

recordCounter = 0
batch = 500
fileSN = 1
paramsData_list_of_dicts = []
# file_list = []

for keysn, param_key in enumerate(HMGULA_keys, start=1):
    page = 1
    print("-" * 45)
    print(f" - Param #{keysn}:")
    print(f"= = = = = = {param_key} = = = = = = ")
    
    while True:
        start_index = (page - 1) * batch
        apiURL_Exp = (
            f"{EBI_Domain}{param_query_exp}{param_key}&rows={batch}&wt=json&start={start_index}&fl={filter_q}"
        )
        responseExp = requests.get(apiURL_Exp, verify=False)
        print(f"A new loop of 'while' with start_index: {start_index}")
        print(f"page: {page}")
        print(f"apiURL_Exp: {apiURL_Exp}")

        if responseExp.status_code == 200:
            dataLoad = responseExp.json()
            if dataLoad.get("response", {}).get("docs"):
                usefulData = dataLoad["response"]["docs"]
                
                for dItem in usefulData:
                    if dItem['biological_sample_group'] == 'control':
                        dItem['url_page'] = page
                        paramsData_list_of_dicts.append(dItem)
                        recordCounter += 1
                        print(f"recordCounter: {recordCounter}")                        

                paramsDataExp_LA = pd.DataFrame(paramsData_list_of_dicts)

                file_name = f"{dirPath}/HMGULA_{fileSN}.csv"
                # file_list.append(file_name)
                # Save the obtained dataframe into a CSV file
                paramsDataExp_LA.to_csv(file_name, index=False)
                fileSN += 1
                recordCounter = 0
                paramsData_list_of_dicts = []

                page += 1
            else:
                break
        else:
            print(f"Error fetching data for parameter {param_key}: {responseExp.status_code}")
            break
