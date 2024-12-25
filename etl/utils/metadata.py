

def union_graphs(left_graph, right_graph):
    L = left_graph.copy()
    R = right_graph.copy()

    for node, data in R.nodes(data=True):
        if node in L:
            if 'label' in data and 'label' in L.nodes[node]:
                L.nodes[node]['label'] += " | " + data['label']
        else:
            L.add_node(node, **data)

    for u, v in R.edges():
        L.add_edge(u, v)

    return L


def append_to_graph(base_graph, graph):
    G = base_graph.copy()
    J = graph.copy()

    # Merge nodes from J into G, updating labels for common nodes
    for node, data in J.nodes(data=True):
        if node in G:
            # If node exists in G, concatenate labels
            if 'label' in data and 'label' in G.nodes[node]:
                G.nodes[node]['label'] += " | " + data['label']
        else:
            # If node doesn't exist in G, add it
            G.add_node(node, **data)

    # Merge edges from J into G
    for u, v in J.edges():
        G.add_edge(u, v)

    return G