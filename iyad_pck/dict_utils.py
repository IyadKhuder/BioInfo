import requests
import json
import csv
import os

def pretty_print_dict(my_dict):
    # Use json.dumps with indent parameter for pretty printing
    pretty_dict = json.dumps(my_dict, indent=4)
    
    # Print the formatted dictionary
    print(pretty_dict)

def print_first_n_items(dictionary, n):
    items_to_print = list(dictionary.items())[:n]
    for key, value in items_to_print:
        print(key)
        pretty_print_dict(value)

def save_dict_to_csv(dictionary, filePath):
    # Get the absolute path of the filename
    abs_path = os.path.abspath(filePath)

    if os.path.exists(abs_path):
        user_input = input(f"The file {abs_path} already exists. \nDo you want to overwrite it? (y/n): ").lower()
        if user_input != 'y':
            print("File not overwritten. Exiting.")
            return
                    
    with open(abs_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Key', 'Value'])  # Write header row

        for key, value in dictionary.items():
            csv_writer.writerow([key, value])

    if os.path.exists(abs_path):
        print(f"The dictionary has been saved to {abs_path}.")

def save_dict_to_json(dictionary, filePath):
    # Get the absolute path of the filename
    abs_path = os.path.abspath(filePath)

    if os.path.exists(abs_path):
        user_input = input(f"The file {abs_path} already exists. \nDo you want to overwrite it? (y/n): ").lower()
        if user_input != 'y':
            print("File not overwritten. Exiting.")
            return
                    
    with open(abs_path, 'w') as json_file:
        json.dump(dictionary, json_file, indent=2)

    if os.path.exists(abs_path):
        print(f"The dictionary has been saved to {abs_path}.")

