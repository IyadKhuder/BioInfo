import os
import pandas as pd

# dtype_specification = {1: str, 2: str, 3: str, 4: str, 5: str, 6: str, 7: str, 8: str, 9: str, 10: str, 11: str, 12: str, 13: str, 14: str, 15: str, 16: str, 17: str, 18: str, 19: str, 20: str, 21: str, 22: str, 23: str, 24: str, str: str, 25: str, 26: str, 27: str, 28: str, 29: str, 30: str, 31: str, 32: str, 33: str, 34: str, 35: str, 36: str, 37: str, 38: str, 39: str, 40: str, 41: str, 42: str, 43: str, 44: str, 45: str, 46: str, 47: str, 48: str, 49: str, 50: str, 51: str, 52: str, 53: str, 54: str, 55: str}
num_columns = 16
dtype_specification = {i: str for i in range(1, num_columns + 1)}

# The number of files
n = 24
dirPath = "Data/HMGULA3/"

# Initialize an empty list to store DataFrames
ExpData_LA_GMC_Control = []


for sn in range(1, n+1):
    filePath = f"{dirPath}/HMGULA_{sn}.csv"
    if os.path.exists(filePath):
        ExpData_Batch = pd.read_csv(filePath, sep=',', dtype = dtype_specification)
        ExpData_LA_GMC_Control.append(ExpData_Batch)

HMGULA_Control_DF3 = pd.concat(ExpData_LA_GMC_Control, ignore_index=True)

HMGULA_Control_DF3.to_csv(f"{dirPath}/_HMGULA_Control_ExpData.csv", index=False)
