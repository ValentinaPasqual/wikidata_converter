# Conjectures efficiency over Wikidata

The final dataset is composed of the union of three main sub-datasets:
- Dataset A: Composed by ca. 3 million Wikidata artworks (along with, when possible, their creator and location) and their relative statements.
- Dataset B: Composed by ca. 3 million Wikidata random entities (except for artworks) and their relative statements. 
- Dataset C: Composed by ca. XXX million entities and their relative statements whose ranking has been randomised (especially with ```wikibase:PreferredRank``` and ```wikibase:DeprecatedRank```).

The final dataset will be modelled with five different RDF models:
- Wikidata statements
- Named Graphs
- Singleton properties
- RDF-star
- Conjectures

## Dataset A
All artworks with their type and when available their location and creator. 

``` 
SELECT DISTINCT ?artwork ?artist ?location ?type
    WHERE {
        ?artwork wdt:P31 ?type.
        ?type wdt:P279* wd:Q838948 
        OPTIONAL {?artwork wdt:P170 ?artist}
        OPTIONAL {?artwork wdt:P276 ?location}
        } 
```
Dataset A2 - artoworks, locations, artists
- 2'000'000 artworks
- 425'436 locations
- 257'791 artists
- Size: 74,7 GB

Dataset A2.6 - artoworks, locations, artists
- 2'600'000 artworks
- 282600 artists
- 443150 locations
- Size: 88,3 GB

Dataset3 - only artworks
- 3'537'243 artworks
- Size: 92 GB

## Dataset B
Entities which are not artworks 

```
SELECT DISTINCT *
WHERE {
    ?entity wdt:P31 ?type.
    FILTER NOT EXISTS {
        ?type wdt:P279* wd:Q838948.
        }
    }
LIMIT 10000
```

Dataset B1:
- 3'000'000 entities
- Size: 144,5 GB

## Dataset C
Work in Progress

# Description

- ```get_json.py```: first, it retrieves a set of Wikidata entities (defined one of the SPARQL queries depending on dataset A, B or C). Then, it requests to Wikidata API all data related to all selected enitities and saves them into several json files (50 entities with their relative metadata each file).
- Work in progress, it will be developed as a node.js application --> ```pybars_coverter.py```: takes as input all json files (from ```get_json.py```) and first, gets rid of useless information and second, convert them into several desider RDF models for expressing statements. `templates``` folder. 
    - The actual conversion fromt json to rdf is hadled with pybars3 templates (python version of javascript handlebars), and they are available in the ```pybars_templates``` folder. 
