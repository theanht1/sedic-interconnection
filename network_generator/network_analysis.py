from igraph import*
import sys

## Read edges file
def read_edges(file_edges):
  f_edges = open(file_edges, "r")

  line = f_edges.readline().split(" ")
  n_node, n_base_link, n_random_link = map(lambda x: int(x), line)

  edges = []
  ## Read base links
  for index in range(n_base_link):
    line = f_edges.readline().split(" ")
    line_int = []
    line_int.append(int(line[0]))
    line_int.append(int(line[1]))
    edges.append(line_int)

  ## Read random links
  for index in range(n_random_link):
    line = f_edges.readline().split(" ")
    n_random_link = int(line[0])
    alpha = float(line[1])
    for r_index in range(n_random_link):
      line = f_edges.readline().split(" ")
      line_int = []
      line_int.append(int(line[0]))
      line_int.append(int(line[1]))
      line_int.append(alpha)
      edges.append(line_int)

  return n_node, n_base_link, n_random_link, edges

def create_graph(n_node, edges):
  graph = Graph()
  graph.add_vertices(n_node)
  for index in range(len(edges)):
    graph.add_edge(edges[index][0], edges[index][1])

  return graph

## Total shorest path = total path length of every pair of nodes
def get_total_shortest_path(n_node, graph):
  total_shortest_path = 0
  for index in range(n_node):
    all_paths = graph.get_shortest_paths(index)
    total_shortest_path += sum(map(lambda x:len(x) - 1, all_paths))

  return total_shortest_path

def get_average_shortest_path(n_node, total_shortest_path):
  return total_shortest_path / (n_node ** 2)

def main():
  # print(len(sys.argv))
  file_geos = sys.argv[1]
  file_edges = sys.argv[2]
  
  n_node, n_base_link, n_random_link, edges = read_edges(file_edges)
  # print(n_node, n_base_link, n_random_link)
  # print(edges)
  graph = create_graph(n_node, edges)

  diameter = graph.diameter(directed = False)
  # print(diameter)
  # print(graph)
  # print(graph.degree())
  total_shortest_path = get_total_shortest_path(n_node, graph)
  average_shortest_path = get_average_shortest_path(n_node, total_shortest_path)
  # print(total_shortest_path)
  # print(average_shortest_path)

  result = {
             'diameter': diameter,
             'total_shortest_path': total_shortest_path,
             'average_shortest_path':average_shortest_path
           }
  print(result)

main()
  
