import json
import os
import random
import re
from datetime import date, timedelta, datetime


# GET JSONS for D4

with open('input_files/selected_artworks_with_creators.json') as f1:
    D4_json_artworks_creators = json.load(f1)

with open('input_files/selected_artworks_with_authors.json') as f2:
    D4_json_artworks_authors = json.load(f2)
    D4_json_artworks_authors = D4_json_artworks_authors[0:92590]

with open('input_files/artworks_with_locations.json') as f3:
    D4_json_artworks_locations = json.load(f3)
    D4_json_artworks_locations = D4_json_artworks_locations[0:int(len(D4_json_artworks_locations) * 20 / 100)]

with open('input_files/humans.json') as f4:
    json_humans = json.load(f4)

with open('input_files/timespans.json') as f5:
    json_timespans = json.load(f5)

with open('input_files/cultural_institutions.json') as f6:
    json_locations = json.load(f6)

# CREATE JSON FOR SELECTED ARTWORKS WITH CREATORS FOR D1,D2 AND D3
directory_name = 'C:/Users/Valentina/Documents/DHDK/DHARC/PhD/tesi_eduard/dataset/D_datasets/D1/'
directory = os.fsencode(directory_name)

def random_end_time(start):
    year = int(re.search(r'[0-9][0-9][0-9][0-9]', start).group(0))
    addition = random.randint(1, 10)
    end = re.sub(r'[0-9][0-9][0-9][0-9]', str(year + addition), start)
    return end

def from_string_to_datetime(start, end):
    start = start.replace('T', ' ').replace('Z', '')
    end = end.replace('T', ' ').replace('Z', '')
    startTime = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    endTime = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    return (startTime, endTime)

def calculate_datetime_overlap(dt_start, dt_end, l, timespans):
    if len(l) > 0:
        for x in l:
            if dt_start != x[0] and dt_end != x[1]:
                latest_start = max(dt_start, x[0])
                earliest_end = min(dt_end, x[1])
                delta = (earliest_end - latest_start).days + 1
                if delta <= 0:
                    return True
                if delta > 0:
                    start = random.choice(timespans)
                    end = random_end_time(start)
                    dt_start, dt_end = from_string_to_datetime(start, end)
                    l.append((dt_start, dt_end))
                    overlap = calculate_datetime_overlap(dt_start, dt_end, l, timespans)

def select_artworks(directory_name, property):
    entities_list = []
    directory = os.fsencode(directory_name)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json") and filename.startswith('artwork'):
            f = open(directory_name + '/' + filename, encoding='utf-8')
            json_file = json.load(f)  # input jsons

            for entity in json_file['entities']:
                for predicate in json_file['entities'][entity]['claims']:
                    if predicate == property:
                        entities_list.append(entity)
    entities_list = list(set(entities_list))
    l = []
    for e in entities_list:
        d = {'artwork' : e}
        l.append(d)
    l = l[0:int(len(l) * 20 /100)]
    print(len(l), 'selected artworks for', property)
    return l


# CREATE FAKE-RANDOMIC JSONS

def randomic_humans(json_artworks_artists, json_humans, dataset_name, folder_name, prop_number, run_number, source):
    artworks_creators_list = [a['artwork'] for a in json_artworks_artists]
    humans_list = [a['human'] for a in json_humans]
    num = [0, 1, 2]

    i = 0
    file_counter = 0
    while i <= len(artworks_creators_list):
        string3, string4, final_string = str(), str(), str()
        for artist in artworks_creators_list[i:i + 200]:
            #print(artist.split('/')[-1], i)
            n = random.choice(num)
            x = 0
            string2 = str()
            short_subj = artist.replace('http://www.wikidata.org/entity/', '')
            while x <= n:
                obj = random.choice(humans_list)
                statement = str('RC-' + str(artworks_creators_list.index(artist)) + '-' + str(x) + "-" + str(run_number) + '-' + artist.replace(
                    'http://www.wikidata.org/entity/', ''))
                short_obj = obj.replace('http://www.wikidata.org/entity/', '')
                string = str()
                string = string + """
                            {\"mainsnak\": {
                        \"snaktype\": \"value\",
                        \"property\": \"P""" + prop_number + """\",
                        \"hash\": \"330a2a62e33dca172c13d2aec4565ef2aba54cb1\",
                        \"datavalue\": {
                        \"value\": {
                                \"entity-type\": \"item\",
                                \"numeric-id\": \"""" + prop_number + """\",
                                \"id\":\"""" + short_obj + """\"
                        },
                        \"type\": \"wikibase-entityid\"
                        },
                        \"datatype\": \"wikibase-item\"
                },
                \"type\": \"statement\",
                \"id\": \"""" + statement + """\",
                \"rank\": \"normal\", 
                \"qualifiers\": {
                    \"P248\": [
                        {
                            \"snaktype\": \"value\",
                            \"property\": \"P248\",
                            \"hash\": \"b5f56a88fb59be05ee255aaa28312e249775921f\",
                            \"datavalue\": {
                                "value": {
                                    "entity-type": "item",
                                    "numeric-id": 104099663,
                                    "id": \""""+ source +"""\"
                                },
                                "type": "wikibase-entityid"
                            },
                            "datatype": "wikibase-item"
                        }
                    ]}}"""
                if x != n:
                    string = string + ','
                string2 = string2 + string
                x += 1
            string3 = """\"""" + short_subj + """\":{"id":\"""" + short_subj + """\", \"claims\": {\"P""" + prop_number + """ \":[""" + string2 + "]}}"
            if artworks_creators_list.index(artist) != len(artworks_creators_list) - 1:
                if artworks_creators_list.index(artist) != i + 199:
                    string3 = string3 + ','
            string4 = string4 + string3
        string_final = """{\"entities\": {""" + string4 + "}}"
        r = json.loads(string_final)
        with open('E:/Datasets/' + dataset_name + "_fake" + "/" + folder_name + str(int(file_counter)) + "take" + str(run_number) + ".json",
                  'w') as outfile:
            json.dump(r, outfile, indent=4)
        i += 200
        file_counter += 1

