# In[1]:

# Importing libraries:
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import signal
from iyad_pck.list_utils import find_duplicates, save_list_to_csv

# =============================================================================
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# Defining some constants

IMPC_Domain = "https://api.mousephenotype.org/impress/"
EBI_Domain = "https://www.ebi.ac.uk/mi/impc/solr/"


def download_data(url):
    logger.info(f"Downloading data from URL: {url}")
    try:
        resp = requests.get(url)
        resp.raise_for_status()  # Raise exception for non-200 status codes
        param_data = resp.json()
        if param_data.get("response", {}).get("docs"):
            return (url, param_data["response"]["docs"])
        else:
            return (url, None)
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download data from URL: {url}, Error: {e}")
        return (url, None)

# =============================================================================
# Function to handle interrupt signal
def handle_interrupt(signal, frame):
    print("Interrupt signal received. Stopping execution...")
    executor.shutdown(wait=False)


# Register the signal handler
signal.signal(signal.SIGINT, handle_interrupt)
# In[2]:
    
filePath = "Data/whole_df.csv"
whole_df = pd.read_csv(filePath, sep=',')

# In[2]:

# A simplified version of the whole_df:
wdf = whole_df[['parameterId', 'parameterKey', 'pipelineType']]

# In[2]:

whole_df_fields = whole_df.columns.tolist()

# In[2]:

params_Comments = whole_df[whole_df['parameterName'].isin(['Comment', 'Comments (in English)', 'Gait comment']) ]

# In[2]:  

# ====== This block can be skipped if wdf_EA_l and wdf_LA_l files are already available =====================
# Filter out alternative parameters:
# wdf_paramm:  the Main parameters, extracted from wdf

# wdf_paramm = wdf[~wdf['parameterKey'].str.startswith('ALT')]

# wdf_EA = wdf_paramm[wdf_paramm['pipelineType']=='Early Adult']
# wdf_EA_l = wdf_EA.iloc[:, 1].tolist()

# wdf_LA = wdf_paramm[wdf_paramm['pipelineType']=='Late Adult']
# wdf_LA_l = wdf_LA.iloc[:, 1].tolist()

# allParamKey_list = wdf_LA_l + wdf_EA_l
# allParamKey_list = list(set(allParamKey_list))

# save_list_to_csv(allParamKey_list, "Data/allParamKey_list.csv")
# # wdf_EA.to_csv("Data/wdf_EA.csv", index = False)
# # wdf_LA.to_csv("Data/wdf_LA.csv", index = False)
# # 
# save_list_to_csv(wdf_EA_l, "Data/wdf_EA_l.csv")
# save_list_to_csv(wdf_LA_l, "Data/wdf_LA_l.csv")

# 
# =============================================================================
# In[12]:

# if wdf_EA_l & wdf_LA_l files are not there, get them from the above block 
wdf_EA_l = pd.read_csv("Data/wdf_EA_l.csv", sep=',')
wdf_LA_l = pd.read_csv("Data/wdf_LA_l.csv", sep=',')

wdf_EA_l = wdf_EA_l.iloc[:, 0].tolist()
wdf_LA_l = wdf_LA_l.iloc[:, 0].tolist()

# In[12]:

# Filtering the param keys belonging to HMGU pheno-center

HMGULA_keys = wdf_LA_l[wdf_LA_l.iloc[:,0].str.startswith('HMGU')]
HMGULA_keys_list = HMGULA_keys.iloc[:, 0].tolist()

save_list_to_csv(HMGULA_keys_list, "Data/HMGULA_keys_list.csv")

# This block generates a list of URL's  for the above lists of parameters
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 

# paging
param_query_stats = "statistical-result/select?q=parameter_stable_id:"
param_query_exp = "experiment/select?q=parameter_stable_id:"

