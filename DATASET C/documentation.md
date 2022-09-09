# RANDOM STATEMENTS

We create a Dataset C with fake artworks attributions and fake artworks locations

## Fake Attributions (with fake humans as artwork's creators)

As subjects, we select 20% of our artworks with an author (```wdt:P170```), so:
  - 3550313 artworks in total
  - 882247 artworks wich has a creator (```wdt:P170```)
  - 176449 artworks we select to be the subject of our random/fake statements (20% out of 882247)

Query to retrieve all artworks which have been created by an artist:
```
SELECT DISTINCT ?artwork
    WHERE {
        ?artwork wdt:P31 ?type.
        ?type wdt:P279* wd:Q838948.
        ?artwork wdt:P170 ?artist}
```

As predicates we choose ```wdt:P170```

As objects we select a number of humans from wikidata (looking at ```wdt:P170 costraints```, the object has to be an individual of human)

Query to retrieve all 200000 humans from wikidata:

```
SELECT DISTINCT ?human
    WHERE {
        ?human wdt:P31 wd:Q5}

LIMIT 200000
```

As statements URI, we create random identifiers (e.g. "RC-176448-1-Q106690507")

Each subject can randomly has from 1 to 5 fake attributions.

Each statement has been added into a json file which has the same structure as the wikidata json which can be retreived from the Wikidata API. (by the script ```randomic_statements.py```). Each statement ranking corresponds to "Deprecated".

The json has been converted in RDF thanks to https://www.fabiovitali.it/wikidataconverter/
With this templating a provenance triple has been added to each statement to qualify its fakeness (```statement prov:wasDerivedFrom "fake news"```)

DATASET C NOW CONTAINS:
- 176400 artworks
- 706611 (fake) attribution statements
- avg. 4 statements added to each artwork
- 621 MB size of all the json files created with ```randomic_statements.py```

Note: these counts has been made trough the ```counter.py``` script, available in this folder


******************************************************************************************************************************************************************

## Fake Locations (with fake time constraints)

We do the same also for fake artworks locations (but this time, we consider also time constraints).

As subjects, we select 20% of our artworks with a location (```wdt:P276```), so:
  - 3550313 artworks in total
  - 1016181 artworks which has a location (```wdt:P276```)
  - 203236 artworks we select to be the subject of our random/fake statements (20% out of 1016181)

Query to retrieve all artworks which have been created by an artist:
```
SELECT DISTINCT ?artwork
    WHERE {
        ?artwork wdt:P31 ?type.
        ?type wdt:P279* wd:Q838948.
        ?artwork wdt:P276 ?location}
```
As predicates we choose ```wdt:P276```

As objects we select a number of humans from wikidata (looking at ```wdt:P276``` constraints, the object has to be an individual of human)

Query to retrieve all 250000 locations from wikidata:

```
SELECT DISTINCT ?location
    WHERE {
      ?location wdt:P31 ?type.
      ?type wdt:P279* wd:Q17334923
    }

LIMIT 250000
```
Query to retrieve 250000 valid timespans from wikidata:
```
SELECT DISTINCT ?startTime ?endTime
    WHERE {
      ?s pq:P580 ?startTime ;
         pq:P582 ?endTime
    }

LIMIT 250000
```

As statements URI, we create random identifiers (e.g. "RL-94400-0-Q29478781")

Each subject can randomly has from 1 to 5 fake locations.

Each statement has been added into a json file which has the same structure as the wikidata json which can be retreived from the Wikidata API. (by the script randomic_statements.py). Each statement ranking corresponds to "Deprecated". Each statement has also a star time date and a end time date to qualify the period when the artwork has been located in the location expressed by the statement (e.g. Mona Lisa location was "Museo della Storia di Bologna" (```wd:Q55107400```) from 10 april 1903 to 13 may 1904).
DISCLAIMER: Dates are complitely random, this means that the artwork's inception can be postumous confronting the start date of its location.

The json has been converted in RDF thanks to https://www.fabiovitali.it/wikidataconverter/
With this templating a provenance triple has been added to each statement to qualify its fakeness (statement prov:wasDerivedFrom "fake news")

DATASET C NOW CONTAINS:
- 203236 artworks
- 812039 (fake) location statements
- avg. 4 statements added to each artwork
- 2,35 GB size of all the json files created with ```randomic_statements.py```

Note: these counts has been made trough the ```counter.py``` script, available in this folder
