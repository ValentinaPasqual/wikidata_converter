import json
import random

f_artists = open('C:/Users/Valentina/Downloads/selected_artworks.json')
f_humans =  open('C:/Users/Valentina/Downloads/humans.json')


with open('C:/Users/Valentina/Downloads/selected_artworks.json') as f1:
   json_artists = json.load(f1)

with open('C:/Users/Valentina/Downloads/humans.json') as f2:
   json_humans = json.load(f2)

artists_list = [a['artwork'] for a in json_artists]
humans_list = [a['human'] for a in json_humans]
num = [1,2,3,4,5]
result = []


i = 0
while i <= len(artists_list):
    string3, string4, final_string = str(), str(), str()
    for artist in artists_list[i:i+200]:
        n = random.choice(num)
        x = 0
        string2 = str()
        short_subj = artist.replace('http://www.wikidata.org/entity/', '')
        while x <= n:
            res = ()
            obj = random.choice(humans_list)
            statement = str('R-' + str(artists_list.index(artist)) + '-' + str(x) + '-' + artist.replace('http://www.wikidata.org/entity/', ''))
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
        if artists_list.index(artist) != len(artists_list) - 1:
            if artists_list.index(artist) != i+199 :
                string3 = string3 + ','
        string4 = string4 + string3
    string_final = """{\"entities\": {""" + string4 + "}}"
    r = json.loads(string_final)
    with open('C:/Users/Valentina/Documents/DHDK/DHARC/PhD/tesi_eduard/fake_statements_2/' + "file" + str(i) + '-' + str(i+ 200) + ".json", 'w') as outfile:
        json.dump(r, outfile, indent=4)
    i += 200
