# RANDOM STATEMENTS

We create a Dataset C with fake artworks attributions and fake artworks locations

## Fake Attributions (with fake humans as artowork's creators)

As subjects, we select 20% of our artworks with an author (wdt:P170), so:
  - 3550313 artworks in total 
  - 882247 artworks wich has a creator (wdt:P170)
  - 176449 artworks we select to be the subject of our random/fake statements (20% out of 882247)

Query to retrieve all artworks which have been created by an artist:
```
SELECT DISTINCT ?artwork
    WHERE {
        ?artwork wdt:P31 ?type.
        ?type wdt:P279* wd:Q838948.
        ?artwork wdt:P170 ?artist}
```

As predicates we choose wdt:P170 

As objects we select a number of humans from wikidata (looking at wdt:P170 costraints, the object has to be an individual of human)

Query to retrieve all 200000 humans from wikidata:

```
SELECT DISTINCT ?human
    WHERE {
        ?human wdt:P31 wd:Q5}

LIMIT 200000
```

As statements URI, we create random identifiers (e.g. "R-176448-1-Q106690507")

Each subject can randomely has from 1 to 5 fake attributions.

Each statement has been added into a json file which has the same structure as the wikidata json which can be retreived from the Wikidata API. (by the script randomic_humans.py). Each statement ranking corresponds to "Deprecated".

The json has been converted in RDF thanks to https://www.fabiovitali.it/wikidataconverter/
With this templating a provenance triple has been added to each statement to qualify its fakeness (statement prov:wasDerivedFrom "fake news")

DATASET C NOW CONTAINS:
- 176400 artworks 
- 706611 (fake) attribution statements 
- avg. 4 statements added to each artwork
- 621 MB size of all the json files created with randomic_humans.py

Note: these counts has been made trough the counter.py script, available in this folder


******************************************************************************************************************************************************************

## Fake Locations (with fake locations and dates)

We do the same also for fake artworks locations (but this time, we consider also time constraints).

As subjects, we select 20% of our artworks with a location (wdt:P276), so:
  - 3550313 artworks in total 
  - 1016181 artworks wich has a location (wdt:P276)
  - 203236 artworks we select to be the subject of our random/fake statements (20% out of 1016181)

Query to retrieve all artworks which have been created by an artist:
```
SELECT DISTINCT ?artwork
    WHERE {
        ?artwork wdt:P31 ?type.
        ?type wdt:P279* wd:Q838948.
        ?artwork wdt:P276 ?location}
```


