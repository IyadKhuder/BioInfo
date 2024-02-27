import pandas as pd

def get_key_by_id(dataframe, id_value):

    # Filter the DataFrame to find the row with the given 'id' value
    row = dataframe[dataframe['pipelineId'] == id_value]

    # Check if any rows are returned
    if not row.empty:
        # Extract the 'key' value from the row
        key_value = row.iloc[0]['pipelineKey']
        return key_value
    else:
        # Return None if the 'id' is not found in the DataFrame
        return None




