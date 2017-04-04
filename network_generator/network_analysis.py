from igraph import *
import sys

##
# Read geos file
#
def read_geos(file_geos):
  f_geos = open(file_geos, "r")

  n_node = int(f_geos.readline())
  geos = []
  for index in range(n_node):
    line = f_geos.readline().split(" ")
    x, y, z = map(lambda x: int(x), line)
    geos.append([x, y, z])

  return n_node, geos

##
# Read edges file
#
def read_edges(file_edges):
  f_edges = open(file_edges, "r")

  line = f_edges.readline().split(" ")
  n_node, n_link, n_random_link = map(lambda x: int(x), line)

  edges = []
  ## Read links
  for index in range(n_link):
    line = f_edges.readline().split(" ")
    if len(line) == 2:
      x, y = map(lambda x: int(x), line)
      edges.append([x, y])
    else:
      x = int(line[0])
      y = int(line[1])
      n_r = int(line[2])
      alpha = float(line[3])

      edges.append([x, y, n_r, alpha])
  
  return n_node, n_link, n_random_link, edges


def create_graph(n_node, edges):
  graph = Graph()
  graph.add_vertices(n_node)
  for index in range(len(edges)):
    graph.add_edge(edges[index][0], edges[index][1])    

  return graph

## Total shorest path = total path length of every pair of nodes
def get_total_shortest_path(n_node, graph):
  all_paths = graph.shortest_paths()
  return sum(map(lambda x: sum(x), all_paths))

def get_average_shortest_path(n_node, total_shortest_path):
  return total_shortest_path / (n_node ** 2)

## Main process
def main():
  # Get file name from parameter
  file_geos = sys.argv[1]
  file_edges = sys.argv[2]
  
  # Read info from geos file
  n_node, geos = read_geos(file_geos)

  # Read info from edges file
  n_node, n_random_link, n_random_link, edges = read_edges(file_edges)

  # Create igraph
  graph = create_graph(n_node, edges)
  # print(graph)

  diameter = graph.diameter(directed = False)

  if n_node <= 1024:
    total_shortest_path = get_total_shortest_path(n_node, graph)
    average_shortest_path = get_average_shortest_path(n_node, total_shortest_path)
  else:
    total_shortest_path = 0
    average_shortest_path = 0

  if n_node > 512:
    geos = []
    edges = []

  result = {
             'geos': geos,
             'edges': edges,
             'n_random_links': n_random_link,
             'diameter': diameter,
             'total_shortest_path': total_shortest_path,
             'average_shortest_path':average_shortest_path
           }
  print(result)

main()
  
