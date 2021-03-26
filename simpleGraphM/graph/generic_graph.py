import copy
from .graph import Graph

class GenericGraph(Graph):
    """A class for the most generic graph type

    Stores both an adjaceny list and cost table

    Parameters:
        edge_dict (dict): Contains all edges and the respective weight, i.e. {('v1', 'v2'): 5.0}
        graph_type (str): "undirected" or None
        visualize (str): Whether to use networkx to visualize results

    Attributes:
        adjList (dict): For each node, a list of adjacent nodes are given
        edge_dict (dict): For each edge, a weight is given

    Todo: 
        - fix visualization for larger graphs
        - Need further test the adjaceny list!
        - Need to update Adjaceny list, whenever cost table is updated!

    """
    def __init__(self, edge_dict=None, vertex_dict=None, graph_type="undirected", deep_copy=True, default_value=0):
        self.adjList = {}

        if deep_copy:
            self.edge_dict = copy.deepcopy(edge_dict) 
            self.vertex_dict = copy.deepcopy(vertex_dict)
        else:
            self.edge_dict = edge_dict
            self.vertex_dict = vertex_dict

        if self.edge_dict is not None:
            # undirected vs directed edges
            if graph_type is "undirected":
                temp = {}
                for key in edge_dict.keys():
                    temp.update({(key[1], key[0]): edge_dict[key]})
                self.edge_dict.update(temp)
            
            # create an adjacency list!
            for key in self.edge_dict.keys():
                if key[0] not in self.adjList:
                    self.adjList[key[0]] = [key[1]]
                if key[1] not in self.adjList:
                    self.adjList[key[1]] = [key[0]]
                else:
                    if key[0] not in self.adjList[key[1]]:
                        self.adjList[key[1]].append(key[0])
                    if key[1] not in self.adjList[key[0]]:
                        self.adjList[key[0]].append(key[1])                

    def edge_count(self):
        if self.edge_dict is not None:   
            return len(self.edge_dict)
        else:
            return 0

    def node_count(self):
        return len(self.adjList) 

    def add_edge(self, edge_dict):
        """Add edges to our graph
        
        Arg:
            edge_dict (dict): i.e. {('v1', 'v2'): 5.0}
        
        """
        self.edge_dict.update(edge_dict)

    def add_vertex(self, vertex_dict):
        """Vertex to our graph

        Arg:
            vertex_dict (dict): {'v1': 5}
        
        """
        self.vertex_dict.update(vertex_dict)
   
    def remove_edges(self, edge_list):
        """Delete specific edges in our graph

        Arg:
            edge_list (iter of edges): 

        """
        for e in edge_list:
            #self.edge_dict.pop(e)  #slightly slower
            del self.edge_dict[e]

    def remove_vertices(self, vertex_list):
        """Delete vertices from our graph

        Arg:
            vertex_list (iter of vertices):
        
        """
        for v in vertex_list:
            del self.vertex_dict[v]

    def neighbors(self, v):
        """Return a list of neighbors of v
        
        Todo:
            - just return adjList[v]!
        
        """
        # neighs = [n for n in self.adjList[v]]
        neighs = self.adjList[v]
        return neighs
    
    def cost(self, *args):
        """Return cost of edge or vertex based on number of args

        Args:
            from_node, to_node (vertex, vertex): Key of vertices, contained in edgeDict
            node (vertex): Key of a single vertex, contained in vertexDict

        """
        try:
            if len(args) == 2:
                from_node, to_node = args
                weight = self.edge_dict[(from_node, to_node)]
                return weight
            elif len(args) == 1:
                node = args[0]
                weight = self.vertex_dict[node]
                return weight
            else:
                print("vertex or edge not found using arguments: ", args)
                raise ValueError
        except Exception as E_:
            print(E_)
            return type(E_)