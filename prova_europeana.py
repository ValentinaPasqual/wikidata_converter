import pandas as pd
from SPARQLWrapper import SPARQLWrapper2, JSON, CSV
from pathlib import Path

sparql = SPARQLWrapper2("https://query.wikidata.org/sparql")
df = pd.read_csv(r'C:/Users/Valentina/Downloads/items_per_class.csv', sep=',')

i = 0
rows = []
while i < 10:
    print(i)
    l,result = [], []
    d = {}
    string = """ SELECT ?superclassLabel
    WHERE {<"""+ df.iloc[i]['class'] +"""> (wdt:P279*) ?superclass 
    SERVICE wikibase:label {
     bd:serviceParam wikibase:language "en" .
   }}"""
    sparql.setQuery(string)
    sparql.query()
    for res in sparql.query().bindings:
        if res != None:
            rows.append([df.iloc[i]['classLabel'], res['superclassLabel'].value, df.iloc[i]['nItem']])
    i += 1
    df_res = pd.DataFrame(rows, columns=["Source", "Target", 'Weight'])

filepath = Path('C:/Users/Valentina/Downloads/class_superclass.csv')
df_res.to_csv(filepath, index=False)


# https://query.wikidata.org/#SELECT%20DISTINCT%20%3Fsuperclass%20%3Fclass%20%28COUNT%28%3Fitem%29%20as%20%3FnItem%29%0AWHERE%20%7B%3Fitem%20wdt%3AP31%20%3Fclass.%20%3Fclass%20wdt%3AP279%20%3Fsupeclass%7D%0AGROUP%20BY%20%3Fsuperclass%20%3Fclass%20ORDER%20BY%20DESC%20%28%3FnItem%29
