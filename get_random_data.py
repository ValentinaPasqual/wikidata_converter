from SPARQLWrapper import SPARQLWrapper2, JSON, CSV
import pandas as pd
import requests
import json
from tqdm import tqdm

'''
File used to generate Dataset B with all the random data
'''

sparql = SPARQLWrapper2("https://query.wikidata.org/sparql")


# Data preparation for Wikidata API requests (50 entities per item)

def wikidata_api_data_preparation(list_of_entities):
    string = ''
    result = []

    x = 50
    w = 0
    while w < len(list_of_entities):
        while w < x:
            if w < len(list_of_entities):
                string += str(list_of_entities[w].replace('http://www.wikidata.org/entity/', '')) + '|'
            w += 1
        if x == w:
            result.append(string[0:len(string) - 1])
            string = ''
        x += 50
    return result


# Actual request (50 at a time) to Wikidata API

def wikidata_api_requestor(prepared_list, output_partial_path=None):
    API_ENDPOINT = "https://www.wikidata.org/w/api.php"

    for query in tqdm(range(len(prepared_list))):
        params = {
            'action': 'wbgetentities',
            'format': 'json',
            'ids': prepared_list[query],
            'uselang': 'en'
        }

        r = requests.get(API_ENDPOINT, params=params)

        with open(output_partial_path + str(query) + ".json", "w") as outfile:
            json.dump(r.json(), outfile, indent=4)


# Gets artworks with (when possible) their creator, location and type and stores them into 4 separate csv files

def get_entities_from_wikidata():  # get the list of entities and store them into 3 csv
    random_entity_list = []
    string = """
    SELECT DISTINCT * WHERE {
        ?entity wdt:P31 ?type. hint:Prior hint:rangeSafe true
        MINUS { ?type (wdt:P279*) wd:Q838948. }
    }
    LIMIT 3000000
    """
    sparql.setQuery(string)  # gets all wd entities which belong to a subclass of work of art with their creators and locations
    sparql.query()

    for res in sparql.query().bindings:
        if res != None:
            random_entity_list.append(res['entity'].value)

    print(str(len(random_entity_list)) + ' random entities')

    random_entity_dict = {'entities': list(set(random_entity_list))}
    df = pd.DataFrame(random_entity_dict)
    df.to_csv('~/wiki/intermediate_files/entities.csv', index=False)

    return random_entity_list


# Call all previous functions

random_entity_list = get_entities_from_wikidata()

prepared_entity_list = wikidata_api_data_preparation(random_entity_list)
wikidata_api_requestor(prepared_entity_list, "/home/yoda/wiki/output_data/random/entities")