# List to store the parameters urls
urlsStats_EA_100k = []
url_id = 0
batch = 1000
num_pages = 100
# sample
# CBC_parameter_keys_list_u = ['BCMLA_CBC_001_001', 'BCMLA_CBC_002_001']

filter_q = "colony_id,effect_size,female_control_mean,female_ko_effect_p_value,female_ko_parameter_estimate"
filter_q += ",zygosity,genotype_effect_p_value,genotype_effect_parameter_estimate,male_control_mean"
filter_q += ",male_ko_effect_p_value,male_ko_parameter_estimate,male_mutant_mean,male_percentage_change"
filter_q += ",p_value,parameter_name,parameter_stable_id,phenotyping_center,pipeline_stable_id,marker_symbol"
filter_q += ",female_percentage_change,genetic_background,procedure_stable_key,procedure_name,female_mutant_mean"
filter_q += ",pipeline_name,strain_name,parameter_stable_key,pipeline_stable_key,procedure_stable_id"

# Iterate through each pipeline ID
for param_key in wdf_EA_l:
    page = 1
    # While loop to iterate through pages
    while page <= num_pages:
        start_index = (page - 1) * batch
        apiURL_Stats = f"{EBI_Domain}{param_query_stats}{param_key}&rows={batch}&wt=json&start={start_index}"
        # apiURL_Exp = f"{EBI_Domain}{param_query_exp}{param_key}&rows={batch}&wt=json&start={start_index}"
        apiURL_Stats += f"&fl={filter_q}"

        # Append the parameter data to the urls list
        urlsStats_EA_100k.append(apiURL_Stats)

        print(f"=> urlsStats_EA_100k #{url_id} =  {urlsStats_EA_100k[url_id]}")
        # print(f"=> urlsExp_50_50 #{url_id} =  {urlsExp_50_50[url_id]}")

        # Increment page number
        page += 1
        url_id += 1


PremusPath = r"\\primus.img.local\data\83_BIOINFORMATICS\Iyad\CBC_procedure_analysis"
filePath = PremusPath + r'\StatData\urlsStats_EA_100k.csv'

# save_list_to_csv(urlsStats_EA_100k, filePath)

urlsStats_EA_100k = pd.read_csv("Data/urlsStats_EA_100k.csv", sep=',')

# In[15]

urlsStats_EA_100k = urlsStats_EA_100k.iloc[:, 0].tolist()

# =============================================================================

# # # This version saves the downloaded data in batches (does not wait until all requests are completed.)
PremusPath = r'\\primus.img.local\data\83_BIOINFORMATICS\Iyad\CBC_procedure_analysis\StatData\\'
Dir = 'StatData/'
# Dict to store successful and failed responses
successful_responses = {}
failed_responses = {}

# Set the maximum number of concurrent downloads (adjust as needed)
max_workers = 10
url_counter = 0
load_size = 1000
# Create ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Use submit to start the downloads asynchronously
    print(f"url_{url_counter+1}")
    futures = {executor.submit(download_data, url): url for url in urlsStats_EA_100k}
    try:
        for future in as_completed(futures):  # Use as_completed directly
            url = futures[future]
            try:
                data = future.result()
                if data[1] is not None:
                    successful_responses[data[0]] = data[1]
                else:
                    failed_responses[data[0]] = "No data retrieved"
            except Exception as e:
                failed_responses[url] = str(e)
                
            url_counter += 1

            # Check if it's time to save a batch of downloaded data
            if url_counter % load_size == 0:
                # Convert the dictionary into a list of dictionaries
                paramsDataStats_list_of_dicts = []
                for key, value in successful_responses.items():
                    for inner_dict in value:
                        paramsDataStats_list_of_dicts.append(inner_dict)

                # Create a DataFrame from the list of dictionaries
                paramsDataStats_EA = pd.DataFrame(paramsDataStats_list_of_dicts)
                paramsDataStats_EA['url_index'] = url_counter
                
                # Save the DataFrame to a CSV file
                file_name = f"{Dir}StData_EA_{url_counter // load_size}.csv"
                paramsDataStats_EA.to_csv(file_name, index=False)
                
                # Clear successful_responses to start fresh for the next batch
                successful_responses = {}


    except KeyboardInterrupt:
        print("Interrupt signal received. Stopping execution...")
        executor.shutdown(wait=False)

