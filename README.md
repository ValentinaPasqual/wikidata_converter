List of queries



- OUR MAIN QUERY: All artworks with their type and when available their location and creator. 

``` 
SELECT DISTINCT ?artwork ?artist ?location ?type
    WHERE {
        ?artwork wdt:P31 ?type.
        ?type wdt:P279* wd:Q838948 
        OPTIONAL {?artwork wdt:P170 ?artist}
        OPTIONAL {?artwork wdt:P276 ?location}
        } 
```

- All artworks in wikidata

```
SELECT DISTINCT ?artwork ?type
    WHERE {
        ?artwork wdt:P31 ?type.
        ?type wdt:P279* wd:Q838948 }
```

# Description

- ```get_json.py```: first, it retrieve a set of Wikidata entities (defined by a SPARQL query - in our case, all artworks with their creators and locations when available). Then, it requests to Wikidata API all data related to all selected enitities and saves them into several json files (50 entities with their relative metadata each).
- ```pybars_coverter.py```: takes as input all json files (from ```get_json.py```) and first, gets rid of useless information and second, convert them into several desider RDF models for expressing statements. `templates``` folder. 
    - The actual conversion fromt json to rdf is hadled with pybars3 templates (python version of javascript handlebars), and they are available in the ```templates``` folder. 
