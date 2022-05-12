import os
from random import *
import shutil
import json
import os
import requests
from tqdm import tqdm
from get_artists_and_locs import *


# STAMPA UN PO' DI STATS??
# FINIRE PER IL D3
# E GLI ARTWORKS SONO APPOSTO BYEEEEE


def make_directory(parent_dir=None, directory=None):
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    return path

def recursive_search_for_int(n, taken_numbers_list):
    random_number = randint(0,n)
    if random_number not in taken_numbers_list:
        taken_numbers_list.append(random_number)
        return random_number, taken_numbers_list
    else:
        return recursive_search_for_int(n, taken_numbers_list)

def findfile(name, path):
    for dirpath, dirname, filename in os.walk(path):
        if name in filename:
            return os.path.join(dirpath, name)

def copy_chosen_files(n, input_path, output_path, file_start_name):
    i = 0
    taken_numbers_list = []
    while i < n:
        random_number, taken_numbers_list = recursive_search_for_int(n, taken_numbers_list)
        file_name = file_start_name + str(random_number) + '.json'
        file_path = findfile(file_name, input_path)
        shutil.copy(file_path, output_path)
        i +=1




################################ SETTING UP INPUT DATA AND DIRECTORIES ################################

# path of input data (jsons artworks 3'500'000)
input_path = str(input('Enter input folder path:> '))
#input_path = "C:/Users/Valentina/Documents/DHDK/DHARC/PhD/tesi_eduard/dataset/json_artworks_not_really/"

# directory where to save new data
root_dir = str(input('Enter output folder path:> '))
#root_dir = "C:/Users/Valentina/Documents/DHDK/DHARC/PhD/tesi_eduard/dataset/"
new_dir = make_directory(root_dir, 'log_data/')

n_artworks_entities = 3537045
n_of_artworks_jsons = 1999 # change with the number of json file in the input path repository

################################ CALL FUNCTION FOR D1 = 3500ca ENTITIES ################################

################################ CALL FUNCTION FOR D1 - ARTWORKS (ca 3500 Entities) ################################

n_entities_d1 = int(n_artworks_entities / 1000)
n_d1 = int(n_entities_d1 / 50)
d1_output_path = make_directory(new_dir, 'D1/')

print('#### starting filling dir D1 #####')
print(n_entities_d1, 'selected artwork entities')
copy_chosen_files(n_d1, input_path, d1_output_path, 'artwork')

d1_entities_list = select_data_from_json(d1_output_path)
d1_prepared_entities_list = wikidata_api_data_preparation(d1_entities_list)
make_directory(d1_output_path, 'related_entities')
wikidata_api_requestor(d1_prepared_entities_list, d1_output_path + 'related_entities/')

################################ CALL FUNCTION FOR D1 - RUMOR (ca 3500 Entities) ################################



################################ CALL FUNCTION FOR D2 = 3500ca ENTITIES ################################

n_entities_d2 = n_artworks_entities / 100
n_d2 = int(n_entities_d2 / 50)
print('#### starting filling dir D2 #####')
print(n_entities_d2, 'selected artwork entities')
d2_output_path = make_directory(new_dir, 'D2/')
copy_chosen_files(n_d2, input_path, d2_output_path, 'artwork')

d2_entities_list = select_data_from_json(d2_output_path)
d2_prepared_entities_list = wikidata_api_data_preparation(d2_entities_list)
make_directory(d2_output_path, 'related_entities')
wikidata_api_requestor(d2_prepared_entities_list, d2_output_path + 'related_entities/')


################################ CALL FUNCTIONS FOR D3 = 350'000 ARTWORK ENTITIES ################################

n_entities_d3 = n_artworks_entities / 10
n_d3 = int(n_entities_d3 / 50)
d3_output_path = make_directory(new_dir, 'D3/')
copy_chosen_files(n_d3, input_path, d3_output_path, 'artwork')

d3_entities_list = select_data_from_json(d3_output_path)
d3_prepared_entities_list = wikidata_api_data_preparation(d3_entities_list)
make_directory(d3_output_path, 'related_entities')
wikidata_api_requestor(d3_prepared_entities_list, d3_output_path + 'related_entities/')