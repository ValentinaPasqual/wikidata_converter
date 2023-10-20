import json
from pymantic import sparql
import time


options = ["A) General Queries", "B) Filtered Queries", "C) Other queries"]

for option in options:
    print(option)

choice = input("Enter the letter corresponding to your choice (A/B/C): ").strip().upper()

if choice == "A":
    with open('general_queries.json', 'r') as file:
        queries = json.load(file)
elif choice == "B":
    with open('filtered_queries.json', 'r') as file:
        queries = json.load(file)
elif choice == "C":
    with open('other_queries.json', 'r') as file:
        queries = json.load(file)

def make_request(namespace, query):
    server = sparql.SPARQLServer('http://localhost:7200/repositories/' + namespace)
    tic = time.time()
    result = server.query(query)
    toc = time.time()
    exec_time = (toc - tic)*1000
    return exec_time, len(result['results']['bindings'])

log_datasets_list = ['D2']

choice_string = choice.replace(' ', '').replace(')', '')
for log_d in log_datasets_list:
    with open(f'results/{log_d}_{choice_string}_partial_queries_exec_time_results.txt', 'w') as f, \
            open(f'results/{log_d}_{choice_string}_final_queries_exec_time_results.txt', 'w') as f_final :
        for key in queries:
            if key != 'headings':
                for query_id,query in queries[key].items():
                    if query != 'None':
                        f.write(f'\n\n#### {log_d} {key} {query_id} ####\n')
                        namespace = log_d + '-' + key
                        x = 0
                        sum_et = 0
                        while x < 11:
                            exec_time, nres = make_request(namespace, query)
                            if x != 0:
                                f.write(str(exec_time) + '\n')
                                sum_et += exec_time
                                #time.sleep(1)
                            x += 1
                        sum_string = str(sum_et/10).replace('.', ',')
                        f_final.write(sum_string + '\n')
                        print(f'{log_d} {key} {query_id}: {str(nres)}')
