# # - - - - - Analysis of the experimental data for the combination (LA, GMC, Control) - - - - -

# Importing libraries:
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
# from iyad_pck.list_utils import find_duplicates, save_list_to_csv

# In[2]

# This enriched version of generate_random_colors() avoids colors that are 
# too light for the white background (or too dark for a dark theme)
def genRandomColorsRich(num_colors, min_luminance=0.1, max_luminance=0.9):
    colors = []
    while len(colors) < num_colors:
        color = '#%06X' % np.random.randint(0x000000, 0xFFFFFF)
        luminance = calculate_luminance(color)
        if min_luminance <= luminance <= max_luminance:
            colors.append(color)
    return colors

# Function to calculate the luminance of a color
def calculate_luminance(color):
    r, g, b = int(color[1:3], 16) / 255, int(color[3:5], 16) / 255, int(color[5:7], 16) / 255
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance

# In[3]

# Generate random colors
def generate_random_colors(num_colors):
    return ['#%06X' % np.random.randint(0x111111, 0xEEEEEE) for _ in range(num_colors)]


def count_and_histogram(df_name, yField, topN, plot_title=None, y_tick_interval=None, show_grid=False, y_label='Count', show_count_on_bars=False):
    # Count the occurrences of each unique value of 'yField'
    parameter_counts = df_name[yField].value_counts()
    
    countByField = parameter_counts.sort_values(ascending=False)
    
    countByField = countByField[:topN]
    
    parameterCounts = df_name[yField].value_counts()
    
    countByField = parameterCounts.sort_values(ascending=False)
    
    countByField = countByField[:topN]
        
    topList = countByField.index.tolist()

    # Mapping each pipeline name with a unique color
    colorSet = genRandomColorsRich(len(topList))
    mapping = dict(zip(topList, colorSet))

    colors = [mapping.get(y, 'skyblue') for y in countByField.index]


    plot_w = math.ceil(topN / 2) + 5   
    # Plotting the histogram
    plt.figure(figsize=(plot_w, 6))  # Adjust the figure size as needed
    plt.bar(countByField.index, countByField.values, color=colors)  # Use index and values for x and y values

    if plot_title is not None:
        plt.title(plot_title)
    else:
        plt.title(f'Count of Unique Values for {yField}. Showing the top {topN}')

    if y_tick_interval is not None:
        plt.yticks(range(0, int(max(countByField.values)) + 1, y_tick_interval))
    
    if show_grid:
        plt.grid(True)  # Display grid

    plt.xlabel(yField)

    if y_label is not None:
        plt.ylabel(y_label)
    else:
        plt.ylabel('Count')


    bars = plt.bar(countByField.index, countByField.values, color=colors)

    if show_count_on_bars:
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom')

    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()

# # = = = = = Plotting both histograms in one figure  = = = = = 
# =============================================================================

def histogram_subplots(df_1, df_2, yField, topN, plot_title1=None, plot_title2=None, show_grid=False):    
   
    plt.figure(figsize=(10, 12)) 
    
    parameterCounts_EA = df_1[yField].value_counts()
    parameterCounts_LA = df_2[yField].value_counts()
    
    countByField_LA = parameterCounts_LA.sort_values(ascending=False)
    countByField_EA = parameterCounts_EA.sort_values(ascending=False)
    
    countByField_LA = countByField_LA[:topN]
    countByField_EA = countByField_EA[:topN]
        
    topList = countByField_LA.index.tolist() + countByField_EA.index.tolist()
    topList = list(set(topList))

    # Mapping each pipeline name with a unique color
    colorSet = genRandomColorsRich(len(topList))
    mapping = dict(zip(topList, colorSet))

    colors_LA = [mapping.get(y, 'skyblue') for y in countByField_LA.index]
    colors_EA = [mapping.get(y, 'skyblue') for y in countByField_EA.index]

    # Plot for df_1
    plt.subplot(2, 1, 1)  # 2 rows, 1 column, subplot 1
    plt.bar(countByField_EA.index, countByField_EA.values, color=colors_EA)  # Use index and values for x and y values
    
    if plot_title1 is not None:
        plt.title(plot_title1)
    else:
        plt.title(f'EA pipelines - Count of Unique {yField}. Showing the top {topN}')

    if show_grid:
        plt.grid(True)  # Display grid

    
    plt.xlabel(yField)
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
    
    # Plot for df_2
    plt.subplot(2, 1, 2)  # 2 rows, 1 column, subplot 2
    plt.bar(countByField_LA.index, countByField_LA.values, color=colors_LA)  # Use index and values for x and y values
    
    if show_grid:
        plt.grid(True)  # Display grid
    
    if plot_title2 is not None:
        plt.title(plot_title2)
    else:
        plt.title(f'LA pipelines - Count of Unique {yField}. Showing the top {topN}')

    plt.xlabel(yField)
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
    # = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
    
    plt.tight_layout()  # Adjust layout to prevent clipping of labels
    plt.show()

    
