import networkx as nx
import pandas as pd
import json


def read_graph_from_csv(filename):
  """
  Reads a directed graph with edge capacities (and optionally other attributes) from a CSV file.

  Mandatory columns are:

  - debtor: The source node of the edge.
  - creditor: The target node of the edge.
  - amount: Used for capacity. The amount of flow allowed on the edge (an integer).

  Weight handling:

  - If a column named "weight" is present in the CSV file, its values are used as edge weights.
  - If the "weight" column is missing, all edges are assigned a weight of 1. This is required for proper execution of minimum cost algorithms.

  Args:
    filename (str): The path to the CSV file.

  Returns:
    nx.DiGraph: A directed NetworkX graph with edge capacities and additional attributes (if present).
  """
  # Read data as a pandas DataFrame
  df = pd.read_csv(filename)

  # Required columns (modify as needed)
  required_cols = ["debtor", "creditor", "amount"]

  # Check for presence of required columns
  if not all(col in df.columns for col in required_cols):
    raise ValueError(f"Missing required columns: {', '.join(set(required_cols) - set(df.columns))}")

  # Create a NetworkX DiGraph
  G = nx.DiGraph()

  # Iterate through rows (assuming debtor, creditor, and capacity are the first 3 columns)
  for idx, row in df.iterrows():
    debtor, creditor, capacity = row[:3]  # Extract first 3 columns
    # edge_data = {col: row[i] for i, col in enumerate(df.columns) if i > 2}  
    edge_data = {col: row.iloc[i] for i, col in enumerate(df.columns) if i > 2} # Extract additional attributes


    # Add weight if "weight" column is missing, otherwise use existing value
    weight = edge_data.get("weight", 1)  # Get weight if present, default to 1
    edge_data["weight"] = weight

    G.add_edge(debtor, creditor, capacity=int(capacity), **edge_data)

  return G


def split_graph_by_edge_data(G, edge_data_name, edge_data_value):
  """
  Splits a directed graph (G) into two directed graphs based on an edge data attribute.

  Args:
    G (nx.DiGraph): The original directed graph.
    edge_data_name (str): The name of the edge data attribute to filter by.
    edge_data_value (any): The value to match in the edge data attribute.

  Returns:
    tuple: A tuple containing two directed graphs (G1, G2).
        - G1: Contains edges where the specified edge data matches the given value.
        - G2: Contains remaining edges where the data doesn't match the value.
  """
  # Create empty DiGraphs for split graphs
  G1 = nx.DiGraph()
  G2 = nx.DiGraph()

  # Iterate through edges
  for u, v, edge_data in G.edges(data=True):
    # Add edge to G1 if data is missing
    if edge_data.get(edge_data_name, None) == None:
      G1.add_edge(u, v, **edge_data)
    # Add edge to G1 if data matches the value
    elif edge_data[edge_data_name] == edge_data_value:
      G1.add_edge(u, v, **edge_data)
    # Otherwise, add to G2
    else:
      G2.add_edge(u, v, **edge_data)

  return G1, G2


def write_graph_to_csv(G, filename, all_data=False):
  """
  Writes a directed graph with edge capacities to a CSV file.

  By default, only writes the basic columns:
  - debtor: The source node of the edge.
  - creditor: The target node of the edge.
  - amount: The capacity of the edge.

  If all_data=True, includes additional columns for all edge attributes (e.g., weight, type, etc.)

  Args:
    G (nx.DiGraph): A directed NetworkX graph with edge capacities and attributes.
    filename (str): The path to the output CSV file.
    all_data (bool): If True, write all edge attributes. If False (default), only write basic columns.

  Returns:
    None
  """
  # Collect all edge data
  edge_data_list = []

  for u, v, data in G.edges(data=True):
    edge_record = {
      'debtor': u,
      'creditor': v,
      'amount': data.get('capacity', 0)
    }

    # Add all other attributes except 'capacity' (which we already mapped to 'amount')
    if all_data:
      for key, value in data.items():
        if key != 'capacity':
          edge_record[key] = value

    edge_data_list.append(edge_record)

  # Create DataFrame and write to CSV
  df = pd.DataFrame(edge_data_list)

  # Ensure column order: debtor, creditor, amount, then others
  cols = ['debtor', 'creditor', 'amount']
  if all_data:
    other_cols = [col for col in df.columns if col not in cols]
    df = df[cols + other_cols]
  else:
    df = df[cols]

  df.to_csv(filename, index=False)


def read_json_file(filename):
  """
  Reads a JSON file and returns the contents as a dictionary.

  Args:
      filename (str): Path to the JSON file.

  Returns:
      dict: The parsed JSON data as a dictionary.

  Raises:
      FileNotFoundError: If the specified file is not found.
      json.JSONDecodeError: If there's an error parsing the JSON data.
  """

  # Open the file in read mode
  try:
    with open(filename, 'r') as file:
      # Read the entire file content
      data = file.read()
      # Parse JSON data and return as dictionary
      return json.loads(data)
  except FileNotFoundError:
    raise FileNotFoundError(f"Error: File not found - {filename}")
  except json.JSONDecodeError as e:
    raise json.JSONDecodeError(f"Error parsing JSON file {filename}: {e}")
