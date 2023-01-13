import networkx as nx
from oop_model import Game
from grafo_nx import g
from print_graph import print_graph

gate = 0

target_list = ['United States', 'United Kingdom', 'France', 'Israel', 'India', 'North Europe', 'Middle Europe',
               'Arabia', 'South Europe', 'East Europe', 'Turkey', 'Japan', 'South Korea', 'Australia', 'New Zealand',
               'Canada', "North Africa", "West Africa", "Central Africa", "Southern Africa", "Eastern Africa", "Southeast Africa",
               "Caucasian States", "Nepal", "Bangladesh", "Southeast Asia", "South America", "Central America"]

NuclearGame = Game(g, target_list)

while gate <= 10:
    NuclearGame.start_third_stage()
    NuclearGame.reset()
    G = NuclearGame.g
    gate += 1

NuclearGame.update_status()

print_graph(G)

for k,v in nx.degree_centrality(G).items():
    print(f"Il grado pesato di {k} è {g.degree(k, weight='weight')}")

print(nx.average_neighbor_degree(G, weight="weight"))





