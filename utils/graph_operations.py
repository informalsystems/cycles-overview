import networkx as nx

class ExtendedGraph:
  def __add__(self, other):
    return add(self, other)

  def __sub__(self, other):
    return sub(self, other)

  def __pos__(self):
    return pos(self)

  def __neg__(self):
    return neg(self)

  def __invert__(self):
    return tra(self)

setattr(nx.Graph,'__add__',ExtendedGraph.__add__)
setattr(nx.Graph,'__sub__',ExtendedGraph.__sub__)
setattr(nx.Graph,'__pos__',ExtendedGraph.__pos__)
setattr(nx.Graph,'__neg__',ExtendedGraph.__neg__)
setattr(nx.Graph,'__invert__',ExtendedGraph.__invert__)


def add(G, H):
  """
  Calculates the element-wise sum of edge capacities between two directed graphs.

  This function creates a new directed graph representing the sum of
  capacities for corresponding edges in `G1` and `G2`. If an edge exists
  in only one graph, its capacity is added to the new graph.

  Args:
      G (nx.DiGraph): The first directed graph.
      H (nx.DiGraph): The second directed graph.

  Returns:
      nx.DiGraph: A new directed graph representing the sum of capacities from G and H.
  """
  sum = nx.DiGraph(G) # Create a copy of G to avoid modifying the original graph
  nx.compose(sum, H) # Use compose to combine node and edge sets, keeping edge attributes (capacities)
  
  for u, v, attr in H.edges(data=True): # Iterate through edges in H to update capacities for existing edges
    if sum.has_edge(u, v):
      sum[u][v]["capacity"] += attr["capacity"]
    else:
      sum.add_edge(u, v, **attr)
  
  return sum


def sub(G, H):
  """
  Calculates the element-wise difference of edge capacities between two directed graphs.

  This function creates a new directed graph representing the difference of
  capacities for corresponding edges in `G` and `H`. If an edge exists in only
  one graph, its negative capacity is added to the new graph.

  Args:
      G (nx.DiGraph): The first directed graph.
      H (nx.DiGraph): The second directed graph.

  Returns:
      nx.DiGraph: A new directed graph representing the difference of capacities from G and H.
  """
  sub = nx.DiGraph(G) # Create a copy of G to avoid modifying the original graph
  nx.compose(sub, H) # Use compose to combine node and edge sets, keeping edge attributes (capacities)
  
  for u, v, attr_dict in H.edges(data=True): # Iterate through edges in H to update capacities for existing edges
    if sub.has_edge(u, v):
      sub[u][v]["capacity"] -= attr_dict["capacity"]
      if sub[u][v]["capacity"] == 0: # Remove the edge if the capacity is zero
        sub.remove_edge(u, v)
    else:
      sub.add_edge(u, v, capacity=-attr_dict["capacity"])
    
  return sub


def pos(G):
  """
  Returns a new graph containing only edges with positive capacities from the original graph.

  Args:
      G (nx.DiGraph): The original directed graph.

  Returns:
      nx.DiGraph: A new directed graph containing only positive capacity edges.
  """
  pos = nx.DiGraph(G) # Create a copy of G to avoid modifying the original graph
  
  for u, v, attr_dict in G.edges(data=True): # Iterate through edges in G to remove negative and zero capacity edges
    if attr_dict["capacity"] <= 0:
      pos.remove_edge(u, v)

  return pos


def neg(G):
  """
  Returns a new graph containing only the absolute values of negative capacity edges from the original graph.

  Args:
      G (nx.DiGraph): The original directed graph.

  Returns:
      nx.DiGraph: A new directed graph containing absolute values of negative capacity edges.
  """
  neg = nx.DiGraph(G) # Create a copy of G to avoid modifying the original graph

  for u, v, attr_dict in G.edges(data=True): # Iterate through edges in G to update negative capacities and remove positive and zero capacity edges
    if attr_dict["capacity"] < 0:
      neg[u][v]["capacity"] = abs(attr_dict["capacity"])
    else:
      neg.remove_edge(u, v)

  return neg


def tra(G):
  """
  Creates a new directed graph representing the transpose of the original graph.

  The transpose swaps the source and target nodes for each edge.

  Args:
      G (nx.DiGraph): The original directed graph.

  Returns:
      nx.DiGraph: A new directed graph representing the transpose of G.
  """
  transpose = nx.DiGraph() # Create a new DiGraph
  
  for u, v, attr_dict in G.edges(data=True): # Iterate through edges in G to create a transposed graph
    transpose.add_edge(v, u, capacity=attr_dict["capacity"])

  return transpose


def total_debt(G):
  """
  Calculates the total debt in the graph.

  This function iterates over all edges in the directed graph `G` and sums 
  the 'capacity' attribute of each edge. The 'capacity' attribute represents
  the debt associated with an edge.

  Args:
      G (nx.DiGraph): A directed NetworkX graph.

  Returns:
      int: The total debt value summed across all edges in the graph.
  """
  total_debt = 0
  for u, v, edge_data in G.edges(data=True):  # Iterate with edge data
      debt = edge_data.get("capacity", 0)  # Handle potential missing capacity
      total_debt += debt

  return total_debt

def balance_vector(G):
    """
    Calculates the balance vector of a directed graph.

    The balance vector is computed as the difference between the total incoming and outgoing capacities for each node.

    Args:
        G (nx.DiGraph): A directed graph.

    Returns:
        dict: A dictionary where keys are nodes and values are their balance (incoming - outgoing).
    """
    balance = {node: 0 for node in G.nodes}  # Initialize balance for each node

    for u, v, edge_data in G.edges(data=True):
        capacity = edge_data.get("capacity", 0)  # Get the capacity of the edge
        balance[u] -= capacity  # Outgoing edges decrease balance
        balance[v] += capacity  # Incoming edges increase balance

    return balance

def debit_vector(G):
    """
    Calculates the debit vector of a directed graph.

    The debit vector is computed as the total outgoing capacity for each node.

    Args:
        G (nx.DiGraph): A directed graph.

    Returns:
        dict: A dictionary where keys are nodes and values are their total outgoing capacities.
    """
    debit = {node: 0 for node in G.nodes}  # Initialize debit for each node

    for u, v, edge_data in G.edges(data=True):
        capacity = edge_data.get("capacity", 0)  # Get the capacity of the edge
        debit[u] += capacity  # Outgoing edges increase debit

    return debit

def credit_vector(G):
    """
    Calculates the credit vector of a directed graph.

    The credit vector is computed as the total incoming capacity for each node.

    Args:
        G (nx.DiGraph): A directed graph.

    Returns:
        dict: A dictionary where keys are nodes and values are their total incoming capacities.
    """
    credit = {node: 0 for node in G.nodes}  # Initialize credit for each node

    for u, v, edge_data in G.edges(data=True):
        capacity = edge_data.get("capacity", 0)  # Get the capacity of the edge
        credit[v] += capacity  # Incoming edges increase credit

    return credit

def is_balanced(G):
    """
    Checks if a directed graph is balanced.

    A graph is considered balanced if the total incoming capacity equals the total outgoing capacity for each node.

    Args:
        G (nx.DiGraph): A directed graph.

    Returns:
        bool: True if the graph is balanced, False otherwise.
    """
    balance = balance_vector(G)
    return all(value == 0 for value in balance.values())