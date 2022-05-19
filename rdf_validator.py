from rdflib import Graph, ConjunctiveGraph, Namespace


# USE IT FOR ngraphs.trig // and then, for conjectures
g_quads = ConjunctiveGraph()
g_quads.parse("FILE_PATH", format="trig")
print(len(g_quads))

# USE IT FOR ALL OTHERS
g_triples = Graph()
g_triples.parse("FILE_PATH", format="ttl")
print(len(g_triples))


# SAMPLE OF 2000 JSONS FILES OF FAKE
# DONE: singleton --> len = 9352810 triples
# DONE: ngraphs --> len = 7354742 quads

