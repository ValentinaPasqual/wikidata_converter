import os
from random import *
import shutil
import json
import os
import requests
from tqdm import tqdm
from get_artists_and_locs import *
from pathlib import Path


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
    files_count = countfiles(input_path) - 1
    while i <= n:
        random_number, taken_numbers_list = recursive_search_for_int(files_count, taken_numbers_list)
        file_name = file_start_name + str(random_number) + '.json'
        file_path = findfile(file_name, input_path)
        new_path = shutil.copy(file_path, output_path + file_name)
        i +=1
    return taken_numbers_list


def last_entities(input_path, output_path, floor, file_name):
    d, res = {}, {}
    l=[]
    file_path = findfile(file_name, input_path)
    f = open(file_path, encoding='utf-8')
    json_file = json.load(f)  # input jsons
    for entity in json_file['entities']:
        l.append(entity)
    l = l[0:floor]
    for x in l:
        d.update({x:json_file['entities'][x]})
    res.update({'entities': d})
    with open(output_path + file_name, 'w') as f:
        json.dump(res, f, indent=4)

################################ SETTING UP INPUT DATA AND DIRECTORIES ################################


input_path_artworks = str(input('Enter input artworks folder path:> '))
input_path_random = str(input('Enter input random entities folder path:> '))
input_path_fake = str(input('Enter input fake entities folder path:> '))
root_dir = str(input('Enter output folder path:> '))
new_dir = make_directory(root_dir, 'log_data\\')


d1 = make_directory(new_dir, 'D1\\')
d2 = make_directory(new_dir, 'D2\\')
d3 = make_directory(new_dir, 'D3\\')


def artworks_data(data_divisor, input_path, output_path):
    n_artworks_entities = 3537045
    n_entities = int(n_artworks_entities / data_divisor)
    n = int(n_entities / 50)
    floor = n_entities % 50

    print(n, 'selected artwork json files')
    print('#### updating dir ' + output_path + ' with json artworks #####')
    copy_chosen_files(n, input_path, output_path, 'artwork')

    taken_numbers_list = []
    files_count = countfiles(input_path) - 1
    random_number, taken_numbers_list = recursive_search_for_int(files_count, taken_numbers_list)
    last_file_name = 'artwork' + str(random_number) + '.json'

    last_entities(input_path, output_path, floor, last_file_name)

    entities_list = select_data_from_json(output_path)
    prepared_entities_list = wikidata_api_data_preparation(entities_list)
    wikidata_api_requestor(prepared_entities_list, output_path)



def random_data(data_divisor, input_path, output_path):
    n_random_entities = 2999999
    n_entities = int(n_random_entities / data_divisor)
    n = int(n_entities / 50)
    floor = n_entities % 50

    print(n, 'selected random json files')
    print('#### updating dir ' + output_path + ' with jsons random #####')
    copy_chosen_files(n, input_path, output_path, 'entities')

    taken_numbers_list = []
    files_count = countfiles(input_path) - 1
    random_number, taken_numbers_list = recursive_search_for_int(files_count, taken_numbers_list)
    last_file_name = 'entities' + str(random_number) + '.json'

    last_entities(input_path, output_path, floor, last_file_name)


def fake_data(data_divisor, input_path, output_path):
    i = 0
    ent_fa= int(153000)  # da rivedere
    ent_fc = int(176000)   # è sbagliato, per ora è a caso, perchè il dato non c'è su github
    ent_fl = int(203236)   # ok??
    ent = int((ent_fa + ent_fc + ent_fl) / data_divisor) # jsons_number
    n = ent / 200
    floor = ent % 200
    print(n, 'selected fake json files')
    print('#### updating dir ' + output_path + ' with jsons fake #####')
    json_files_list = list(Path(input_path).rglob("*.[jJ][sS][oO][nN]"))
    fake_jsons_path = make_directory(output_path, 'fake_jsons')
    while i <= n:
        file_path = choice(json_files_list)
        shutil.copy(file_path, fake_jsons_path)
        json_files_list.remove(file_path)
        i += 1
    last_path = choice(json_files_list)
    string = str(last_path)
    rel_path = os.path.dirname(last_path) # .split('\\')[-1]
    file_name = string.replace(rel_path, '')
    print(rel_path, file_name)
    # RICORDATI DI CAMBIARE L'INPUT PATH CON LA CARTELLA IN QUESTIONE
    last_entities(rel_path, output_path, floor, file_name.replace('\\', ''))


################################ CALL ALL FUNCTIONS ###################################

# FILL DIRECTORY D1
artworks_data(1000, input_path_artworks, d1)
random_data(1000, input_path_random, d1)
fake_data(1000, input_path_fake, d1)

# FILL DIRECTORY D2
artworks_data(100, input_path_artworks, d2)
random_data(100, input_path_random, d2)
fake_data(100, input_path_fake, d2)


# FILL DIRECTORY D3
artworks_data(10, input_path_artworks, d3)
random_data(10, input_path_random, d3)
fake_data(10, input_path_fake, d3)
