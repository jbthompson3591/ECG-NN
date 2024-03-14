### this part of the code reads the ptbxl_database.csv file in as a list of dictionaries ###
import csv
import wfdb
import ast
import pandas as pd
import numpy as np

def load_csv_as_list_of_dicts(file_path):
    result_list = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            result_list.append(row)
    return result_list

csv_file_path = (
    '/Users/jbthompson/Documents/final_folder/'
    'ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.3/'
    'ptbxl_database.csv'
)

data_as_list_of_dicts = load_csv_as_list_of_dicts(csv_file_path)

path = (
    '/Users/jbthompson/Documents/final_folder/'
    'ptb-xl-a-large-publicly-available-electrocardiography-dataset-1.0.3/'
)

for dict in data_as_list_of_dicts:
    extension = dict['filename_lr']
    data = wfdb.rdsamp(path+extension)[0]
    dict['data'] = data

dlist = data_as_list_of_dicts
new_list = []

for dict in dlist:
    scp_codes = dict['scp_codes']
    scp_codes = ast.literal_eval(scp_codes)
    box =[]
    data = dict['data']
    new_dict = {}
    for key, value in scp_codes.items():
        if value == 100.0:
            box.append(key)
    for item in box:
        new_dict[item] = data
        new_list.append(new_dict)

new_list = []
for dict in dlist:
    scp_codes = dict['scp_codes']
    scp_codes = ast.literal_eval(scp_codes)
    box =[]
    data = dict['data']
    new_dict = {}
    for key, value in scp_codes.items():
        if value == 100.0:
            box.append(key)
    for item in box:
        new_dict[item] = data
        new_list.append(new_dict)

# Load scp_statements.csv for diagnostic aggregation
agg_df = pd.read_csv(path+'scp_statements.csv')
agg_df = agg_df[agg_df.diagnostic == 1]
test = new_list[0]

final_list = []
for dictionary in new_list:
    new_dict = {}
    for key in dictionary:
        data = dictionary[key]
        search_value = key
        result = agg_df[agg_df['name'] == search_value]
        result = result['diagnostic_class']
        result = result.to_string()
        new_dict[result] = data
        final_list.append(new_dict)

new_list_of_dicts = []
# Iterate through the list of dictionaries
for dictionary in final_list:
    # Check if any key contains the substring 'Series'
    has_series_key = any('Series' in key for key in dictionary.keys())
    # If 'Series' key is not present, add the dictionary to the new list
    if not has_series_key:
        new_list_of_dicts.append(dictionary)
# Update the original list with the new list
list_of_dicts = new_list_of_dicts

modified_list_of_dicts = []
for dictionary in list_of_dicts:
    # Create a new dictionary to store modified keys and corresponding values
    modified_dict = {}
    
    # Iterate through each key-value pair in the dictionary
    for key, value in dictionary.items():
        # Strip numbers and blank spaces from the key
        new_key = ''.join(char for char in key if not char.isdigit() and not char.isspace())
        
        # Store the modified key-value pair in the new dictionary
        modified_dict[new_key] = value
    
    # Append the modified dictionary to the new list
    modified_list_of_dicts.append(modified_dict)

values_by_keys = {}

# Iterate through the list of dictionaries
for dictionary in modified_list_of_dicts:
    # Extract the key and value from the dictionary
    key, value = list(dictionary.items())[0]  # Assuming each dictionary contains only one key-value pair
    
    # Add the value to the list corresponding to the key
    if key not in values_by_keys:
        values_by_keys[key] = []
    values_by_keys[key].append(value)

for key, values in values_by_keys.items():
    # Generate a file name based on the key
    filename = f"{key}.npy"
    
    # Save the values to the file
    np.save(filename, np.array(values))

    print(f"Data for key '{key}' saved to {filename}")