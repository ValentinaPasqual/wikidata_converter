import os
import json
import re

# Enter the path to input/output folder
info = ''' 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Rename the files in the folders                         +
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
print(info)

input_folder_path = str(input('Enter input folder path:> '))
name = str(input('Enter name:> '))
#/home/yoda/authors/
#/home/yoda/creators/
#/home/yoda/locations/

# Change the directory
os.chdir(input_folder_path)


# Iterate the folder and save the file names in a list
def iterate_all_file_in_folder(folder_name):
    file_list = os.listdir(folder_name)
    index = 0
    for file_name in file_list:
        first_part = name + str(index) + '.json'
        os.rename(file_name, first_part)
        index += 1;

iterate_all_file_in_folder(input_folder_path)