import os
import pandas as pd
# =============================================================================
# dtype_specification = {1: str, 2: str, 3: str, 4: str, 5: str, 6: str, 7: str, 8: str, 9: str, 10: str, 11: str, 12: str, 13: str, 14: str, 15: str, 16: str, 17: str, 18: str, 19: str, 20: str, 21: str, 22: str, 23: str, 24: str, str: str, 25: str, 26: str, 27: str, 28: str, 29: str, 30: str, 31: str, 32: str, 33: str, 34: str, 35: str, 36: str, 37: str, 38: str, 39: str, 40: str, 41: str, 42: str, 43: str, 44: str, 45: str, 46: str, 47: str, 48: str, 49: str, 50: str, 51: str, 52: str, 53: str, 54: str, 55: str}
dtype_specification = {1: str, 2: str, 3: str, 4: str, 5: str, 6: str, 7: str, 8: str, 9: str, 10: str, 11: str, 12: str, 13: str, 14: str, 15: str, 16: str}
# =============================================================================
# Define the number of DataFrames
n = 48
PrimusPath = "ExpData/LA/GMC-Control"

# Initialize an empty list to store DataFrames
ExpData_LA_GMC_Control_DF = []
ExpData_LA_GMC_Control = []


for sn in range(n):
    filePath = f"{PrimusPath}/ExpData_LA_{sn+1}.csv"
    if os.path.exists(filePath):
        ExpData_Batch = pd.read_csv(filePath, sep=',', dtype = dtype_specification)
        ExpData_LA_GMC_Control.append(ExpData_Batch)

ExpData_LA_GMC_Control_DF = pd.concat(ExpData_LA_GMC_Control, ignore_index=True)

ExpData_LA_GMC_Control_DF.to_csv(f"{PrimusPath}/_ExpData_LA_GMC_Control.csv", index=False)
