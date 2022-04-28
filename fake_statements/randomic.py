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

string3 = str()
string_final = str()
for na in range(len(artists_list)):
    n = random.choice(num)
    x = 0
    artist = artists_list[na]
    string2 = str()
    short_subj = artist.replace('http://www.wikidata.org/entity/', '')
    while x <= n:
        res = ()
        obj = random.choice(humans_list)
        statement = str('R-' + str(na) + '-' + str(x) + '-' + artist.replace('http://www.wikidata.org/entity/', ''))
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
    string3 = """{\"""" + short_subj + """\":{"id":\"""" + short_subj+ """\", \"claims\": {\"P170\":[""" + string2 + "]}}}"
string_final = """{\"entities\": """ + string3 + "}"

print(string_final)
print('****************************')







