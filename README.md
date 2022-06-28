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

Dataset C contains a selection of fake statements regarding the creator, author or location of artworks (from dataset A3). Those new statements contain fake randomic information and are ranked as Deprecated in order to increase the number of conjectural statements in the final dataset. 

For example, a fake statement can be the attribution of Mona Lisa to Tim Berners Lee. 

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

# Asserted and Non-asserted statements in Wikidata
In Wikidata, assertion or non assertion of claims is strictly dependent from their rankings. 

For example, the triples (1)```wd:Q10743 wdt:P214 "249422654"``` and (2)```wd:Q10743 wdt:P214 "315523483"``` share the same subject-predicate values, but differ wrt their objects. 

- If both triples (1 and 2) are ranked as Normal, they are both asserted.
- If both triples (1 and 2) are ranked as Preferred, they are both asserted.
- If both triples (1 and 2) are ranked as Normal, they are both non-asserted.
- If triple (1) is ranked as Preferred and triple (2) is ranked as Normal, the first (1) is asserted and the second (2) is non-asserted. 
- If triple (1) is ranked as Deprecated and triple (2) is ranked as Noraml, the first (1) in non-asserted and the second (2) is asserted. 
- If triple (1) is ranked as Deprecated and triples (2) is ranked as Preferred, the first (1) is non-asserted and the second (2) is asserted. 

# Additional materials
- In folder ```handlebars_templates``` has been saved all templates to convert jsons into RDF with https://www.fabiovitali.it/wikidataconverter/
- In folder ```handlebars_templates_fake``` has been saved all templates to convert fake jsons (Dataset C) into RDF https://www.fabiovitali.it/wikidataconverter/
- In folder ```handlebars_templates``` you can find an additional set of helpers called ```helper.js```, this is meant to be use in data conversions since it reproduces the assertion - non assertion of the statements in the json files (a more in the depth explanation of the topic is in the section above).


# Converting files via Wikidata Converter App
The downloaded json files from Wikidata can be trasformed into RDF format with the online converter 
- Download the application from  [LINK AL COVERTER AGGIORNATO].
- Start the application by simply starting node with the command ```node app.js```, the interface will be available in your browser at port ```3000```.
- In the interface, upload the templates (available in folder ```handlebars_templates``` and ```handlebars_templates_fake```) or fill the dedicated forms.
- Use "Bulk convert" function to upload a .zip archive containing all jsons. 
    - Note. Do not upload a .zip file grater than 2GB. 
    - Note 2. If the process stops, allocate more RAM space in the cmd with the command ```node --max-old-space-size=12288 app.js``` to run again the application. 
- A .zip folder will be automatically downloaded. This archive contains all RDF files converted against your chosen templates. 

# Example output RDF files out of handlebars templates
A conversion test has been run agaist the templates. In the folder ```conversion_test``` can be found input and output data. Each output RDF dataset has been validated with Blazegraph. Below a summary:

|                      | Upload time (ms) | Query Time (ms) | Triples |
|----------------------|------------------|-----------------|---------|
| Wikidata Statement   | 1340             | 773             | 6487    |
| Singleton Properties | 1304             | 681             | 5385    |
| Named Graphs         | 1239             | 3334            | 611     |
| RDF-star             |                  |                 |         |
| Conjectures          |                  |                 |         |


### Wikidata

```
## Two statements ranked as normal ##


wd:Q183 p:P1705 s:Q183-d657d418-4a25-98d6-5180-a3659a11fbcd .
s:Q183-d657d418-4a25-98d6-5180-a3659a11fbcd a wikibase:Statement; 
    wikibase:rank wikibase:NormalRank;
    ps:P1705 "Bundesrepublik Deutschland"@de;
    wikibase:rank wikibase:NormalRank.
    
wd:Q183 p:P1705 s:Q183$E2A638D7-78B7-424D-9F63-AF49F5DCAE84 .
s:Q183-E2A638D7-78B7-424D-9F63-AF49F5DCAE84 a wikibase:Statement; 
    wikibase:rank wikibase:NormalRank;
    ps:P1705 "Deutschland"@de;
    wikibase:rank wikibase:NormalRank.
    
#### Three statements ranked respectively as normal, deprecated and preferred. ####

wd:Q183 p:P530 s:Q183-DF432913-CEBA-49ED-BCA4-7214957E6CDA .
s:Q183-DF432913-CEBA-49ED-BCA4-7214957E6CDA a wikibase:Statement; 
    wikibase:rank wikibase:NormalRank;
    pq:P805 wd:Q15910813;
    pq:P582 "1972-00-00T00:00:00Z"^^xsd:dateTime;
    pq:P2241 wd:Q26256296;
    ps:P530 wd:Q865;
    wikibase:rank wikibase:NormalRank.

wd:Q183 p:P530 s:Q183-a6aa383f-4c30-79bf-0767-dcf4ea80f8d6 .
s:Q183-a6aa383f-4c30-79bf-0767-dcf4ea80f8d6 a wikibase:Statement; 
    wikibase:rank wikibase:DeprecatedRank;
    pq:P805 wd:Q1201896;
    pq:P2241 wd:Q28831311;
    ps:P530 wd:Q917;
    wikibase:rank wikibase:DeprecatedRank.
     
wd:Q183 p:P530 s:Q183-0B26503A-A8BF-4B40-9F0A-CAE242AE03A1 .
s:Q183-0B26503A-A8BF-4B40-9F0A-CAE242AE03A1 a wikibase:Statement; 
    wikibase:rank wikibase:PreferredRank;
    pq:P805 wd:Q28498636;
    pq:P531 wd:Q58003162;
    ps:P530 wd:Q1011;
    wikibase:rank wikibase:PreferredRank.
```

