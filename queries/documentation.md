## Endpoint setup
RUN BLAZEGRAPH and GRAPHDB locally
Upload all provided datasets (each dataset corresponds to a GraphDB Repository). Each namespace (or repository) must be named as, for example, "D1-conj" or "D1-ng" or "D1-sng" or "D1-wiki" or "D1-rdfstar". Since this project focuses over four logaritmic datasets, each namespace/repository has to be named after "D1" or "D2" or "D3" or "D4". When all datasets have been uploaded to the selected SPARQL endpoints (20 datasets in total), the scripts in this folder can be run.

## Running graphDB_run.py
Both scripts run the 8 selected queries (stored in general_queries.json and filtered_queries.json) 10 times each. Each run of the scripts produces 2 .txt files:
- the first contains the execution times of each query
- the second contains the avarage exectution for each query (run 10 times) of each dataset
- additionally, the scripts print the number of results in the python console aiming to check also the dataset consistency

If you occur in some Heap memory threshold overload, please add to your GraphDB instance the rule "Ddefault.min.distinct.threshold:300000000" (which is usually 250m by default)
