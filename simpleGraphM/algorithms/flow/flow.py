import collections
import numpy as np

from simpleGraphM.algorithms.search import BreadthFirstSearch
from simpleGraphM.graph import GraphFactory

INF = np.inf

class Queue:
    """FIFO data structure """
    def __init__(self):
        # deque is a double ended queue. you can add or remove elements on the left or right
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()


class MaxFlow:
    """Solve a max flow problem (by default using edmonds-karp). Assumed all flow is initially zero.
    Instantiate this class and call run

    """
    def __init__(self, G, source=None, sink=None):
        # construct Gf, the residual graph.
        self.G = G
        self.Gf = GraphFactory.create_graph("Generic", edge_dict=G.edge_dict, vertex_dict=None, graph_type="undirected", deep_copy=True)
        self.source = source
        self.sink = sink  
        # Add flow to edges
        for e, val in self.G.edge_dict.items():
            val["flow"] = 0   

        # Variables defined at termination
        self.maxFlowVal = None
        self.minCutVal = 0
        self.minCutSet = {}
        self.reachSet = None

    def set_source(self, source):
        self.source = source

    def set_sink(self, sink):
        self.sink = sink

    def run(self, method="edmonds_karp"):
        mapping = {"edmonds_karp": self.__run_edmonds_karp,
                   "push_relabel": self.__run_pushrelabel

        }
        if method not in mapping:        
            raise ValueError("Please select a method from this list: {}".format(str(list(mapping))))
        mapping[method]()    

    ##############################
    ### PUSH RELABEL ALGORITHM ###
    ##############################  
    def __run_pushrelabel(self):   
        # Create a queue of active or overflowing nodes for O(V^3) implementation
        excessQ = Queue()

        # initialize the algorithm        
        # Add excess and height to vertices
        for v, val in self.G.vertex_dict.items():
            if val is None:
                self.G.vertex_dict[v] = {}
                val = self.G.vertex_dict[v]    
            val["excess"] = 0
            val["height"] = 0
        # Set source height
        self.G.vertex_dict[self.source]["height"] = self.G.node_count()
        # Set flows out of source to be at-capacity, the excess at the downstream to be at-capacity
        for v in self.G.neighbors(self.source):
            self.G.edge_dict[(self.source,v)]["flow"] = self.G.edge_dict[(self.source,v)]["cap"]
            self.G.vertex_dict[v]["excess"] = self.G.edge_dict[(self.source,v)]["cap"]
            self.G.vertex_dict[self.source]["excess"]-=self.G.edge_dict[(self.source,v)]["cap"]

            excessQ.put(v)
        
        while not excessQ.empty():
            # Get active node
            u = excessQ.get()
            # choose to relabel or push
            relabel_cases = []
            push_cases = []
            for v in self.Gf.neighbors(u):
                if v != self.source and v != self.sink:                
                    if self.__residual_cap(u,v)>0 and self.G.vertex_dict[u]["height"] <= self.G.vertex_dict[v]["height"]:
                        relabel_cases.append(True)
                    else:
                        relabel_cases.append(False)

                if self.__residual_cap(u,v)>0 and self.G.vertex_dict[u]["height"] == self.G.vertex_dict[v]["height"] + 1:
                    push_cases.append(v)

                if self.G.vertex_dict[v]["excess"]>0:
                    excessQ.put(v)

            if all(relabel_cases):
                self.__relabel(u)
                if self.G.vertex_dict[u]["excess"]>0:
                    excessQ.put(u)    

            if push_cases:
                # for v in push_cases:
                v = push_cases[0]
                self.__push(u, v)


                    
        pass

    def __push(self,u, v):
        """Because u is overflowing, push some flow from u to v 

        """
        # amount of flow to push
        del_f = min(self.G.vertex_dict[u]["excess"], self.__residual_cap(u,v))
        if (u,v) in self.G.edge_dict:
            self.G.edge_dict[(u,v)]['flow'] += del_f
        else:
            self.G.edge_dict[(v,u)]["flow"]-= del_f
        #update excess
        self.G.vertex_dict[u]["excess"]-= del_f
        self.G.vertex_dict[v]["excess"]+= del_f

    def __relabel(self, u):
        """Relabel the overflowing node u s.t. for all outgoing edges with non-zero residual capacity, +1 to min height
        
        """
        min_h = None
        for v in self.Gf.neighbors(u):
            if self.__residual_cap(u,v) > 0 and v != self.source and v != self.sink:
                if min_h is None or self.G.vertex_dict[v]["height"] < min_h:
                    min_h = self.G.vertex_dict[v]["height"]
        if min_h is not None: 
            self.G.vertex_dict[u]["height"] = 1 + min_h

    ##############################
    ### EDMONDS-KARP ALGORITHM ###
    ##############################
    def __run_edmonds_karp(self):
        '''Implementation of Ford-Fulkerson's Algorithm via Edmonds-Karp, requring
            a shortest augmenting path each iteration

        '''
        # search for first augmenting path in gf
        isPath, path = self.__augmenting_path()
        while isPath:
            # compute residual capacity
            min_cf = None
            for e in zip(path, path[1:]):
                if min_cf is None or self.__residual_cap(e[0], e[1]) < min_cf:
                    min_cf = self.__residual_cap(e[0], e[1])
            # increment the flow in graph G
            for e in zip(path, path[1:]):
                if e in self.G.edge_dict:
                    self.G.edge_dict[e]['flow'] += min_cf
                else:
                    self.G.edge_dict[e[1], e[0]]['flow'] -= min_cf 
            
            # Find another augmenting path
            isPath, path = self.__augmenting_path()

            # debug
            # for e in zip(path, path[1:]):
            #     print(self.residual_cap(e[0], e[1])) 

        # Report the good news
        pass

    def residual_cap(self,u,v):
        if (u,v) in self.G.edge_dict:
            return self.G.edge_dict[(u,v)]['cap'] - self.G.edge_dict[(u,v)]['flow']
        elif (v,u) in self.G.edge_dict:
            return self.G.edge_dict[(v,u)]['flow']
        else:
            return 0

    def __residual_cap(self,u,v):
        if (u,v) in self.G.edge_dict:
            return self.G.edge_dict[(u,v)]['cap'] - self.G.edge_dict[(u,v)]['flow']
        elif (v,u) in self.G.edge_dict:
            return self.G.edge_dict[(v,u)]['flow']
        else:
            return 0

    def __skip_condition(self, u,v):
        # Skip edge in bfs if residual is zero
        if self.__residual_cap(u,v) > 0:
            return False
        else:
            return True

    def __augmenting_path(self):
        if self.source == None or self.sink == None:
            raise ValueError("source and/or sink is 'None'. They must be defined!")
        bfs = BreadthFirstSearch(self.Gf, start=self.source, goal=self.sink)
        # Rebind skip condition in bfs
        bfs.skip_case = self.__skip_condition
        bfs.run()

        if self.sink in bfs.g:
            # reconstruct shortest path from s-t (assumed edge weight=1)
            current = self.sink
            path = [current]
            while current is not None:
                current = bfs.parent[current]
                if current is not None:
                    path.append(current)
            # reverse direction
            path.reverse()
            return True, path 
        else:
            # Terminate if no augmenting path exists and store answers
            self.reachSet = bfs.g
            for v in self.reachSet:
                for w in self.G.neighbors(v):
                    if w not in self.reachSet:
                        self.minCutSet.update({(v,w): self.G.cost(v, w, name='flow')})
                        self.minCutVal += self.G.cost(v, w, name='flow')
            self.maxFlowVal = sum(self.G.cost(self.source, v, name='flow') for v in self.G.neighbors(self.source))
            return False, None

        pass