### Named Graphs
With named graphs all statements are asserted. Rankings has been mantained with each graph in order to retrieve their confidence. 

```
## Two statements ranked as normal ##

GRAPH s:Q183-d657d418-4a25-98d6-5180-a3659a11fbcd { 
    wd:Q183 wdt:P1705 "Bundesrepublik Deutschland"@de 
}
s:Q183-d657d418-4a25-98d6-5180-a3659a11fbcd wikibase:rank wikibase:NormalRank.

GRAPH s:Q183-E2A638D7-78B7-424D-9F63-AF49F5DCAE84 { 
    wd:Q183 wdt:P1705 "Deutschland"@de 
}
s:Q183-E2A638D7-78B7-424D-9F63-AF49F5DCAE84 wikibase:rank wikibase:NormalRank.

#### Three statements ranked respectively as normal, deprecated and preferred. ####  

GRAPH s:Q183-DF432913-CEBA-49ED-BCA4-7214957E6CDA { 
wd:Q183 wdt:P530 wd:Q865 
}
s:Q183-DF432913-CEBA-49ED-BCA4-7214957E6CDA pq:P805 wd:Q15910813.
s:Q183-DF432913-CEBA-49ED-BCA4-7214957E6CDA pq:P582 "1972-00-00T00:00:00Z"^^xsd:dateTime.
s:Q183-DF432913-CEBA-49ED-BCA4-7214957E6CDA pq:P2241 wd:Q26256296.
s:Q183-DF432913-CEBA-49ED-BCA4-7214957E6CDA wikibase:rank wikibase:NormalRank.

GRAPH s:Q183-a6aa383f-4c30-79bf-0767-dcf4ea80f8d6 { 
    wd:Q183 wdt:P530 wd:Q917 
}
s:Q183-a6aa383f-4c30-79bf-0767-dcf4ea80f8d6 pq:P805 wd:Q1201896.
s:Q183-a6aa383f-4c30-79bf-0767-dcf4ea80f8d6 pq:P2241 wd:Q28831311.
s:Q183-a6aa383f-4c30-79bf-0767-dcf4ea80f8d6 wikibase:rank wikibase:DeprecatedRank.

GRAPH s:Q183-0B26503A-A8BF-4B40-9F0A-CAE242AE03A1 { 
wd:Q183 wdt:P530 wd:Q1011 
}
s:Q183-0B26503A-A8BF-4B40-9F0A-CAE242AE03A1 pq:P805 wd:Q28498636.
s:Q183-0B26503A-A8BF-4B40-9F0A-CAE242AE03A1 pq:P531 wd:Q58003162.
s:Q183-0B26503A-A8BF-4B40-9F0A-CAE242AE03A1 wikibase:rank wikibase:PreferredRank.

```

### Singleton Properties
```
## Two statements ranked as normal ##

wd:Q183 wdt:P1705 "Bundesrepublik Deutschland"@de.
wd:Q183 sng:Q183-d657d418-4a25-98d6-5180-a3659a11fbcd "Bundesrepublik Deutschland"@de.
sng:Q183-d657d418-4a25-98d6-5180-a3659a11fbcd sng:singletonPropertyOf wdt:P1705 .
    wikibase:rank wikibase:NormalRank.
 
wd:Q183 wdt:P1705 "Deutschland"@de.
wd:Q183 sng:Q183-E2A638D7-78B7-424D-9F63-AF49F5DCAE84 "Deutschland"@de.
sng:Q183-E2A638D7-78B7-424D-9F63-AF49F5DCAE84 sng:singletonPropertyOf wdt:P1705 .
    wikibase:rank wikibase:NormalRank.

#### Three statements ranked respectively as normal, deprecated and preferred. ####  

wd:Q183 sng:Q183-DF432913-CEBA-49ED-BCA4-7214957E6CDA wd:Q865.
sng:Q183-DF432913-CEBA-49ED-BCA4-7214957E6CDA sng:singletonPropertyOf wdt:P530 .
    pq:P805 wd:Q15910813;
    pq:P582 "1972-00-00T00:00:00Z"^^xsd:dateTime;
    pq:P2241 wd:Q26256296;
    wikibase:rank wikibase:NormalRank.

wd:Q183 sng:Q183-a6aa383f-4c30-79bf-0767-dcf4ea80f8d6 wd:Q917.
sng:Q183-a6aa383f-4c30-79bf-0767-dcf4ea80f8d6 sng:singletonPropertyOf wdt:P530 .
    pq:P805 wd:Q1201896;
    pq:P2241 wd:Q28831311;
    wikibase:rank wikibase:DeprecatedRank.

wd:Q183 wdt:P530 wd:Q1011.
wd:Q183 sng:Q183-0B26503A-A8BF-4B40-9F0A-CAE242AE03A1 wd:Q1011.
sng:Q183-0B26503A-A8BF-4B40-9F0A-CAE242AE03A1 sng:singletonPropertyOf wdt:P530 .
    pq:P805 wd:Q28498636;
    pq:P531 wd:Q58003162;
    wikibase:rank wikibase:PreferredRank.
```
