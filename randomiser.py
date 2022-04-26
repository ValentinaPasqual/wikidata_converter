import os
import json
import random

directory_name = "DIRECTORY_PATH_NAME"
directory = os.fsencode(directory_name)

# GETS ELEMENTS FROM DIRECTORY
for file in os.listdir(directory):
    g = rdflib.Graph()
    filename = os.fsdecode(file)
    if filename.endswith(".json"):
        f = open(directory_name + '/' + filename, encoding='utf-8')
        print(filename)
        json_file = json.load(f) # input jsons

predicates_list, entities_list, values_list = [], [], []
for entity in json_file['entities']:
    entities_list.append(entity)
    for predicate in json_file['entities'][entity]['claims']:
        predicates_list.append(predicate)
        values_list = json_file['entities'][entity]['claims'][predicate]['datavalue']['value']
