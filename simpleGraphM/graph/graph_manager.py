from .graph import Graph
from .square_grid import OccupancySquareGrid, SquareGrid
from .generic_graph import GenericGraph

class GraphFactory:
    """ A factory class used to create graph objects
    
    Create a square grid

    Example:
        minX = -15			# [m]
        maxX = 15           
        minY = -15
        maxY = 15
        grid = None         # pre-existing 2d numpy array?
        grid_size = 1       # grid fineness[m]
        grid_dim = [minX, maxX, minY, maxY]
        n_type = 8           # neighbor type

        # Create a squareGrid using GraphFactory
        sq = GraphFactory.create_graph("SquareGrid", grid=grid, grid_dim=grid_dim, grid_size=grid_size, n_type= n_type)      

    Create generic graph

    Example:
        # Define some edges
        edgeDict = {('v1','v2'): 1,
                    ('v2','v3'): 1,
                    ('v3','v4'): 1,
                    ('v4','v5'): 1,
                    ('v5','v6'): 1,
                    ('v6','v7'): 1,
                    ('v7','v8'): 1,
                    ('v8','v5'): 1}
        
        # Create a generic graph using factory method
        genG = GraphFactory.create_graph("Generic", edge_dict = edgeDict, graph_type = "undirected", visualize=False)

    """
    @staticmethod
    def create_graph(type_: str, **kwargs ) -> Graph:
        try:
            if type_ is "OccupancySquareGrid":
                # GraphManager.add_layer(OccupancySquareGrid(**kwargs), name)
                return OccupancySquareGrid(**kwargs)
            elif type_ is "Generic":
                # GraphManager.add_layer(GenericGraph(**kwargs), name)
                return GenericGraph(**kwargs)
            elif type_ is "SquareGrid":
                # GraphManager.add_layer(SquareGraph(**kwargs), name)
                return SquareGrid(**kwargs)
            else:
                raise AssertionError("Graph type not defined")
            # return GraphManager.get_layer(name)
        except AssertionError as _e:
            print(_e)
            raise

class GraphManager:
    """Singleton Metaclass to keep track of all graph instances.
        Will overwrite existing layers!
    
    """
    layers = {}

    @classmethod
    def add_layer(cls, graph, name=""):
        assert not name in cls.layers, '"{}" ALREADY EXISTS'.format(name)
        cls.layers[name] = graph

    @classmethod
    def update_layer(cls, graph, name):
        assert name in cls.layers, '"{}" NOT FOUND,  ADD IT FIRST via add_layer(graph, name)'.format(name)
        cls.layers[name] = graph

    @classmethod
    def delete_layer(cls, name):
        del cls.layers[name]
        print('Deleted "{}"'.format(name))

    @classmethod
    def get_layer(cls, name):
        return cls.layers[name]

import numpy as np
class CostMapManager: 
    """Cost map class assuming maps are representing as 2D numpy arrays """
    def __init__(self):    
        self.layers= {}

    def add_layer(self, grid=None, name=""):
        assert  not name in self.layers, '"{}"  ALREADY EXISTS'.format(name)
        self.layers[name] = grid
    
    # THIS FUCNTION MAY BE USELESS
    def update_layer(self, grid, name):
        assert name in self.layers, '"{}" NOT FOUND, ADD IT FIRST'.format(name)
        self.layers[name] = grid 

    def does_layer_exist(self, name):
        ''' helper function to only add layer once 
            name := a tuple or list of names ('name1', name2')
        '''
        if not isinstance(name,list) and not isinstance(name, tuple):
            name = [name]
        #return name in self.layers
        return  all(n in self.layers for n in name)

    def return_total_map(self):  
        # Convert self.layers to a 3d array
        array_3d = np.dstack(list(self.layers.values()))
        return np.sum(array_3d, axis=2)

    def delete_layer(self, name):
        del self.layers[name]
        print('Deleted "{}"'.format(name))