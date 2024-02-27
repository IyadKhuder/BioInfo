# In[1]:

# Importing libraries:
import pandas as pd
import os

# =============================================================================
import logging
dtype_specification = {1: str, 2: str, 3: str, 4: str, 5: str, 6: str, 7: str, 8: str, 9: str, 10: str, 11: str, 12: str, 13: str, 14: str, 15: str, 16: str, 17: str, 18: str, 19: str, 20: str, 21: str, 22: str, 23: str, 24: str, str: str, 25: str, 26: str, 27: str, 28: str, 29: str, 30: str}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
n = 350
PremusPath = "StatData"

# Initialize an empty list to store DataFrames
StatsData_LA_byParam = []
StatsData_LA_byParam_DF = []

for sn in range(n):
    batchName = f"StatData/StData_LA_{sn+1}"
    file_path = f"{batchName}.csv"
    if os.path.exists(file_path):
        StatsData_Batch = pd.read_csv(f"{batchName}.csv", sep=',', dtype = dtype_specification)
        StatsData_LA_byParam.append(StatsData_Batch)

StatsData_LA_byParam_DF = pd.concat(StatsData_LA_byParam, ignore_index=True)

StatsData_LA_byParam_DF.to_csv(f"{PremusPath}/_StatsData_LA_byParam.csv", index=False)

# StatsData_LA_IMG = StatsData_LA_byParam_DF[StatsData_LA_byParam_DF['phenotyping_center']=='CCP-IMG' ]
