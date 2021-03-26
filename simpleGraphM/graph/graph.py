""" Custom graph class structures

classes:

    :GraphFactory: Primarily used to create graphs. Serves as the client interface

    :IGraph: The interface class responsible for actually created graph objects

    :SquareGrid: A 2D grid-based graph 
        
        :neighbors(v): given tuple (x,y), returns neighbors
        :cost(v1, v2): given two tuples (v1, v2), returns cost of edge

    :MyGraph: User can define a generic graph, by giving a edge list
        
        :neighbors(v): similar to above, but v is generic here
        :cost(v1,v2): similar to above, but v1,v2 is generic

Todo:
    - Create a 3D graph class
    
"""

from abc import ABC, abstractmethod

class Graph(ABC):
    """An abstract class which should be subclassed with methods defined concretely
       
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def neighbors(self, v):
        pass

    @abstractmethod
    def cost(self):
        pass


    
