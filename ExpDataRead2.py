import os
import pandas as pd

# Folder path
folder_path = 'LA_HMGU'

# =============================================================================
# Initialize an empty list to store DataFrames
exp_category_df_list = []

# Loop through files in the folder
for file_name in os.listdir(folder_path):
    if file_name.startswith('category'):
        # File path
        file_path = os.path.join(folder_path, file_name)
        
        # Read CSV file into a DataFrame
        exp_category = pd.read_csv(file_path)
        
        # Append DataFrame to the list
        exp_category_df_list.append(exp_category)


# Concatenate the list of DataFrames into one DataFrame
exp_category_df = pd.concat(exp_category_df_list, ignore_index=True)


# =============================================================================
# Initialize an empty list to store DataFrames
exp_ontology_df_list = []

# Loop through files in the folder
for file_name in os.listdir(folder_path):
    if file_name.startswith('ontology'):
        file_path = os.path.join(folder_path, file_name)
        
        # Read CSV file into a DataFrame
        exp_ontology = pd.read_csv(file_path)
        
        # Append DataFrame to the list
        exp_ontology_df_list.append(exp_ontology)


# Concatenate the list of DataFrames into one DataFrame
exp_ontology_df = pd.concat(exp_ontology_df_list, ignore_index=True)


# =============================================================================
# Initialize an empty list to store DataFrames
exp_time_series_df_list = []

# Loop through files in the folder
for file_name in os.listdir(folder_path):
    if file_name.startswith('time_series'):
        file_path = os.path.join(folder_path, file_name)
        
        # Read CSV file into a DataFrame
        exp_time_series = pd.read_csv(file_path)
        
        # Append DataFrame to the list
        exp_time_series_df_list.append(exp_time_series)


# Concatenate the list of DataFrames into one DataFrame
exp_time_series_df = pd.concat(exp_time_series_df_list, ignore_index=True)

# =============================================================================
# Initialize an empty list to store DataFrames
exp_unidimensional_df_list = []

# Loop through files in the folder
for file_name in os.listdir(folder_path):
    if file_name.startswith('unidimensional'):
        file_path = os.path.join(folder_path, file_name)
        
        # Read CSV file into a DataFrame
        exp_unidimensional = pd.read_csv(file_path)
        
        # Append DataFrame to the list
        exp_unidimensional_df_list.append(exp_unidimensional)


# Concatenate the list of DataFrames into one DataFrame
exp_unidimensional_df = pd.concat(exp_unidimensional_df_list, ignore_index=True)



# =============================================================================
# Initialize an empty list to store DataFrames
exp_unidimensional_df_list = []

# Loop through files in the folder
for file_name in os.listdir(folder_path):
    if file_name.startswith('unidimensional'):
        file_path = os.path.join(folder_path, file_name)
        
        # Read CSV file into a DataFrame
        exp_unidimensional = pd.read_csv(file_path)
        
        # Append DataFrame to the list
        exp_unidimensional_df_list.append(exp_unidimensional)


# Concatenate the list of DataFrames into one DataFrame
exp_unidimensional_df = pd.concat(exp_unidimensional_df_list, ignore_index=True)




