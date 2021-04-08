from optparse import OptionParser
import inspect

from simpleGraphM.graph import GraphFactory
from simpleGraphM.algorithms.flow import INF, MaxFlow

class MaxFlowGraphs:

    # def anti_parallel_edges(cls):
    #     # Problem 1: complex example from william cook
    #     edgeDict = {(0, 1): {"cap": 16},
    #                 (0, 2): {"cap": 13},
    #                 (1, 2): {"cap": 10},
    #                 (1, 3): {"cap": 12},
    #                 (2, 1): {"cap": 4},
    #                 (2, 3): {"cap": 5},
    #                 (2, 4): {"cap": 14},
    #                 (3, 2): {"cap": 9},
    #                 (3, 4): {"cap": 5},
    #                 (3, 5): {"cap": 25},
    #                 (4, 3): {"cap": 7},
    #                 (4, 5): {"cap": 4},
    #                 }
    #     source = 0
    #     sink = 5
    #     maxFlowSol = 23
    #     return edgeDict, maxFlowSol
    def network_flow_cook_1(self):
        # Define some edges
        edgeDict = {('r','p'): {"cap": 6},
                    ('r','a'): {"cap": 9},
                    ('r','q'): {"cap": 4},
                    ('p','b'): {"cap": 3},
                    ('p','q'): {"cap": 2},
                    ('q','p'): {"cap": 1},
                    ('q','b'): {"cap": 2},
                    ('q','d'): {"cap": 6},
                    ('b','a'): {"cap": 1},
                    ('b','s'): {"cap": 8},
                    ('a','c'): {"cap": 8},
                    ('a','d'): {"cap": 1},
                    ('c','q'): {"cap": 1},
                    ('c','b'): {"cap": 2},
                    ('c','s'): {"cap": 4},
                    ('d','c'): {"cap": 1},
                    ('d','s'): {"cap": 6},
                    }
        source = 'r'
        sink = 's'
        maxFlowSol = None
        data = {"source": source, "sink": sink, "sol": maxFlowSol}
        return edgeDict, data

    def network_flow_simple_1(self):
        edgeDict = {('s','1'): {"cap": 3},
                ('s','2'): {"cap": 2},
                ('1','2'): {"cap": 5},
                ('1','t'): {"cap": 2},
                ('2','t'): {"cap": 3},
                }

        source = 's'
        sink = 't'
        maxFlowSol = 5
        data = {"source": source, "sink": sink, "sol": maxFlowSol}
        return edgeDict, data

    def network_flow_simple_2(self):
        edgeDict = {(0, 1): {"cap": 16},
            (0, 2): {"cap": 13},
            (1, 2): {"cap": 10},
            (1, 3): {"cap": 12},
            (2, 1): {"cap": 4},
            (2, 4): {"cap": 14},
            (3, 2): {"cap": 9},
            (3, 5): {"cap": 20},
            (4, 3): {"cap": 7},
            (4, 5): {"cap": 4},
            }

        source = 0
        sink = 5
        maxFlowSol = 5
        data = {"source": source, "sink": sink, "sol": maxFlowSol}
        return edgeDict, data

    def network_flow_simple_3(self):
        edgeDict = {('S', 'A'): {"cap": 4},
                    ('S', 'B'): {"cap": 2},
                    ('A', 'C'): {"cap": 3},
                    ('B', 'C'): {"cap": 2},
                    ('B', 'D'): {"cap": 3},
                    ('C', 'B'): {"cap": 1},
                    ('C', 'T'): {"cap": 2},
                    ('D', 'T'): {"cap": 4},
                    }

        source = 'S'
        sink = 'T'
        maxFlowSol = 5
        data = {"source": source, "sink": sink, "sol": maxFlowSol}
        return edgeDict, data

    def network_flow_simple_4(self):
        edgeDict = {('A', 'B'): {"cap": 3},
            ('A', 'D'): {"cap": 3},
            ('B', 'C'): {"cap": 4},
            ('C', 'A'): {"cap": 3},
            ('C', 'D'): {"cap": 1},
            ('C', 'E'): {"cap": 2},
            ('D', 'E'): {"cap": 2},
            ('D', 'F'): {"cap": 6},
            ('E', 'B'): {"cap": 1},
            ('E', 'G'): {"cap": 1},
            ('F', 'G'): {"cap": 9},
            }
        source = 'A'
        sink = 'G'
        maxFlowSol = 5
        data = {"source": source, "sink": sink, "sol": maxFlowSol}
        return edgeDict, data

    def network_flow_simple_inf_1(self):
        edgeDict = {('r', 'a'): {"cap": 2},
            ('r', 'b'): {"cap": 4},
            ('r', 'c'): {"cap": 3},
            ('r', 'd'): {"cap": 2},
            ('e', 's'): {"cap": 7},
            ('f', 's'): {"cap": 1},
            ('g', 's'): {"cap": 3},
            ('h', 's'): {"cap": 1},
            ('a', 'e'): {"cap": INF},
            ('b', 'a'): {"cap": INF},
            ('b', 'c'): {"cap": INF},
            ('c', 'd'): {"cap": INF},
            ('c', 'f'): {"cap": INF},
            ('f', 'g'): {"cap": INF},
            ('d', 'g'): {"cap": INF},
            ('h', 'd'): {"cap": INF},
            }
        source = 'r'
        sink = 's'
        maxFlowSol = None
        data = {"source": source, "sink": sink, "sol": maxFlowSol}
        return edgeDict, data

class MaxFlowGraphsTests:
    @staticmethod
    def return_alg_sol(algorithm: str):
        # MyClass = MaxFlowGraphs
        # method_list = [attribute for attribute in dir(MyClass) if callable(getattr(MyClass, attribute)) and attribute.startswith('__') is False]
        method_list = inspect.getmembers(MaxFlowGraphs, predicate=inspect.isfunction)

        mfg = MaxFlowGraphs()

        sol = []
        for func in method_list:
            try:
                edgeDict, data = func[1](mfg)
                myGraph = GraphFactory.create_graph("Generic", edge_dict=edgeDict, vertex_dict=None, graph_type="directed", deep_copy=False)
                mf = MaxFlow(myGraph, source=data['source'], sink=data['sink'])
                mf.run(algorithm)
                sol.append([mf.maxFlowVal, mf.minCutVal])
            except Exception as e:
                e.message="Failed at: "+ func[0]
                raise

        return sol