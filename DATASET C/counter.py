import json
import os

directory_name = 'E:/Datasets/D4_fake'
directory = os.fsencode(directory_name)


def counter(json_file):
    entities_list, statements_list = [], []
    for entity in json_file['entities']:
        entities_list.append(entity)
        for predicate in json_file['entities'][entity]['claims']:
            for claim in json_file['entities'][entity]['claims'][predicate]:
                statements_list.append(claim['id'])
    n_entities = len(entities_list)
    n_statements = len(statements_list)
    return n_entities, n_statements

tot_ne, tot_ns = int(), int()
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".json") and filename.startswith('author'):
        f = open(directory_name + '/' + filename, encoding='utf-8')
        json_file = json.load(f) # input jsons
        ne, ns = counter(json_file)
        tot_ne += ne
        tot_ns += ns
        
print(tot_ne, tot_ns)

