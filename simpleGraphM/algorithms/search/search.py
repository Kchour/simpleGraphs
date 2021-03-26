"""Iterative search algorithms with Astar, DepthFirstSearch, and Dijkstra 

Example:

    # Create search object
    graph = GraphFactory(...)
    asearch = AStarSearch(graph, start, goal, h_type, visualize=False)
    
    # Query the search object
    parentList, optimalCosts = asearch.use_algorithm()

    # Run one iteration of search
    parentList, optimalCosts, frontierList, currentNode = asearch.iterate_algorithm()

Todo:
    - Consider combining this class with generic search?
    - Dijkstra class not fully implemented
    - More documentation later

"""

import numpy as np
import time

from .search_utils import PriorityQueueHeap
from .search_utils import Queue

class Search:
    
    total_expanded_nodes = 0

    def __init__(self, graph, start, goal):
        self.graph = graph
        self.start = start
        self.goal = goal
        
        # Open set or frontier must be defined properly 
        self.frontier = None
        
        # closed list with cost-so-far
        self.g = {}

        # A linked list giving predecessor nodes
        self.parent = {}

    def set_start(self, start):
        self.start = start

    def set_goal(self, goal):
        self.goal = goal

    def run(self):
        pass

class BreadthFirstSearch(Search):

    def __init__(self, graph, start=None, goal=None):
        Search.__init__(self, graph, start, goal)
        
        # init frontier
        self.frontier = Queue()
        self.frontier.put(self.start)

        # init the rest
        self.parent[self.start] = None
        self.g[self.start] = 0

    def skip_case(self, u, v):
        return False

    def run(self):
        while not self.frontier.empty():
            # deque the frontier
            current = self.frontier.get()

            if current == self.goal:
                break

            for next in self.graph.neighbors(current):
                # Skip condition for special cases
                if self.skip_case(current, next):
                    continue
                
                # Rest of the bfs algorithm
                g_next = self.g[current] + 1
                if next not in self.g or g_next < self.g[next]:
                    self.frontier.put(next)
                    self.g[next] = g_next
                    self.parent[next] = current

class BestFirstSearch(Search):
    """Standard A-Star or Dijkstra search on any generic graph, though heuristics are only defined for grid-based graphs atm"""
    def __init__(self, graph, start, goal=None, heuristic_type='zero', depth_limit=None, visualize=False):
        Search.__init__(self, graph, start, goal)
        self.heuristic_type = heuristic_type
        self.visualize = visualize

        # A star initialize openList, closedList
        self.frontier = PriorityQueueHeap()
        self.frontier.put(self.start, 0)      # PUT START IN THE OPENLIST
        self.parent = {}              # parent, {loc: parent}

        # g function dict, {loc: f(loc)}, CLOSED LIST BASICALLY
        self.g = {}
        self.parent[self.start] = None
        self.g[self.start] = 0

        #depth limit
        self.depth_limit = depth_limit
        self.boundary_nodes = set()

    def heuristic(self, a, b, type_='manhattan'):
        """ Grid based heuristics """
        (x1, y1) = a
        (x2, y2) = b
        if type_ == 'manhattan':
            return abs(x1 - x2) + abs(y1 - y2)
        elif type_ == 'euclidean':
            v = [x2 - x1, y2 - y1]
            return np.hypot(v[0], v[1])
        elif type_ == 'diagonal_uniform':
            # Chebyshev Distance
            return max(abs(x1 - x2), abs(y1 - y2))
        elif type_ == 'diagonal_nonuniform':
            dmax = max(abs(x1 - x2), abs(y1 - y2))
            dmin = min(abs(x1 - x2), abs(y1 - y2))
            return 1.414*dmin + (dmax - dmin)
    
    def deepen(self, new_depth_limit):
        """Allow continued search from the last stop, starting off with boundary nodes 
            as the frontier

        """
        for v in self.boundary_nodes:
            self.frontier.put(v, self.g[v])

        self.depth_limit = new_depth_limit

    def run(self):
        """ Usage:
            - call to runs full algorithm until termination

            Returns:
            - a linked list, 'parent'
            - hash table of nodes and their associated min cost, 'g'
        """
        
        frontier = self.frontier
        parent = self.parent
        g = self.g

        while not frontier.empty():
            _, current = frontier.get()  # update current to be the item with best priority

            if self.visualize:
                AnimateV2.add("current", current[0], current[1], markersize=10, marker='o')

            # early exit if we reached our goal
            if current == self.goal: 
                break

            # expand current node and check neighbors
            for next in self.graph.neighbors(current):
                g_next = g[current] + self.graph.cost(current, next)
                # if next location not in CLOSED LIST or its cost is less than before
                # Newer implementation
                if next not in g or g_next < g[next]:
                    if self.heuristic_type == 'zero' or self.heuristic_type == None or self.goal == None:
                        priority = g_next 
                    else:
                        priority = g_next + self.heuristic(self.goal, next, self.heuristic_type)
                    
                    if self.depth_limit is not None: 
                        if priority <= self.depth_limit:
                            g[next] = g_next
                            frontier.put(next, priority)
                            parent[next] = current
                        else:
                            self.boundary_nodes.add(current)
                    else:
                        g[next] = g_next    
                        frontier.put(next, priority)
                        parent[next] = current

            if self.visualize:
                # self.animateNeighbors.update(next)
                if np.fmod(self.total_expanded_nodes, 100000)==0 or self.total_expanded_nodes == 0:
                #     data = [k[2] for k in self.frontier.elements]
                #     AnimateV2.add("frontier", np.array(data).T.tolist(), markersize=10, marker='D', draw_clean=True)
                    AnimateV2.update()

        return parent, g



