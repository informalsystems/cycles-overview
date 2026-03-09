import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np

def graph_print(G, order=None):
  """
  Prints a directed graph as a square matrix with edge capacities
  with node names for columns and rows using Pandas.

  Args:
      G (nx.DiGraph): The directed graph to print.
      order (list, optional): A list of node names to use for row and column order.
          Defaults to None (uses node order from the graph).
  """
  capacity_matrix = nx.attr_matrix(G, edge_attr='capacity', rc_order=order)

  if order == None:
    names = capacity_matrix[1]
    capacities = capacity_matrix[0]
  else:
    names = order
    capacities = capacity_matrix
 
  # Convert matrix to DataFrame
  df = pd.DataFrame(capacities, columns=names, index=names, dtype=np.int64)
  
  # Print the DataFrame
  print(df)
  print()
  

def graph_draw(G, layout_func=nx.circular_layout, edgecolors="black", pos=None, connectionstyle="arc3, rad=0.3", node_size=300, update_edge_labels={}, figsize=(5, 5)):
  """
  Visualizes a settlement network with node labels and edge capacities.

  This function utilizes the NetworkX library to create a visual representation
  of a settlement network (`G`). Nodes in the network represent entities, and edges
  represent connections between them. The function allows for customization of
  various visual aspects.

  Args:
      G (nx.DiGraph): The directed graph object representing settlement network.
      layout_func (function, optional): A function used to arrange the nodes in the graph.
          Defaults to `nx.circular_layout` which positions nodes in a circular layout.
          Users can provide alternative layout functions from NetworkX for different node arrangements.
      edgecolors (str, optional): The color of the edges in the graph (e.g., "red", "blue").
          Defaults to "black".
      pos (dict, optional): A dictionary specifying pre-defined node positions.
          If provided, this dictionary will be used for node placement instead of the `layout_func`.
          The dictionary keys should be node identifiers from the graph `G`, and the values
          should be tuples representing (x, y) coordinates for each node position.
          **Note:** Using `pos` overrides the `layout_func`.
      connectionstyle (str, optional): Defines the visual style of the edges, including curvature.
          Defaults to "arc3, rad=0.3" which creates curved edges with a radius of 0.3.
          Consult NetworkX documentation for available connection styles.
      node_size (int, optional): The size of the nodes in the visualization (in pixels).
          Defaults to 300.
      update_edge_labels (dict, optional): A dictionary used to update edge labels displayed in the visualization.
          The dictionary keys should be tuples representing the source and target nodes of an edge.
          The values should be the desired labels to be displayed on those edges.
          **Note:** This dictionary allows for modification of existing edge labels in the graph `G`.
  """
  # Get node positions using the specified layout function
  if pos == None:
    pos = layout_func(G)

  # Create the plot
  plt.figure(figsize=figsize)  # Adjust figure size as needed

  # Draw nodes and edges
  nx.draw_networkx_nodes(
    G, 
    pos, 
    node_size=node_size, 
    edgecolors=edgecolors, 
    node_color="white", 
    node_shape='o'
  )

  # Define edge styles based on "o/c" data
  edge_styles = ["solid" if G.edges[edge].get("o/c", "o") == "o" else "dashed" for edge in G.edges()]

  # Draw edges with style based on "o/c" data
  nx.draw_networkx_edges(
      G,
      pos,
      edge_color="black",
      connectionstyle=connectionstyle,
      width=1,
      alpha=0.7,
      node_size=node_size,
      style=edge_styles
  )

  # Draw node labels
  nx.draw_networkx_labels(G, pos, font_size=8)

  # Draw edge capacities as annotations near edges
  edge_labels = {(u, v): d['capacity'] for u, v, d in G.edges(data=True)}
  # Update edge annotations to present special case like: discounts, infinity,...
  edge_labels.update(update_edge_labels)
  nx.draw_networkx_edge_labels(G, pos, connectionstyle=connectionstyle, edge_labels=edge_labels, font_size=8)

  # Customize plot
  plt.axis('off')  # Hide axes

  # Display the plot
  plt.show()