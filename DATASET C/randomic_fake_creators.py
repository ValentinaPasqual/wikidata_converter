import json
import random
import time

# GET JSONS

with open('/your_local_path_to_the_data/input/selected_artworks_with_creators.json') as f1:
    json_artworks_creators = json.load(f1)

with open('/your_local_path_to_the_data/input/humans.json') as f2:
    json_humans = json.load(f2)


# CREATE FAKE-RANDOMIC JSONS

def randomic_humans(json_artworks_artists, json_humans, folder_name):
    artworks_creators_list = [a['artwork'] for a in json_artworks_artists]
    humans_list = [a['human'] for a in json_humans]
    num = [1, 2, 3, 4, 5]
    result = []

    i = 0
    while i <= len(artworks_creators_list):
        string3, string4, final_string = str(), str(), str()
        for artist in artworks_creators_list[i:i + 200]:
            print(artist.split('/')[-1], i)
            n = random.choice(num)
            x = 0
            string2 = str()
            short_subj = artist.replace('http://www.wikidata.org/entity/', '')
            while x <= n:
                res = ()
                obj = random.choice(humans_list)
                statement = str('RC-' + str(artworks_creators_list.index(artist)) + '-' + str(x) + '-' + artist.replace(
                    'http://www.wikidata.org/entity/', ''))
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
                                \"id\":\"""" + short_obj + """\"
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
            string3 = """\"""" + short_subj + """\":{"id":\"""" + short_subj + """\", \"claims\": {\"P170\":[""" + string2 + "]}}"
            if artworks_creators_list.index(artist) != len(artworks_creators_list) - 1:
                if artworks_creators_list.index(artist) != i + 199:
                    string3 = string3 + ','
            string4 = string4 + string3
        string_final = """{\"entities\": {""" + string4 + "}}"
        r = json.loads(string_final)
        with open('/your_local_path_to_the_data/output/' + folder_name + "/file" + str(i) + '-' + str(i + 200) + ".json",
                  'w') as outfile:
            json.dump(r, outfile, indent=4)
        i += 200


# CALL FUNCTION
start_time = time.time()
randomic_humans(json_artworks_creators, json_humans, "creators")
end_time = time.time()
print(f'Total execution time: {end_time - start_time} seconds (~{int((end_time - start_time)/60)} minutes)')
