import json
import random



# GET JSONS

f_creators = open('C:/Users/Valentina/Downloads/selected_artworks_with_creators.json')
f_humans =  open('C:/Users/Valentina/Downloads/humans.json')
#f_authors =  open('C:/Users/Valentina/Downloads/humans_artworks_with_authors.json')



with open('C:/Users/Valentina/Downloads/selected_artworks_with_creators.json') as f1:
   json_artworks_creators = json.load(f1)

with open('C:/Users/Valentina/Downloads/humans.json') as f2:
   json_humans = json.load(f2)


#with open('C:/Users/Valentina/Downloads/selected_artworks_with_authors.json') as f3:
   #json_artworks_authors = json.load(f3)


# CREATE FAKE-RANDOMIC JSONS

def randomic_humans(json_artworks_artists, json_humans, folder_name):
    artworks_creators_list = [a['artwork'] for a in json_artworks_artists]
    humans_list = [a['human'] for a in json_humans]
    num = [1,2,3,4,5]
    result = []

    i = 0
    while i <= len(artworks_creators_list):
        string3, string4, final_string = str(), str(), str()
        for artist in artworks_creators_list[i:i+200]:
            n = random.choice(num)
            x = 0
            string2 = str()
            short_subj = artist.replace('http://www.wikidata.org/entity/', '')
            while x <= n:
                res = ()
                obj = random.choice(humans_list)
                statement = str('R-' + str(artworks_creators_list.index(artist)) + '-' + str(x) + '-' + artist.replace('http://www.wikidata.org/entity/', ''))
                res = (artist, obj, statement)
                result.append(res)
                short_obj = obj.replace('http://www.wikidata.org/entity/', '')
                string = str()
                string = string + """
                            {\"mainsnak\": {
                        \"snaktype\": \"value\",
                        \"property\": \"P170\",
                        \"hash\": \"330a2a62e33dca172c13d2aec4565ef2aba54cb1\",
                        \"datavalue\": {
                        \"value\": {
                                \"entity-type\": \"item\",
                                \"numeric-id\": 170,
                                \"id\":\""""+ short_obj +"""\"
                        },
                        \"type\": \"wikibase-entityid\"
                        },
                        \"datatype\": \"wikibase-item\"
                },
                \"type\": \"statement\",
                \"id\": \"""" + statement + """\",
                \"rank\": \"deprecated\"}"""
                if x != n:
                    string = string + ','
                string2 = string2 + string
                x += 1
            string3 = """\"""" + short_subj + """\":{"id":\"""" + short_subj+ """\", \"claims\": {\"P170\":[""" + string2 + "]}}"
            if artworks_creators_list.index(artist) != len(artworks_creators_list) - 1:
                if artworks_creators_list.index(artist) != i+199 :
                    string3 = string3 + ','
            string4 = string4 + string3
        string_final = """{\"entities\": {""" + string4 + "}}"
        r = json.loads(string_final)
        with open('C:/Users/Valentina/Documents/DHDK/DHARC/PhD/tesi_eduard/fake_statements_2/' + folder_name + "/file" + str(i) + '-' + str(i+ 200) + ".json", 'w') as outfile:
            json.dump(r, outfile, indent=4)
        i += 200


# CALL FUNCTION

#randomic_humans(json_artworks_creators, json_humans, "creators")
#randomic_humans(json_artworks_authors, json_humans, "authors")


################################## LOCATIONS ##################################################

with open('C:/Users/Valentina/Documents/GitHub/wikidata_converter/DATASET C/input_files/artworks_with_locations.json') as f4:
    json_artworks_locations = json.load(f4)

json_artworks_locations = json_artworks_locations[:203236]

with open('C:/Users/Valentina/Documents/GitHub/wikidata_converter/DATASET C/input_files/cultural_institutions.json') as f5:
    json_locations = json.load(f5)

with open('C:/Users/Valentina/Documents/GitHub/wikidata_converter/DATASET C/input_files/timespans.json') as f6:
    json_timespans = json.load(f6)

def randomic_locations(json_artworks_locations, json_locations, folder_name): # rivedi
    artworks_list = [a['artwork'] for a in json_artworks_locations]
    loc_list = [a['location'] for a in json_locations]
    timespans = [(a['startTime'], a['endTime']) for a in json_timespans if "wikidata" not in a['startTime']]
    for x in timespans:
        print(x)
    num = [1,2,3,4,5]
    result = []

    i = 0
    while i <= len(artworks_list):
        string3, string4, final_string = str(), str(), str()
        for loc in artworks_list[i:i + 200]:
            n = random.choice(num)
            x = 0
            string2 = str()
            short_subj = loc.replace('http://www.wikidata.org/entity/', '')
            while x <= n:
                res = ()
                obj = random.choice(loc_list)
                print(i, short_subj, obj)
                statement = str('R-' + str(artworks_list.index(loc)) + '-' + str(x) + '-' + loc.replace(
                    'http://www.wikidata.org/entity/', ''))
                res = (loc, obj, statement)
                result.append(res)
                short_obj = obj.replace('http://www.wikidata.org/entity/', '')
                random_time = random.choice(timespans)
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
                                                    "time": \""""+ random_time[0] +"""\",
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
                                                    "time": \"""" + random_time[1] + """\",
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
                                    ]}}"""
                if x != n:
                    string = string + ','
                string2 = string2 + string
                x += 1
            string3 = """\"""" + short_subj + """\":{"id":\"""" + short_subj + """\", \"claims\": {\"P276\":[""" + string2 + "]}}"
            if artworks_list.index(loc) != len(artworks_list) - 1:
                if artworks_list.index(loc) != i + 199:
                    string3 = string3 + ','
            string4 = string4 + string3
        string_final = """{\"entities\": {""" + string4 + "}}"
        r = json.loads(string_final)
        with open(
                'C:/Users/Valentina/Documents/DHDK/DHARC/PhD/tesi_eduard/fake_statements_2/' + folder_name + "/file" + str(
                        i) + '-' + str(i + 200) + ".json", 'w') as outfile:
            json.dump(r, outfile, indent=4)
        i += 200




randomic_locations(json_artworks_locations, json_locations, "locations")


