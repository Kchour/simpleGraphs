import copy
from .graph import Graph

class GenericGraph(Graph):
    """A class for the most generic graph type. Stores both an adjaceny list and cost table

    Parameters:
        edge_dict (dict): Contains all edges and the respective weight, i.e. {('v1', 'v2'): 5.0}. Weights can be anything (a list, a dict)
        vertex_dict (dict): Contains a key-value pair of vertices and their weights
        graph_type (str): "undirected" or "directed" (by default "directed")
        visualize (str): Whether to visualize results using matplotlib (not implemented yet)
        deep_copy (bool): Whether to create a deep copy (rather than a shallow copy) of input dictionaries

    Attributes:
        adjList (dict): For each node, a list of adjacent nodes are given
        edge_dict (dict): For each edge, a weight is given
        vertex_dict (dict): For each node, a weight is given

    Todo: 
        - Add visualization capabilities

    """
    @staticmethod
    def mat_to_dict(mat):
        """Return a edge_dict representation of edges

        Parameter:
            mat (list of list): elements that are nonzero or non-None type specify an adjacency
        
        Return:
            edge_dict (dict): A dict where each entry is a edge, keyed by value of that edge (which could be a hyper edge)

        """
        edge_dict = {}
        for i, row_vect in enumerate(mat):
            for j, val in enumerate(row_vect):
                if val != 0 and val != None:
                    edge_dict.update({(i,j): val})
        return edge_dict

    def __init__(self, edge_dict=None, vertex_dict=None, graph_type="directed", deep_copy=True):
        self.adjList = {}
        self.graph_type = graph_type

        # Deep copy to avoid modifying original graph by reference
        if deep_copy:
            self.edge_dict = copy.deepcopy(edge_dict) 
            self.vertex_dict = copy.deepcopy(vertex_dict)
        else:
            self.edge_dict = edge_dict
            self.vertex_dict = vertex_dict

        if edge_dict is None:
            self.edge_dict = {}
        if vertex_dict is None:
            self.vertex_dict = {}

        if self.edge_dict is not None:
            self._update_adj_list()
            
    def _update_adj_list(self):
        # undirected vs directed edges
        if self.graph_type is "undirected":
            temp = {}
            for key in self.edge_dict.keys():
                temp.update({(key[1], key[0]): self.edge_dict[key]})
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
        else:
            for key in self.edge_dict.keys():
                if key[0] not in self.adjList:
                    self.adjList[key[0]] = [key[1]]
                else:
                    if key[1] not in self.adjList[key[0]]:
                        self.adjList[key[0]].append(key[1])
                if key[1] not in self.adjList:
                    self.adjList[key[1]] = []    

        # CONSIDER DELETING EMPTY ADJACENCY KEYS

        # Update self.vertex_dict
        if self.vertex_dict is not None:
            for v in self.adjList:
                if v not in self.vertex_dict:
                    self.vertex_dict[v] = None

    # CREATE SETTER AND GETTER FUNCTION FOR vertex_dict attribute
    # LET adjList keep track of vertex_dict instead! j

    @property
    def edges(self):
        return self.edge_dict

    @property 
    def vertices(self):
        return self.vertex_dict

    def edge_count(self):
        if self.edge_dict is not None:   
            return len(self.edge_dict)
        else:
            return 0

    def node_count(self):
        # adjlist can be zero here
        return max(len(self.adjList), len(self.vertex_dict))

    def get_vertices(self):
        return list(self.vertex_dict)

    def add_edge(self, edge_dict):
        """Add edges to our graph. Will silently replace edges if it already exists. 
        
        Arg:
            edge_dict (dict): i.e. {('v1', 'v2'): 5.0}
        
        """
        self.edge_dict.update(edge_dict)
        self._update_adj_list()

    def add_vertex(self, vertex_dict):
        """Vertex to our graph

        Arg:
            vertex_dict (dict): {'v1': 5}
        
        """
        self.vertex_dict.update(vertex_dict)
        # SHOULD WE ALSO UPDATE ADJ LIST TO CONTAIN NEW NODES?
   
    def remove_edges(self, edge_list):
        """Delete specific edges in our graph

        Arg:
            edge_list (iter of edges): 

        """
        for e in edge_list:
            
            # update adjacency list and edge dict
            if self.graph_type == "directed":
                # update adjacency list
                if e[1] in self.adjList[e[0]]:
                    self.adjList[e[0]].remove(e[1])
                
                # update edge_dict 
                # self.edge_dict.pop(e)  #slightly slower
                del self.edge_dict[e]   #raises KeyError if not there
            else:
                # update adjacency list in both directions
                if e[1] in self.adjList[e[0]]:
                    self.adjList[e[0]].remove(e[1])
                if e[0] in self.adjList[e[1]]:
                    self.adjList[e[1]].remove(e[0])
                
                # update edge dicts in both directions
                del self.edge_dict[e]
                del self.edge_dict[(e[1], e[0])]

    def remove_vertices(self, vertex_list):
        """Delete vertices from our graph

        Arg:
            vertex_list (iter of vertices):

        Todo:
            - delete edges associated with deleted vertex
        
        """
        for v in vertex_list:
            del self.vertex_dict[v]

    def neighbors(self, v):
        """Return a list of neighbors of v
        
        Todo:
            - just return adjList[v]!
        
        """
        # neighs = [n for n in self.adjList[v]]
        if v in self.adjList:
            neighs = self.adjList[v]
            return neighs
        else:
            return []
    
    def cost(self, *args, **kwargs):
        """Return cost of edge or vertex based on number of args

        Args:
            from_node, to_node (vertex, vertex): Key of vertices, contained in edgeDict
            node (vertex): Key of a single vertex, contained in vertexDict

        Kwargs:
            name (str): To determine the specific reference for multi-weighted edges of graphs

        """
        # unpack name if in kwargs
        try:
            # case 1) gets an edge weight. case 2) gets a vertex weight
            if len(args) == 2:
                from_node, to_node = args
                if "name" in kwargs:
                    name = kwargs["name"]

                    # if a list of names, then iterate through the list
                    if type(name)==list:
                        weight = self.edge_dict[(from_node, to_node)]
                        for n in name:
                            weight = weight[n]     
                    else:
                        weight = self.edge_dict[(from_node, to_node)][name]               
                    return weight
                weight = self.edge_dict[(from_node, to_node)]
                return weight
            elif len(args) == 1:
                node = args[0]
                if "name" in kwargs:
                    name = kwargs["name"]
                    
                    # if a list of names, then iterate through the list
                    if type(name)==list:
                        weight = self.vertex_dict[node]
                        for n in name:
                            weight = weight[n]     
                    else:
                        weight = self.vertex_dict[node][name]
                    return weight

                weight = self.vertex_dict[node]
                return weight
            else:
                print("vertex or edge not found using arguments: ", args)
                raise KeyError("vertex or edge not found using arguments: ")
        except Exception as E_:
            raise E_