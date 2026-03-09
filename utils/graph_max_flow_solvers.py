import networkx as nx

# ------------------------ #
# Max flow solver helpers  #
# ------------------------ #

def build_flow_directory(R):
    """
    Builds a nested flow directory from a residual graph (R), using edge 'flow' attribute for values.

    Args:
        R (networkx.DiGraph): A directed graph representing the residual network.

    Returns:
        dict: A nested dictionary representing the flow directory.
    """
    return {u: {v: flow_value for _, v, flow_value in R.edges(u, data="flow") if flow_value > 0} for u in R.nodes}


"""
Small helper functions to get flow directories from various NetworkX flow functions

Args:
    G (networkx.DiGraph): Directed graph representing the settlement network

Returns:
    dict: A nested dictionary representing the flow directory.
"""

def max_flow_min_cost(G, source, target):
    flow = nx.max_flow_min_cost(G, source, target)
    return flow

def max_flow(G, source, target):
    (_, flow) = nx.maximum_flow(G, source, target)
    return flow

def network_simplex(G, source, target):
    # Deconstruct source-target network and replace with node demands
    for successor in G.successors(source):
        G.nodes[successor]["demand"] = -G[source][successor]["capacity"]
    for predecessor in G.predecessors(target):
        G.nodes[predecessor]["demand"] = G[predecessor][target]["capacity"]
    G.remove_node(source)
    G.remove_node(target)
    # Run on smaller network for performance
    (_, flow) = nx.network_simplex(G)
    return flow

def diniz(G, source, target):
    R = nx.flow.dinitz(G, source, target)
    flow = build_flow_directory(R)
    return flow

def preflow_push(G, source, target):
    R = nx.flow.preflow_push(G, source, target)
    flow = build_flow_directory(R)
    return flow

def edmonds_karp(G, source, target):
    R = nx.flow.edmonds_karp(G, source, target)
    flow = build_flow_directory(R)
    return flow

def boykov_kolmogorov(G, source, target):
    R = nx.flow.boykov_kolmogorov(G, source, target)
    flow = build_flow_directory(R)
    return flow

def shortest_augmenting_path(G, source, target):
    R = nx.flow.shortest_augmenting_path(G, source, target)
    flow = build_flow_directory(R)
    return flow

# Available algorithms with slow algorithms commented out
available_algorithms = [max_flow_min_cost,
                        max_flow,
                        network_simplex,
                        # diniz,
                        preflow_push,
                        # edmonds_karp,
                        boykov_kolmogorov,
                        shortest_augmenting_path ]

# ------------------------- #
# Max flow solver framework #
# ------------------------- #

def max_flow_solver(G, max_flow_algo=max_flow_min_cost):
    """
    Reduces a network graph (G) to identify potential cycles and returns a DiGraph representing 
    the cyclic structure after finding a maximum flow solution using the specified algorithm.

    Args:
        G (nx.DiGraph): A NetworkX directed graph representing the liabilities network.
        max_flow_algo (callable, optional): The maximum flow algorithm to use. 
            Defaults to "max_flow_min_cost". Other options include functions from the 
            available_algorithms list (e.g., max_flow, network_simplex, etc.).

    Returns:
        nx.DiGraph: A NetworkX directed graph representing the cyclic structure after finding 
                   the maximum flow solution.
    """
    # Copy the graph to avoid modifying the original
    L = G.copy()

    # Remove head and tail nodes with no incoming or outgoing edges
    heads_and_tails = True
    while heads_and_tails:
        heads_and_tails = False
        remove_list = [n for n in L.nodes if not list(L.predecessors(n)) or not list(L.successors(n))]
        if remove_list:
            heads_and_tails = True
            L.remove_nodes_from(remove_list)

    # Candidates for cyclic structure
    all_edges = [n for n in L.edges.data("capacity")]

    # Add source and target nodes to balance the reduced graph
    source, target = "source", "target"
    for firm in [n for n in L.nodes]:  # Create a list copy of nodes to iterate over
        net_position = sum(L[d][firm]["capacity"] for d in L.predecessors(firm)) - \
                       sum(L[firm][c]["capacity"] for c in L.successors(firm))
        if net_position < 0:
            L.add_edge(source, firm, capacity=-net_position, weight=1)  # Inflow
        else:
            L.add_edge(firm, target, capacity=net_position, weight=1)  # Outflow

    # Find maximum flow solution based on chosen algorithm if the network is imbalanced
    max_flow = max_flow_algo(L, source, target) if source in L.nodes() else {}

    # Create a DiGraph of the cyclic structure
    cyclic_structure = nx.DiGraph()
    for (debtor, creditor, capacity) in all_edges:
        if debtor not in max_flow or creditor not in max_flow[debtor]:
            # Not in max flow, add to cyclic structure
            cyclic_structure.add_edge(debtor, creditor, capacity=capacity)
        else:
            # Substract max_flow from the edge and add to cyclic structure
            remaining_flow = capacity-max_flow[debtor][creditor]
            if remaining_flow > 0:
                cyclic_structure.add_edge(debtor, creditor, capacity=remaining_flow)

    return cyclic_structure