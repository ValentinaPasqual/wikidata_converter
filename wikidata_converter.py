import json
import pybars
from pybars import Compiler
import os
import json
import rdflib
from rdflib import Graph, ConjunctiveGraph, RDF, RDFS, XSD, Namespace
import tqdm

prefixes = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ontolex: <http://www.w3.org/ns/silemon/ontolex#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix wikibase: <http://wikiba.se/ontology#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix schema: <http://schema.org/> .
@prefix cc: <http://creativecommons.org/ns#> .
@prefix geo: <http://www.opengis.net/ont/geosparql#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix wd: <http://www.wikidata.org/entity/> .
@prefix data: <https://www.wikidata.org/wiki/Special:EntityData/> .
@prefix s: <http://www.wikidata.org/entity/statement/> .
@prefix ref: <http://www.wikidata.org/reference/> .
@prefix v: <http://www.wikidata.org/value/> .
@prefix wdt: <http://www.wikidata.org/prop/direct/> .
@prefix wdtn: <http://www.wikidata.org/prop/direct-normalized/> .
@prefix p: <http://www.wikidata.org/prop/> .
@prefix ps: <http://www.wikidata.org/prop/statement/> .
@prefix psv: <http://www.wikidata.org/prop/statement/value/> .
@prefix psn: <http://www.wikidata.org/prop/statement/value-normalized/> .
@prefix pq: <http://www.wikidata.org/prop/qualifier/> .
@prefix pqv: <http://www.wikidata.org/prop/qualifier/value/> .
@prefix pqn: <http://www.wikidata.org/prop/qualifier/value-normalized/> .
@prefix pr: <http://www.wikidata.org/prop/reference/> .
@prefix prv: <http://www.wikidata.org/prop/reference/value/> .
@prefix prn: <http://www.wikidata.org/prop/reference/value-normalized/> .
@prefix wdno: <http://www.wikidata.org/prop/novalue/> .
@prefix singleton: <http://www.sigleton.com/> .
"""

def bind_graph(g):
    wd = Namespace('http://www.wikidata.org/entity/')
    g.bind(wd, 'wd')
    wdt = Namespace('http://www.wikidata.org/prop/direct/')
    g.bind(wdt, 'wdt')
    s = Namespace('http://www.wikidata.org/entity/statement/')
    g.bind(s, 's')
    schema = Namespace('http://schema.org/')
    g.bind(schema, 'schema')
    singleton = Namespace('http://www.sigleton.com/')
    g.bind(singleton, 'singleton')

def filter_languages(json_file):
    selectors = ['labels', 'descriptions', 'aliases']
    for entity in json_file['entities']:
        for selector in selectors:
            if json_file['entities'][entity][selector] != {}:
                lang_list = list(json_file['entities'][entity][selector])
                if 'en' in lang_list:
                    for lang in lang_list:
                        if lang != 'en':
                            del json_file['entities'][entity][selector][lang]
    return json_file

def singleton_pybars(json_file):
    source = u"""
{{#each entities}}

  {{#each labels}}
    wd:{{../.id}} rdfs:label "{{escape this.value}}"@{{this.language}} ;
    skos:prefLabel "{{escape this.value}}"@{{this.language}} ;
    schema:name "{{escape this.value}}"@{{this.language}} .
  {{/each}}

  {{#each descriptions}}
    wd:{{../.id}} schema:description "{{escape this.value}}"@{{this.language}}.
  {{/each}}

  {{#each aliases}}
    {{#each this}}
      wd:{{../../.id}} skos:altLabel "{{escape this.value}}"@{{this.language}}.
    {{/each}}
  {{/each}}


  {{#each claims}}
    {{#each this}}

      wd:{{../../.id}} s:{{nd this.id}} {{dataValue this.mainsnak.datavalue}}.
      s:{{nd this.id}} singleton:singletonPropertyOf wdt:{{this.mainsnak.property}} .

      s:{{nd this.id}} wikibase:rank wikibase:{{tc this.rank}}Rank.
      {{#each qualifiers}}
        {{#each this}}
          s:{{nd ../../.id}} p:{{this.property}} {{dataValue this.datavalue}}.
        {{/each}}
      {{/each}}


    {{/each}}
  {{/each}}
{{/each}}
"""

    def _dataValue(this, arg):
        if not arg:
            return 'wdno:NO_TYPE'
        if arg['type'] == 'wikibase-entityid':
            return 'wd:' + arg['value']['id']
        if arg['type'] == 'monolingualtext':
            return "\"" + arg['value']['text'].replace('\"', '\\\"') + "\"@" + arg['value']['language']
        if arg['type'] == 'string':
            return "\"" + arg['value'].replace('\"', '\\\"') + '\"'
        if arg['type'] == 'time':
            return "\"" + arg['value']['time'] + "\"" + "^^xsd:dateTime"
        if arg['type'] == 'quantity':
            return "\"" + arg['value']['amount'] + "\"" + "^^xsd:decimal"
        if arg['type'] == 'globecoordinate':
            return "Point(" + arg['value']['longitude'] + ' ' + arg['value']['latitude'] + "\"" + "^^geo:wktLiteral"
        else:
            return arg['type'] + '   # WARNING Unmanaged value'

    def _tc(this, aString):
        return aString[0].upper() + aString[1:].lower()

    def _uc(this, aString):
        return aString.upper()

    def _nd(this, arg):
        return arg.replace('$', '-')

    def _escape(this, aString):  # non va
        string = aString.replace('"', '\\\"')
        string2 = string.replace('&#x27;', '\'')
        return string2

    # def _ifEquals(arg1, arg2, options)

    helpers = {'dataValue': _dataValue, 'tc': _tc, 'uc': _uc, 'nd': _nd, 'escape': _escape}

    compiler = pybars.Compiler()
    template = compiler.compile(source)

    output = template(json_file, helpers=helpers)
    return output


directory_name = 'E:/wiki/output_data/test2/'
directory = os.fsencode(directory_name)
final_graph = rdflib.Graph()

for file in os.listdir(directory):
    g = rdflib.Graph()
    filename = os.fsdecode(file)
    if filename.endswith(".json"):
        f = open(directory_name + '/' + filename, encoding='utf-8')
        print(filename)
        json_file = json.load(f) # input jsons
        short_json = filter_languages(json_file)
        prov_graph = prefixes + singleton_pybars(short_json)
        single_graph = prov_graph.replace("\/", "/")
        #single_graph = single_graph.replace("\"", "")
        #single_graph = single_graph.replace("\\", "/")
        single_graph = single_graph.replace("&quot;", "\"")
        try:
            g.parse(data=single_graph, format='ttl')
            final_graph = final_graph + g
        except:
            print(filename, 'parsing failed')
        print(len(final_graph))
        continue
    else:
        continue

bind_graph(final_graph)
final_graph.serialize('prova.ttl', format='ttl') # needs to be saved in hard disk
