from simpleGraphM.algorithms.search import BreadthFirstSearch
from simpleGraphM.graph import GraphFactory
import numpy as np

INF = np.inf

class MaxFlow:
    '''Implementation of Ford-Fulkerson's Algorithm via Edmonds-Karp, requring
        a shortest augmenting path each iteration

    '''
    def __init__(self, G, source=None, sink=None):
        # construct Gf, the residual graph.
        self.G = G
        self.Gf = GraphFactory.create_graph("Generic", edge_dict=G.edge_dict, vertex_dict=None, graph_type="undirected", deep_copy=True)
        self.source = source
        self.sink = sink
        for e, val in G.edge_dict.items():
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

    def run(self):
        # search for first augmenting path in gf
        isPath, path = self.augmenting_path()
        while isPath:
            # compute residual capacity
            min_cf = None
            for e in zip(path, path[1:]):
                if min_cf is None or self.residual_cap(e[0], e[1]) < min_cf:
                    min_cf = self.residual_cap(e[0], e[1])
            # increment the flow in graph G
            for e in zip(path, path[1:]):
                if e in self.G.edge_dict:
                    self.G.edge_dict[e]['flow'] += min_cf
                else:
                    self.G.edge_dict[e[1], e[0]]['flow'] -= min_cf 
            
            # Find another augmenting path
            isPath, path = self.augmenting_path()

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

    def skip_condition(self, u,v):
        # Skip edge in bfs if residual is zero
        if self.residual_cap(u,v) > 0:
            return False
        else:
            return True

    def augmenting_path(self):
        if self.source == None or self.sink == None:
            raise ValueError("source and/or sink is 'None'. They must be defined!")
        bfs = BreadthFirstSearch(self.Gf, start=self.source, goal=self.sink)
        # Rebind skip condition in bfs
        bfs.skip_case = self.skip_condition
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
            self.reachSet = bfs.g
            for v in self.reachSet:
                for w in self.G.neighbors(v):
                    if w not in self.reachSet:
                        self.minCutSet.update({(v,w): self.G.cost(v, w, name='flow')})
                        self.minCutVal += self.G.cost(v, w, name='flow')
            self.maxFlowVal = sum(self.G.cost(self.source, v, name='flow') for v in self.G.neighbors(self.source))
            return False, None

        pass