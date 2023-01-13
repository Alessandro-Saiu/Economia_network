import pandas as pd
import networkx as nx
from random import choice
import forceatlas2.fa2 as fa2
import matplotlib.pyplot as plt
import matplotlib
from itertools import count


g = nx.Graph()

g.add_nodes_from(["United States",
                  "Russia",
                  "United Kingdom",
                  "France",
                  "China",
                  "Israel",
                  "India",
                  "Pakistan",
                  "North Korea",
                  "North Europe",
                  "Middle Europe",
                  "South Europe",
                  "East Europe",
                  "Turkey",
                  "North Africa",
                  "West Africa",
                  "Central Africa",
                  "Southern Africa",
                  "Eastern Africa",
                  "Southeast Africa",
                  "Syria",
                  "Libano",
                  "Arabia",
                  "Yemen",
                  "Iraq",
                  "Iran",
                  "Caucasian States",
                  "Central Asia",
                  "Nepal",
                  "Bangladesh",
                  "Southeast Asia",
                  "Japan",
                  "South Korea",
                  "Australia",
                  "New Zealand",
                  "South America",
                  "Central America",
                  "Canada"])

coalition_dict = {"United States" : "Leader",
                  "Russia" : "Challenger",
                  "United Kingdom" : "Leader",
                  "France" : "Leader",
                  "China" : "Challenger",
                  "Israel" : "Leader",
                  "India" : "Leader",
                  "Pakistan" : "Challenger",
                  "North Korea" : "Challenger",
                  "North Europe" : "West",
                  "Middle Europe" : "West",
                  "South Europe" : "West",
                  "East Europe" : "West" ,
                  "Turkey" : "West",
                  "North Africa" : "Neutral",
                  "West Africa" : "Neutral",
                  "Central Africa" : "Neutral",
                  "Southern Africa" : "Neutral",
                  "Eastern Africa" : "Neutral",
                  "Southeast Africa" : "Neutral",
                  "Syria" : "Anti-west",
                  "Libano" : "Anti-west",
                  "Arabia" : "West",
                  "Yemen" : "Anti-west",
                  "Iraq" : "Anti-west",
                  "Iran" : "Anti-west",
                  "Caucasian States" : "Neutral",
                  "Central Asia" : "Anti-west",
                  "Nepal" : "Neutral",
                  "Bangladesh" : "Neutral",
                  "Southeast Asia" : "Neutral",
                  "Japan" : "West",
                  "South Korea" : "West",
                  "Australia" : "West",
                  "New Zealand" : "West",
                  "South America" : "Neutral",
                  "Central America" : "Neutral",
                  "Canada" : "West"}

warheads_dict = {"China" : 350,
                 "United States": 3708,
                 "Russia" : 4477,
                 "United Kingdom" : 180,
                 "France" : 290,
                 "Israel" : 90,
                 "India" : 160,
                 "Pakistan" : 165,
                 "North Korea" : 20}

nx.set_node_attributes(g, coalition_dict, "coalition" )
nx.set_node_attributes(g, warheads_dict, "n_warheads" )

# creazione delle coalizioni di partenza

leaders = ["United States", "United Kingdom", "France", "Israel", "India"]
challengers = ["China", "Russia", "Pakistan", "North Korea"]
challenger_ally = ["Syria","Libano", "Yemen", "Iraq", "Iran", "Central Asia"]
weight_dict = {}

for node_r, attributes_r in g.nodes(data=True):
    if "Leader" in attributes_r.values():
        g.add_edges_from([(node_r, node) for node, attributes in g.nodes(data=True)
                          if coalition_dict.get(node) == "Leader"
                          and node != node_r])
    elif "Challenger" in attributes_r.values():
        g.add_edges_from([(node_r, node) for node, attributes in g.nodes(data=True)
                          if coalition_dict.get(node) == "Challenger"
                          and node != node_r])
    elif "West" in attributes_r.values():
        g.add_edges_from([(node_r, node) for node, attributes in g.nodes(data=True)
                          if coalition_dict.get(node) == "Leader"
                          and node != node_r])
    elif "Anti-west" in attributes_r.values():
        g.add_edges_from([(node_r, node) for node, attributes in g.nodes(data=True)
                          if coalition_dict.get(node) == "Challenger"
                          and node != node_r])

for edge in g.edges():
    if edge[0] in leaders and edge[1] in leaders:
        weight_dict[edge] = 5
    elif edge[0] in challengers and edge[1] in challengers:
        weight_dict[edge] = 5
    elif edge[0] in challengers and edge[1] in challenger_ally:
        weight_dict[edge] = 5
    else:
        weight_dict[edge] = 5

nx.set_edge_attributes(g, weight_dict, "weight")

# attribuzione casuale dei tratti che influenzano il comportamento dei diversi paesi

status_1 = ["reliable", "unreliable"]
status_2 = ["hard", "soft"]
status_3 = ["ambitious", "content"]

player_status_1 = {}
player_status_2 = {}
player_status_3 = {}

for country in g.nodes():
    player_status_1[country] = choice(status_1)
    player_status_2[country] = choice(status_2)
    player_status_3[country] = choice(status_3)


nx.set_node_attributes(g, player_status_1, "reliability")
nx.set_node_attributes(g, player_status_2, "stance")
nx.set_node_attributes(g, player_status_3, "aptitude")

# groups = set(nx.get_node_attributes(g,'coalition').values())
# mapping = dict(zip(sorted(groups),count()))
# nodes = g.nodes()
# colors = [mapping[g.nodes[n]['coalition']] for n in nodes]
#
# forceatlas2 = fa2.ForceAtlas2(
#                         # Behavior alternatives
#                         outboundAttractionDistribution=True,  # Dissuade hubs
#                         linLogMode=False,  # NOT IMPLEMENTED
#                         adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
#                         edgeWeightInfluence=1.0,
#
#                         # Performance
#                         jitterTolerance=0.5,  # Tolerance
#                         barnesHutOptimize=False,
#                         barnesHutTheta=1.2,
#                         multiThreaded=False,  # NOT IMPLEMENTED
#
#                         # Tuning
#                         scalingRatio=0.01,
#                         strongGravityMode=False,
#                         gravity=4.9,
#
#                         # Log
#                         verbose=True)
#
# position = forceatlas2.forceatlas2_networkx_layout(g, pos=None, iterations=2000, weight_attr="weight")
# # weight_attr='weight'
#
# ec = nx.draw_networkx_edges(g, position, alpha=0.2)
# nc = nx.draw_networkx_nodes(g, position, nodelist=nodes,
#                             node_color=colors,
#                             node_size=100,
#                             cmap=plt.cm.jet,
#                             edgecolors='black')
#
# print(g.edges(data=True))
#
# label_dict = {}
# for k, v in position.items():
#     tmp = list(v)
#     tmp[1] -= 0.03
#     label_dict[k] = tmp
#
# # nx.draw_networkx_labels(g, pos=label_dict, font_size=8)
# plt.axis('off')
# plt.savefig("prova.png", dpi=1280, bbox_inches='tight')
# plt.show()
#
# for k,v in nx.degree_centrality(g).items():
#     print(f"\nIl grado di {k} è {v}")
#
# for k,v in nx.betweenness_centrality(g, normalized=False).items():
#     print(f"\nLa betweennes di {k} è {v}")