# ======= Load the parameters Data of EA & LA pipelines  =======================
dirPath = "Data/HMGULA4/"
filePath = f"{dirPath}_HMGULA_Cntrl_Exp4.csv"
ExpData = pd.read_csv(filePath, sep=',')

# ======= Group by parameters and count  =======================

paramCounts = ExpData['parameter_stable_id'].value_counts()

countByParam = paramCounts.sort_values(ascending=False)

countByParam_df = countByParam.to_frame().reset_index()

# Rename the columns
countByParam_df.columns = ['paramKey', 'count']

# ==============================


# Check for duplicates based on the combination of all columns
duplicate_rows = ExpData[ExpData.duplicated(keep=False)]

# Print the duplicate rows, if any
if not duplicate_rows.empty:
    print("Duplicate rows based on the combination of all columns:")
    print(duplicate_rows)
else:
    print("No duplicate rows based on the combination of all columns.")

# ==============================
fields_list = ExpData.columns.tolist()

columns = [
    'parameter_stable_id', 'parameter_name', 'phenotyping_center', 'biological_sample_group', 'zygosity',
    'sex', 'pipeline_name', 'pipeline_stable_id', 'procedure_name', 'procedure_stable_id',
    'specimen_id', 'strain_name', 'genetic_background', 'data_point', 'date_of_experiment',
    'observation_type', 'category', 'discrete_point', 'sub_term_name', 'sub_term_id',
]

ExpData_uniq = ExpData.drop_duplicates(columns)

# count_and_histogram for 'parameter_name':
topN = 2
plot_title1 = "Comparison between the number of males and females in the experimental data for LA pipelines, at GMC phenotype center, for the control samples"
y_label1 = "Count of females/males"
count_and_histogram(ExpData, 'sex', topN, plot_title1, None, True, y_label1, True)

# =============================================================================
# In[13]:

fieldsList= ExpData.columns.tolist()
print(fieldsList)


unique_param = ExpData['parameter_stable_id'].unique()

unique_param_list = unique_param.tolist()

# In[18]:

topN = 30
count_and_histogram(ExpData, 'parameter_name', 30)
plot_title1 = f"The frequency of top {topN} parameters in the experimental data for LA pipelines, at GMC phenotype center, for the control samples"
y_label1 = "frequency in the exp. data"

count_and_histogram(ExpData, 'parameter_name', 30, plot_title1, None, True, y_label1)



# In[19]:

# count_and_histogram for 'zygosity':
count_and_histogram(ExpData, 'zygosity', 3)



# In[20]:

# count_and_histogram for 'pipeline_name':
count_and_histogram(ExpData, 'pipeline_name', 40)

# In[21]:

# count_and_histogram for 'project_name':
count_and_histogram(ExpData, 'project_name', 40)


# In[22]:

# Extract unique values of 'parameter_name'
unique_parameters = ExpData['parameter_name'].unique()

# Initialize an empty DataFrame to store 'parameter_name' and 'center_count'
rows = []
# center_per_parameter = pd.DataFrame(columns=['parameter_name', 'center_count'])

# Iterate over unique parameters
for parameter in unique_parameters:
    # Count the number of unique centers for each parameter
    center_count = ExpData[ExpData['parameter_name'] == parameter]['phenotyping_center'].nunique()
    # Append the parameter and its center count to the DataFrame
   
    rows.append({'parameter_name': parameter, 'center_count': center_count})

center_per_parameter = pd.DataFrame(rows)
# Sort the DataFrame by 'center_count' in descending order
center_per_parameter = center_per_parameter.sort_values(by='center_count', ascending=False)

