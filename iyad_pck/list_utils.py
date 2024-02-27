import requests
import json
import csv
import os

def find_duplicates(input_list):
    unique_values = sorted(list(set(input_list)))
    duplicates = len(input_list) - len(unique_values)

    if duplicates == 0:
        print("No duplicates found.")
    else:
        print(f"{duplicates} duplicate(s) found.")
        print(f"Number of unique values: {len(unique_values)}")
    
    return unique_values

def save_list_to_csv(data_list, filePath):
    # Get the absolute path of the filename
    abs_path = os.path.abspath(filePath)

    if os.path.exists(abs_path):
        user_input = input(f"The file {abs_path} already exists. Do you want to overwrite it? (y/n): ").lower()
        if user_input != 'y':
            print("File not overwritten. Exiting.")
            return
                    
    with open(abs_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Value'])  # Write header row

        for value in data_list:
            csv_writer.writerow([value])
            
    if os.path.exists(abs_path):
        print(f"The list has been saved to: {filePath}.")

def import_csv_as_list(file_path):
    data = []
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.extend(row)
    return data