# Convert the remaining successful responses into a DataFrame and save
paramsDataStats_list_of_dicts = []
for key, value in successful_responses.items():
    for inner_dict in value:
        paramsDataStats_list_of_dicts.append(inner_dict)

if paramsDataStats_list_of_dicts:
    paramsDataStats_EA = pd.DataFrame(paramsDataStats_list_of_dicts)
    paramsDataStats_EA['url_index'] = url_counter
    file_name = f"{Dir}StData_EA_{url_counter // load_size + 1}.csv"
    paramsDataStats_EA.to_csv(file_name, index=False)

# Create a DataFrame from the list of dictionaries
# paramsDataStats_EA = pd.DataFrame(paramsDataStats_list_of_dicts)
# paramsDataStats_EA.to_csv("Data/paramsDataStats_EA.csv", index=False)

# In[13]

# # # This version only saves the downloaded data when all requests and batches are compelted.

# Dict to store successful and failed responses
successful_responses = {}
failed_responses = {}

# Set the maximum number of concurrent downloads (adjust as needed)
max_workers = 3

# Create ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Use submit to start the downloads asynchronously
    futures = {executor.submit(download_data, url): url for url in urlsStats_EA_100k}
    try:
        for future in as_completed(futures):  # Use as_completed directly
            url = futures[future]
            try:
                data = future.result()
                if data[1] is not None:
                    successful_responses[data[0]] = data[1]
                else:
                    failed_responses[data[0]] = "No data retrieved"
            except Exception as e:
                failed_responses[url] = str(e)

    except KeyboardInterrupt:
        print("Interrupt signal received. Stopping execution...")
        executor.shutdown(wait=False)

# Convert the dictionary into a list of dictionaries
paramsDataStats_list_of_dicts = []
for key, value in successful_responses.items():
    for inner_dict in value:
        paramsDataStats_list_of_dicts.append(inner_dict)

# Create a DataFrame from the list of dictionaries
paramsDataStats_EA = pd.DataFrame(paramsDataStats_list_of_dicts)
paramsDataStats_EA.to_csv("Data/paramsDataStats_EA.csv", index=False)

# =============================================================================
# # In[15]
# 
# allParamsStats_LA.to_csv("Data/paramsStats1k_LA.csv", index=False)
# # Connect to the SMB share
# with smbclient.SambaClient(server=share_path, username=username, password=password, domain=domain) as client:
#     # Now you can perform file operations using the client
#     filePath = r'\StatData\file.csv'
#     save_list_to_csv(urlsStats_EA, filePath)
# 
# =============================================================================

# In[15]

# This version is enriched with a 
# Dict to store the parameters dataKeyboardInterrupt feature. Last update: 11 Feb.
# =============================================================================
# paramsDataStats_EA = {}
# max_workers = 2
# 
# # Create ThreadPoolExecutor
# with ThreadPoolExecutor(max_workers=max_workers) as executor:
#     # Use submit to start the downloads asynchronously
#     futures = {executor.submit(download_data, url): url for url in urlsStats_EA}
# 
#     try:
#         # Wait for all downloads to complete
#         wait(futures)
#     except KeyboardInterrupt:
#         # If KeyboardInterrupt (Ctrl+C) is received, handle the interrupt
#         print("Interrupt signal received. Stopping execution...")
#         executor.shutdown(wait=False)
# 
#     # Collect results from completed futures
#     paramsDataStats_EA = {url: future.result() for future, url in futures.items() if future.result() is not None}
# 
# =============================================================================
# In[15]

