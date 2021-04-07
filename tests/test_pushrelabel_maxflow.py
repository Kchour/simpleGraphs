import unittest

from simpleGraphM.graph import GraphFactory
from simpleGraphM.algorithms.flow import MaxFlow, INF

class TestFlow(unittest.TestCase):

    def test_max_flow_with_push_relabel_simple_1(self):
        edgeDict = {('s','1'): {"cap": 3},
                    ('s','2'): {"cap": 2},
                    ('1','2'): {"cap": 5},
                    ('1','t'): {"cap": 2},
                    ('2','t'): {"cap": 3},
                    }

        myGraph = GraphFactory.create_graph("Generic", edge_dict=edgeDict, vertex_dict=None, graph_type="directed", deep_copy=False)

        # Test undefined sink, source error
        mf = MaxFlow(myGraph)
        self.assertRaises(ValueError, mf.run)

        # either is valid
        mf = MaxFlow(myGraph, source = 's', sink='t')

        mf = MaxFlow(myGraph)
        mf.set_source('s')
        mf.set_sink('t')

        # execute push_relabel
        mf.run("push_relabel")

        # test solution
        self.assertEqual(myGraph.edge_dict[('s','1')]['flow'], 3)
        self.assertEqual(myGraph.edge_dict[('s','2')]['flow'], 2)
        self.assertEqual(myGraph.edge_dict[('1','2')]['flow'], 1)
        self.assertEqual(myGraph.edge_dict[('1','t')]['flow'], 2)
        self.assertEqual(myGraph.edge_dict[('2','t')]['flow'], 3)

        # Test min-cut and max-flow values
        self.assertEqual(mf.maxFlowVal, mf.minCutVal)

    def test_max_flow_with_push_relabel_simple_2(self):
        # Define some edges       
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

        myGraph = GraphFactory.create_graph("Generic", edge_dict=edgeDict, vertex_dict=None, graph_type="directed", deep_copy=False)

        # Test undefined sink, source error
        mf = MaxFlow(myGraph)
        self.assertRaises(ValueError, mf.run)

        # either is valid
        mf = MaxFlow(myGraph, source=0, sink=5)

        # or this
        mf = MaxFlow(myGraph)
        mf.set_source(0)
        mf.set_sink(5)

        # execute
        mf.run("push_relabel")
        
        # Test max flow value
        self.assertEqual(myGraph.edge_dict[(0,1)]['flow']+myGraph.edge_dict[(0,2)]['flow'], 23)

        # Test min-cut and max-flow values
        self.assertEqual(mf.maxFlowVal, mf.minCutVal)
    
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