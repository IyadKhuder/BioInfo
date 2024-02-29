import os
import pandas as pd

num_columns = 21
dtype_specification = {i: str for i in range(1, num_columns + 1)}

# The number of files
n = 1230
dirPath = "Data/HMGULA4/"

# Initialize an empty list to store DataFrames
ExpData_LA_GMC_Control = []


for sn in range(1, n+1):
    filePath = f"{dirPath}/HMGULA_{sn}.csv"
    if os.path.exists(filePath):
        ExpData_Batch = pd.read_csv(filePath, sep=',', dtype = dtype_specification)
        ExpData_LA_GMC_Control.append(ExpData_Batch)

HMGULA_Control_DF4 = pd.concat(ExpData_LA_GMC_Control, ignore_index=True)

HMGULA_Control_DF4.to_csv(f"{dirPath}/_HMGULA_Cntrl_Exp4.csv", index=False)


