import json
from pymantic import sparql
import time

import csv

with open('C:\\Users\\Valentina\\Downloads\D3_results\\general_queries.csv') as f:
    general_queries = [{k: v for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True, delimiter='@')]

def make_request(namespace, query):
    server = sparql.SPARQLServer('http://localhost:9999/blazegraph/namespace/' + namespace +'/sparql')
    tic = time.time()
    result = server.query(query)
    toc = time.time()
    exec_time = (toc - tic)*1000
    return exec_time, len(result['results']['bindings'])

datasets_list = ['D1', 'D2', 'D3'] # add D4
models_list = ['conj', 'ng', 'sng', 'wiki']

with open('C:\\Users\\Valentina\\Downloads\D3_results\\BLAZEGRAPH_partial_general_queries_exec_time_results.txt', 'w') as f, \
        open('C:\\Users\\Valentina\\Downloads\D3_results\\BLAZEGAPH_final_general_queries_exec_time_results.txt', 'w') as f_final :
    for d in datasets_list:
        for m in models_list:
            f_final.write(f'\n\n#### ' + d + ' ' + m + ' ####\n')
            for idx, g in enumerate(general_queries):
                f.write(f'\n\n#### ' + d + ' ' + m + ' Q' + str(idx + 1) + ' ####\n')
                namespace = d + '-' + m
                x = 0
                sum_et = 0
                while x < 11:
                    exec_time, nres = make_request(namespace, g[m])
                    if x != 0:
                        f.write(str(exec_time) + '\n')
                        sum_et += exec_time
                        time.sleep(1)
                    x += 1
                sum_string = str(sum_et/10).replace('.', ',')
                f_final.write(sum_string + '\n')
                print(d + ' ' + m + ' Q' + str(idx + 1) + ': ' + str(nres))




