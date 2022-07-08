import json
import os
import requests
from tqdm import tqdm

def select_data_from_json(directory_name):
    entities_list = []
    directory = os.fsencode(directory_name)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"):
            f = open(directory_name + '/' + filename, encoding='utf-8')
            #print(filename)
            json_file = json.load(f) # input jsons

        for entity in json_file['entities']:
            for predicate in json_file['entities'][entity]['claims']:
                if predicate == 'P170' or predicate == 'P50' or predicate == 'P276':
                    entities_list.append(entity)
                    x = 0
                    while x < len(json_file['entities'][entity]['claims'][predicate]):
                        try:
                            entities_list.append(json_file['entities'][entity]['claims'][predicate][x]['mainsnak']['datavalue']['value']['id'])
                        except:
                            #print('some uncaught json structure', entity, predicate)
                            None
                        x += 1
    entities_list = list(set(entities_list))
    print(len(entities_list), 'new P170, P50 and P276 entities')
    return entities_list

def wikidata_api_data_preparation(list_of_entities):
    string = ''
    result = []

    x = 50
    w = 0
    while w < len(list_of_entities):
        while w < x:
            if w < len(list_of_entities):
                string += str(list_of_entities[w].replace('http://www.wikidata.org/entity/','')) + '|'
            w += 1
        if x == w:
            result.append(string[0:len(string)-1])
            string = ''
        x += 50
    #print('The list of entities to get from Wikidata API', result)
    return result

def wikidata_api_requestor(prepared_list, output_partial_path=None):
    API_ENDPOINT = "https://www.wikidata.org/w/api.php"

    for query in tqdm(range(len(prepared_list))):

        params = {
          'action': 'wbgetentities',
          'format': 'json',
          'ids': prepared_list[query],
          'uselang': 'en'
      }

        r = requests.get(API_ENDPOINT, params = params)

        with open(output_partial_path + 'art_rel_entities' + str(query) + ".json", "w") as outfile:
            json.dump(r.json(), outfile, indent = 4)


# REMOVE COMMENTS BELOW TO GET ENTITIES

#entities_list = select_data_from_json("FILE PATH")
#prepared_entities_list = wikidata_api_data_preparation(entities_list)
#wikidata_api_requestor(prepared_entities_list, "FILE PATH")