# CREATE FAKE-RANDOMIC JSONS
def randomic_locations(json_artworks_locations, json_locations, dataset_name, folder_name, run_number, source):
    artworks_locations_list = [a['artwork'] for a in json_artworks_locations]
    loc_list = [a['location'] for a in json_locations]
    timespans = [a['startTime'] for a in json_timespans if "wikidata" not in a['startTime']]
    num = [0,1,2]
    result = []

    i = 0
    file_counter = 0
    while i <= len(artworks_locations_list):
        l = []
        string3, string4, final_string = str(), str(), str()
        for loc in artworks_locations_list[i:i + 200]:
            n = random.choice(num)
            x = 0
            string2 = str()
            short_subj = loc.replace('http://www.wikidata.org/entity/', '')
            while x <= n:
                obj = random.choice(loc_list)
                statement = str('RL-' + str(artworks_locations_list.index(loc)) + '-' + str(x) + "-" + str(run_number) + '-' + loc.replace(
                    'http://www.wikidata.org/entity/', ''))
                res = (loc, obj, statement)
                result.append(res)
                short_obj = obj.replace('http://www.wikidata.org/entity/', '')
                start = random.choice(timespans)
                end = random_end_time(start)
                dt_start, dt_end = from_string_to_datetime(start, end)
                l.append((dt_start, dt_end))
                calculate_datetime_overlap(dt_start, dt_end, l, timespans)
                string = str()
                string = string + """
                                    {\"mainsnak\": {
                                       \"snaktype\": \"value\",
                                       \"property\": \"P276\",
                                       \"hash\": \"330a2a62e33dca172c13d2aec4565ef2aba54cb1\",
                                       \"datavalue\": {
                                       \"value\": {
                                               \"entity-type\": \"item\",
                                               \"numeric-id\": 276,
                                               \"id\":\"""" + short_obj + """\"
                                       },
                                       \"type\": \"wikibase-entityid\"
                                       },
                                       \"datatype\": \"wikibase-item\"
                               },
                               \"type\": \"statement\",
                               \"id\": \"""" + statement + """\",
                               \"rank\": \"deprecated\",
                                \"qualifiers\": {
                                    \"P580\": [
                                        {
                                            \"snaktype\": \"value\",
                                            \"property\": \"P580\",
                                            \"hash\": \"b5f56a88fb59be05ee255aaa28312e249775921f\",
                                            \"datavalue\": {
                                                "value": {
                                                    "time": \"""" + start + """\",
                                                    "timezone": 0,
                                                    "before": 0,
                                                    "after": 0,
                                                    "precision": 9,
                                                    "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                                                },
                                                "type": "time"
                                            },
                                            "datatype": "time"
                                        }
                                    ],
                                    "P582": [
                                        {
                                            "snaktype": "value",
                                            "property": "P582",
                                            "hash": "ed06eff7c97d8f382694792f2bac154744ac3abd",
                                            "datavalue": {
                                                "value": {
                                                    "time": \"""" + end + """\",
                                                    "timezone": 0,
                                                    "before": 0,
                                                    "after": 0,
                                                    "precision": 9,
                                                    "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
                                                },
                                                "type": "time"
                                            },
                                            "datatype": "time"
                                        }
                                    ],
                                    \"P248\": [
                        {
                        \"snaktype\": \"value\",
                        \"property\": \"P248\",
                        \"hash\": \"b5f56a88fb59be05ee255aaa28312e249775921f\",
                        \"datavalue\": {
                            "value": {
                                "entity-type": "item",
                                "numeric-id": 104099663,
                                "id": \""""+ source +"""\"
                            },
                            "type": "wikibase-entityid"
                        },
                        "datatype": "wikibase-item"
                        }
                    ]}}"""
                if x != n:
                    string = string + ','
                string2 = string2 + string
                x += 1
            string3 = """\"""" + short_subj + """\":{"id":\"""" + short_subj + """\", \"claims\": {\"P276\":[""" + string2 + "]}}"
            if artworks_locations_list.index(loc) != len(artworks_locations_list) - 1:
                if artworks_locations_list.index(loc) != i + 199:
                    string3 = string3 + ','
            string4 = string4 + string3
        string_final = """{\"entities\": {""" + string4 + "}}"
        r = json.loads(string_final)
        with open('E:/Datasets/' + dataset_name + "_fake" + "/" + folder_name + str(int(file_counter)) + "take" + str(
                run_number) + ".json",
                  'w') as outfile:
            json.dump(r, outfile, indent=4)
        i += 200
        file_counter += 1


