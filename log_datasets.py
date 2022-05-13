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

def countfiles(path):
    for dirpath, dirname, filename in os.walk(path):
        return len(filename)

def findfile(name, path):
    for dirpath, dirname, filename in os.walk(path):
        if name in filename:
            return os.path.join(dirpath, name)

def copy_chosen_files(n, input_path, output_path, file_start_name):
    i = 0
    taken_numbers_list = []
    while i < n:
        files_count = countfiles(input_path)
        random_number, taken_numbers_list = recursive_search_for_int(files_count, taken_numbers_list)
        file_name = file_start_name + str(random_number) + '.json'
        file_path = findfile(file_name, input_path)
        new_path = shutil.copy(file_path, output_path + file_name)
        i +=1


# C:/Users/Valentina/Documents/DHDK/DHARC/PhD/tesi_eduard/dataset/dataset_sample


################################ SETTING UP INPUT DATA AND DIRECTORIES ################################


input_path_artworks = str(input('Enter input artworks folder path:> '))
input_path_random = str(input('Enter input random entities folder path:> '))
input_path_fake = str(input('Enter input fake entities folder path:> '))
root_dir = str(input('Enter output folder path:> '))
new_dir = make_directory(root_dir, 'log_data\\')



def artworks_data(data_divisor, directory_name, input_path_artworks):
    n_artworks_entities = 3537045
    n_entities = int(n_artworks_entities / data_divisor)
    n = int(n_entities / 50)
    output_path = make_directory(new_dir, str(directory_name + '\\'))

    print('#### starting filling dir ' + directory_name + ' #####')
    print(n_entities, 'selected artwork entities')
    copy_chosen_files(n, input_path_artworks, output_path, 'artwork')

    #entities_list = select_data_from_json(output_path)
    #prepared_entities_list = wikidata_api_data_preparation(entities_list)
    #make_directory(output_path, 'related_entities')
    #wikidata_api_requestor(prepared_entities_list, output_path + 'related_entities/')

    return output_path


d1_path = artworks_data(1000, 'D1', input_path_artworks)
d2_path = artworks_data(100, 'D2', input_path_artworks)
#d3_path = artworks_data(10, 'D3', input_path_artworks)


def random_data(data_divisor, output_path, input_path_random):
    n_random_entities = 2999999
    n_entities = int(n_random_entities / data_divisor)
    n = int(n_entities / 50)

    print('#### starting filling dir #####')
    print(n_entities, 'selected random entities')
    copy_chosen_files(n, input_path_random, output_path, 'entities')

random_data(1000, d1_path, input_path_random)
random_data(100, d2_path, input_path_random)
#random_data(10, d3_path, input_path_random)

def fake_data(data_divisor, output_path, input_path_fake):
    n_fake_authors = int(996679 / data_divisor)
    n_fake_creators = int(50000/ data_divisor)   # è sbagliato, per ora è a caso, perchè il dato non c'è su github
    n_fake_locations = int(203236 / data_divisor)
    n_authors = int(n_fake_authors / 200)
    n_creators = int(n_fake_creators / 200)
    n_locations = int(n_fake_locations / 200)
    print('#### starting filling dir #####')
    print(n_authors, 'selected fake authors entities')
    print(n_creators, 'selected fake creators entities')
    print(n_locations, 'selected fake locations entities')
    fake_jsons_path = make_directory(output_path, 'fake_jsons')
    copy_chosen_files(n_authors, input_path_random + 'authors/', fake_jsons_path, 'author')
    copy_chosen_files(n_creators, input_path_random + 'creators/', fake_jsons_path, 'creator')
    copy_chosen_files(n_locations, input_path_random + 'locations/', fake_jsons_path, 'location')

fake_data(1000, d1_path, input_path_fake)

