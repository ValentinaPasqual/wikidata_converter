import os
import json
import re

# Enter the path to input/output folder
info = ''' 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+   In order to create a unique json file that contain all the individual json-s,   +
+   please provide the "Input" and the "Output" folder!                             +
+   The path should have this format: /home/x_y_z/Dev/wikidata_converter/prova      +
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
print(info)

input_folder_path = str(input('Enter input folder path:> '))
output_folder_path = str(input('Enter output folder path:> '))

# Change the directory
os.chdir(input_folder_path)


# Iterate the folder and save the file names in a list
def iterate_all_file_in_folder(folder_name):
    file_list = os.listdir(folder_name)
    names = []
    for file_name in file_list:
        names.append(file_name)
    return names


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


# Sort the elements of the list
json_files = sorted_alphanumeric(iterate_all_file_in_folder(input_folder_path))


# Merge all individual json files into one unique file
def merge_json_files(filename):
    result = list()
    file_nr = 0
    for f1 in filename:
        with open(f1, 'r') as infile:
            result.append(json.load(infile))
        with open('{0}/final_json_file.json'.format(output_folder_path), 'w') as output_file:
            json.dump(result, output_file)
            file_nr += 1
            print(file_nr)



# Comparing the returned list to empty list
if not os.listdir(output_folder_path):
    merge_json_files(json_files)
else:
    print('Folders contain files, please delete existing file and then run the script!')
