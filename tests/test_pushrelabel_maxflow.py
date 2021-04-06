import unittest

from simpleGraphM.graph import GraphFactory
from simpleGraphM.algorithms.flow import MaxFlow, INF

class TestFlow(unittest.TestCase):
    
    def test_max_flow_with_push_relabel_simple_3(self):
        # Define some edges
       
        edgeDict = {('S', 'A'): {"cap": 4},
                    ('S', 'B'): {"cap": 2},
                    ('A', 'C'): {"cap": 3},
                    ('B', 'C'): {"cap": 2},
                    ('B', 'D'): {"cap": 3},
                    ('C', 'B'): {"cap": 1},
                    ('C', 'T'): {"cap": 2},
                    ('D', 'T'): {"cap": 4},
                    }

        myGraph = GraphFactory.create_graph("Generic", edge_dict=edgeDict, vertex_dict=None, graph_type="directed", deep_copy=False)

        # Test undefined sink, source error
        mf = MaxFlow(myGraph)
        self.assertRaises(ValueError, mf.run)

        # either is valid
        # mf = MaxFlow(myGraph, source='S', sink='T')

        # or this
        mf = MaxFlow(myGraph)
        mf.set_source('S')
        mf.set_sink('T')

        # execute push_relabel
        mf.run("push_relabel")

        # Test max flow value
        self.assertEqual(myGraph.edge_dict[('S','A')]['flow']+myGraph.edge_dict[('S','B')]['flow'], 5)

        # Test min-cut and max-flow values
        self.assertEqual(mf.maxFlowVal, mf.minCutVal)

if __name__ == "__main__":
    unittest.main()