# CALL FUNCTION FOR D4
#start_time = time.time()
#randomic_creators(D4_json_artworks_creators, json_humans, "creators", 1)
#randomic_creators(D4_json_artworks_creators, json_humans, "creators", 2)
#end_time = time.time()
#print(f'Total execution time: {end_time - start_time} seconds (~{int((end_time - start_time)/60)} minutes)')

VP_source = "<https://w3id.org/conjectures/ContrievedAttributionsInArtHistory-VP>"
FV_source = "<https://w3id.org/conjectures/InventedPaternityOfArtworks-FV>"

# CALL FUNCTION FOR D1
directory_name_D1 = 'E:/Datasets/D1/'
#sel_art_P170_D1 = select_artworks(directory_name_D1, 'P170')
#randomic_humans(sel_art_P170_D1, json_humans, "D1", "creators", '170', 1, VP_source)
#randomic_humans(sel_art_P170_D1, json_humans, "D1", "creators", '170', 2, FV_source)

#sel_art_P50_D1 = select_artworks(directory_name_D1, 'P50')
#randomic_humans(sel_art_P50_D1, json_humans, "D1", "authors", '50', 1, VP_source)
#randomic_humans(sel_art_P50_D1, json_humans, "D1", "authors", '50', 2, FV_source)

#sel_art_P276_D1 = select_artworks(directory_name_D1, 'P276')
#randomic_locations(sel_art_P276_D1, json_locations, "D1", "locations", 1, VP_source)
#randomic_locations(sel_art_P276_D1, json_locations, "D1", "locations", 2, FV_source)

##### d2 ####
#directory_name_D2 = 'E:/Datasets/D2/'
#sel_art_P170_D2 = select_artworks(directory_name_D2, 'P170')
#randomic_humans(sel_art_P170_D2, json_humans, "D2", "creators", '170', 1, VP_source)
#randomic_humans(sel_art_P170_D2, json_humans, "D2", "creators", '170', 2, FV_source)

#sel_art_P50_D2 = select_artworks(directory_name_D2, 'P50')
#randomic_humans(sel_art_P50_D2, json_humans, "D2", "authors", '50', 1, VP_source)
#randomic_humans(sel_art_P50_D2, json_humans, "D2", "authors", '50', 2, FV_source)

#sel_art_P276_D2 = select_artworks(directory_name_D2, 'P276')
#randomic_locations(sel_art_P276_D2, json_locations, "D2", "locations", 1, VP_source)
#randomic_locations(sel_art_P276_D2, json_locations, "D2", "locations", 2, FV_source)


##### d3 ####

#directory_name_D3 = 'E:/Datasets/D3/'
#sel_art_P170_D3 = select_artworks(directory_name_D3, 'P170')
#randomic_humans(sel_art_P170_D3, json_humans, "D3", "creators", '170', 1, VP_source)
#randomic_humans(sel_art_P170_D3, json_humans, "D3", "creators", '170', 2, FV_source)

#sel_art_P50_D3 = select_artworks(directory_name_D3, 'P50')
#randomic_humans(sel_art_P50_D3, json_humans, "D3", "authors", '50', 1, VP_source)
#randomic_humans(sel_art_P50_D3, json_humans, "D3", "authors", '50', 2, FV_source)

#sel_art_P276_D3 = select_artworks(directory_name_D3, 'P276')
#randomic_locations(sel_art_P276_D3, json_locations, "D3", "locations", 1, VP_source)
#randomic_locations(sel_art_P276_D3, json_locations, "D3", "locations", 2, FV_source)


##### d4 ####

#randomic_humans(D4_json_artworks_creators, json_humans, "D4", "creators", '170', 1, VP_source)
#randomic_humans(D4_json_artworks_creators, json_humans, "D4", "creators", '170', 2, FV_source)

#randomic_humans(D4_json_artworks_authors, json_humans, "D4", "authors", '50', 1, VP_source)
#randomic_humans(D4_json_artworks_authors, json_humans, "D4", "authors", '50', 2, FV_source)

#randomic_locations(D4_json_artworks_locations, json_locations, "D4", "locations", 1, VP_source)
#randomic_locations(D4_json_artworks_locations, json_locations, "D4", "locations", 2, FV_source)













