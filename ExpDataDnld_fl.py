# Importing libraries:
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import signal
from iyad_pck.list_utils import find_duplicates, save_list_to_csv
import logging
# import os
# =============================================================================

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
dirPath = "Data/HMGULA2/"

# =============================================================================
# Defining some constants

IMPC_Domain = "https://api.mousephenotype.org/impress/"
EBI_Domain = "https://www.ebi.ac.uk/mi/impc/solr/"

def download_data(url):
    logger.info(f"Downloading data from URL: {url}")
    try:
        resp = requests.get(url, verify=False)
        resp.raise_for_status()  # Raise exception for non-200 status codes
        param_data = resp.json()
        if param_data.get("response", {}).get("docs"):
            return (url, param_data["response"]["docs"])
        else:
            return (url, None)
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download data from URL: {url}, Error: {e}")
        return (url, None)

def download_data_fl(url, phCenter):
    logger.info(f"Downloading data from URL: {url}")
    try:
        resp = requests.get(url, verify=False)
        resp.raise_for_status()  # Raise exception for non-200 status codes
        param_data = resp.json()
        if param_data.get("response", {}).get("docs"):
            usefulData = param_data["response"]["docs"]
            if usefulData['phenotyping_center']==phCenter:
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

PrimusPath = "ExpData/LA"

# # save_list_to_csv(urlsStats_LA_25k, filePath)

# Read the list of URL's and save them in a list:
urlsExp_EA_25k = pd.read_csv(r"Data/urlsExp_EA_25k.csv", sep=',')
urlsExp_EA_25k = urlsExp_EA_25k.iloc[:, 0].tolist()

urlsExp_LA_25k = pd.read_csv(r"Data/urlsExp_LA_25k.csv", sep=',')
urlsExp_LA_25k = urlsExp_LA_25k.iloc[:, 0].tolist()

print(f"There are {len(urlsExp_LA_25k)} URL's")
# =============================================================================
# This version saves the downloaded data in batches (does not wait until all requests are completed.)
# # Dict to store successful and failed responses
successful_responses = {}
failed_responses = {}

# Set the maximum number of concurrent downloads (adjust as needed)
max_workers = 5
url_counter = 0
load_size = 100
# Create ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Use submit to start the downloads asynchronously
    print(f"url_{url_counter + 1}")
    futures = {executor.submit(download_data_fl, url, 'HMGU'): url for url in urlsExp_LA_25k[1500:5200]}
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
                paramsData_list_of_dicts = []
                for key, value in successful_responses.items():
                    for inner_dict in value:
                        paramsData_list_of_dicts.append(inner_dict)

                # Create a DataFrame from the list of dictionaries
                paramsDataExp_LA = pd.DataFrame(paramsData_list_of_dicts)
                paramsDataExp_LA['url_index'] = url_counter

                # Save the DataFrame to a CSV file
                file_name = f"{PrimusPath}/ExpData_LA_{url_counter // load_size}.csv"
                paramsDataExp_LA.to_csv(file_name, index=False)

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
    paramsDataExp_LA = pd.DataFrame(paramsDataStats_list_of_dicts)
    paramsDataExp_LA['url_index'] = url_counter
    file_name = f"{PrimusPath}/ExpData_LA_{url_counter // load_size + 1}.csv"
    paramsDataExp_LA.to_csv(file_name, index=False)

print(f"There are {len(paramsDataExp_LA)} records")
