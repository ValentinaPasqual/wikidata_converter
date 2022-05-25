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

From Wikidata SPARQL endpoint, we selected all artworks (Q1). Then we got all artworks related metadata from Wikidata API (```wbgetentities``` method). 
This process is available at ```get_all_artworks.py```.

Q1: 
```
SELECT DISTINCT ?artwork ?type WHERE {
    ?artwork wdt:P31 ?type.
    ?type (wdt:P279*) wd:Q838948. hint:Prior hint:rangeSafe true
}
``` 
Additionally, we selected all creators (```wdt:P170```) (Q2), authors (```wdt:P50```) (Q3), locations (```wdt:P276```) (Q3) of the abovementioned artworks (extracted with Q1).
As in the previous step, we we got all creators, authors and locations related metadata from Wikidata API. 
This process is available at ```get_artists_and_locs.py```.

We created three Datasets A (namely A1, A2, A3) which differ in their size. We finally decide to maintain in the final dataset the dataset A3. 

The results are summarised in the table below. 

|                          | **Dataset A1** | **Dataset A2** | **Dataset A3**  |
|--------------------------|----------------|----------------|-----------------|
| **Artworks Entities**    | 996679         | 1989191        | 3537045         |
| **Artworks Statements**  | 12737671       | 23043346       | 39868568        |
| **Locations Entities**   | 25282          | 76159          | 1233369         |
| **Locations Statements** | 906008         | 3376693        | 24189262        |
| **Authors Entities**     | //             | //             | 765350          |
| **Authors Statements**   | //             | //             | 24389391        |
| **Creators Entities**    | 19865          | 88663          | 1377454         |
| **Creators Statements**  | 1235069        | 5988387        | 53738223        |
| **Total Entities**       | 1041826        | 2154013        | 6913218         |
| **Total Statements**     | 23032748       | 32408426       | 142185444       |
| **Folder weight**        | 31.7 GB        | 74.6 GB        | 359,2 GB        |


## Dataset B
Then we selected 3'000'000 random wikidata entities which are not artworks along with their metadata (Q2).  This process is available at ```get_random_data.py```.

Q2: 
```
SELECT DISTINCT * WHERE {
    ?entity wdt:P31 ?type. hint:Prior hint:rangeSafe true
    MINUS { ?type (wdt:P279*) wd:Q838948. }
}
LIMIT 3000000
```

The results are summarised in the table below. 

|                          | **Dataset B**  | 
|--------------------------|----------------|
| **Entities**             | 2999999        |
| **Statements**           | 62102993       |
| **Folder weight**        | 144.3 GB       | 

## Dataset C
For an in depth documentation of the process of creation of Dataset C, please see ```documentation.md``` in ```DATASET C``` folder.

|                                    | **Fake creators** | **Fake authors** | **Fake locations** | **Total Dataset C** |
|------------------------------------|-------------------|------------------|--------------------|---------------------|
| **Entities (artworks)**            | 996679            | 153070           | 203236             |                     |
| **Statements (fake)**              | 12737671          | 612387           | 813050             |                     |
| **Avg. fake statements x artwork** | 4                 | 4                | 4                  |                     |
| **Folder weight**                  | 0.621 GB          | 0.551 GB         | 2,35 GB            |                     |

# LOG DATASETS

Dataset A + B + C constitute our final dataset. From now, we will refer to the final dataset as D4. 
In order to test Conjectures efficiency, we decided to create 3 additional datasets from D4:
- D1 is D4 files / 1000 
- D2 is D4 files / 100
- D3 is D4 files / 10

D1, D2, D3 contain a selected randomic selection of D4 in order to present the same Dataset in 4 different sizes (logaritmic increment) with a weighted distribution of the files.

The process has been realised with ```log_datasets.py```.

# Additional materials
- In folder ```handlebars_templates``` has been saved all templates to convert jsons into RDF with https://www.fabiovitali.it/wikidataconverter/
- In folder ```handlebars_templates_fake```has been saved all templates to convert fake jsons (Dataset C) into RDF https://www.fabiovitali.it/wikidataconverter/
