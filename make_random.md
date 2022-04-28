# RANDOM STATEMENTS

We create a Dataset C with fake attributions, composed by:

As subjects, we select 20% of our artworks with an author (wdt:P170), so:
  - 3550313 artworks in total 
  - 882247 artworks wich has a creator (wdt:P170)
  - 176449 artworks we select to be the subject of our random/fake statements (20% out of XXXXX)

Query to retrieve all artworks which have been created by an artist:
SELECT DISTINCT ?artwork
    WHERE {
        ?artwork wdt:P31 ?type.
        ?type wdt:P279* wd:Q838948.
        ?artwork wdt:P170 ?artist}

As predicates we choose wdt:P170 

As objects we select a number of humans from wikidata (looking at wdt:P170 costraints, the object has to be an individual of human)

Query to retrieve all 200000 humans from wikidata:

SELECT DISTINCT ?human
    WHERE {
        ?human wdt:P31 wd:Q5}

LIMIT 200000


As statements URI, we create random identifiers

Each subject can randomely has from 1 to 5 fake attributions.