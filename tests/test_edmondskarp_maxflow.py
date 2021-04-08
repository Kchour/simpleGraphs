import unittest

from simpleGraphM.graph import GraphFactory
from simpleGraphM.algorithms.flow import MaxFlow, INF

class TestFlow(unittest.TestCase):

    def test_max_flow_with_fordfulkerson_edkarp_complex(self):
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

        myGraph = GraphFactory.create_graph("Generic", edge_dict=edgeDict, vertex_dict=None, graph_type="directed", deep_copy=False)

        # either is valid
        mf = MaxFlow(myGraph, source = 's', sink='t')

        mf = MaxFlow(myGraph)
        mf.set_source('r')
        mf.set_sink('s')

        mf.run()
        
        # Test min-cut and max-flow values
        self.assertEqual(mf.maxFlowVal, mf.minCutVal)
        

    def test_max_flow_with_fordfulkerson_edkarp_simple_1(self):

        #             +---------+             
        #      +------>         |-------+     
        #    3 |      |    1    |       |2    
        #      |      +---------+       |     
        # +---------+      |       +----v----+
        # |         |      |       |         |
        # |   s     |    5 |       |    t    |
        # +---------+      |       +----^----+
        #      |      +----v----+       |     
        #    2 |      |         |       |3    
        #      +------>    2    |-------+     
        #             +---------+   
        # 
        #   Define some edges         
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

        mf.run()

        # test solution
        self.assertEqual(myGraph.edge_dict[('s','1')]['flow'], 3)
        self.assertEqual(myGraph.edge_dict[('s','2')]['flow'], 2)
        self.assertEqual(myGraph.edge_dict[('1','2')]['flow'], 1)
        self.assertEqual(myGraph.edge_dict[('1','t')]['flow'], 2)
        self.assertEqual(myGraph.edge_dict[('2','t')]['flow'], 3)

        # Test min-cut and max-flow values
        self.assertEqual(mf.maxFlowVal, mf.minCutVal)

    def test_max_flow_with_fordfulkerson_edkarp_simple_2(self):
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
        mf.run()
        
        # Test max flow value
        self.assertEqual(myGraph.edge_dict[(0,1)]['flow']+myGraph.edge_dict[(0,2)]['flow'], 23)

        # Test min-cut and max-flow values
        self.assertEqual(mf.maxFlowVal, mf.minCutVal)

    def test_max_flow_with_fordfulkerson_edkarp_simple_3(self):
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

        # execute
        mf.run()

        # Test max flow value
        self.assertEqual(myGraph.edge_dict[('S','A')]['flow']+myGraph.edge_dict[('S','B')]['flow'], 5)

        # Test min-cut and max-flow values
        self.assertEqual(mf.maxFlowVal, mf.minCutVal)

    # This test relies on reverse edges
    def test_max_flow_with_fordfulkerson_edkarp_simple_4(self):
        # Define some edges       
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

        myGraph = GraphFactory.create_graph("Generic", edge_dict=edgeDict, vertex_dict=None, graph_type="directed", deep_copy=False)

        # Test undefined sink, source error
        mf = MaxFlow(myGraph)
        self.assertRaises(ValueError, mf.run)

        # either is valid
        # mf = MaxFlow(myGraph, source='A', sink='G')

        # or this
        mf = MaxFlow(myGraph)
        mf.set_source('A')
        mf.set_sink('G')

        # execute
        mf.run()

        # Test max flow value
        self.assertEqual(myGraph.edge_dict[('A','B')]['flow']+myGraph.edge_dict[('A','D')]['flow'], 5)

        # Test min-cut and max-flow values
        self.assertEqual(mf.maxFlowVal, mf.minCutVal)

    def test_max_flow_with_fordfulkerson_edkarp_infinity_1(self):
        # Define some edges       
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

        myGraph = GraphFactory.create_graph("Generic", edge_dict=edgeDict, vertex_dict=None, graph_type="directed", deep_copy=False)

        mf = MaxFlow(myGraph)
        self.assertRaises(ValueError, mf.run)

        # Create mf object and set source + sink
        mf = MaxFlow(myGraph)
        mf.set_source('r')
        mf.set_sink('s')

        # execute
        mf.run()

        # Test min-cut and max-flow values
        self.assertEqual(mf.maxFlowVal, mf.minCutVal)

if __name__ == "__main__":
    unittest.main()