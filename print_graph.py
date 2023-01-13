import forceatlas2.fa2 as fa2
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
from itertools import count


def print_graph(grafo):

    # divide i gruppi e assegna un colore
    groups = set(nx.get_node_attributes(grafo,'coalition').values())
    mapping = dict(zip(sorted(groups),count()))
    nodes = grafo.nodes()
    colors = [mapping[grafo.nodes[n]['coalition']] for n in nodes]

    forceatlas2 = fa2.ForceAtlas2(
        # Behavior alternatives
        outboundAttractionDistribution=True,  # Dissuade hubs
        linLogMode=False,  # NOT IMPLEMENTED
        adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
        edgeWeightInfluence=1.0,

        # Performance
        jitterTolerance=0.9,  # Tolerance
        barnesHutOptimize=True,
        barnesHutTheta=1.2,
        multiThreaded=False,  # NOT IMPLEMENTED

        # Tuning
        scalingRatio=1.0,
        strongGravityMode=False,
        gravity=30.0,

        # Log
        verbose=True)

    position = forceatlas2.forceatlas2_networkx_layout(grafo, pos=None, iterations=2000, weight_attr="weight")
    # weight_attr='weight'

    ec = nx.draw_networkx_edges(grafo, position, alpha=0.2)
    nc = nx.draw_networkx_nodes(grafo, position, nodelist=nodes,
                                node_color=colors,
                                node_size=100,
                                cmap=plt.cm.jet,
                                edgecolors='black')

    print(grafo.edges(data=True))

    label_dict = {}
    for k, v in position.items():
        tmp = list(v)
        tmp[1] -= 0.9
        label_dict[k] = tmp

    nx.draw_networkx_labels(grafo, pos=label_dict, font_size=8)
    plt.axis('off')
    plt.savefig("modello.png", dpi=1280, bbox_inches='tight')
    plt.show()