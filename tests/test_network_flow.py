import unittest

from simpleGraphM.graph import GraphFactory
from simpleGraphM.algorithms.flow import MaxFlow

class TestFlow(unittest.TestCase):

    # def test_max_flow_with_fordfulkerson_edkarp_complex(self):
    #     # Define some edges
    #     edgeDict = {('r','p'): {"cap": 6},
    #                 ('r','a'): {"cap": 1},
    #                 ('r','q'): {"cap": 4},
    #                 ('p','b'): {"cap": 3},
    #                 ('p','q'): {"cap": 2},
    #                 ('q','p'): {"cap": 1},
    #                 ('q','b'): {"cap": 2},
    #                 ('q','d'): {"cap": 6},
    #                 ('b','a'): {"cap": 1},
    #                 ('b','s'): {"cap": 8},
    #                 ('a','c'): {"cap": 8},
    #                 ('a','d'): {"cap": 1},
    #                 ('c','q'): {"cap": 1},
    #                 ('c','b'): {"cap": 2},
    #                 ('c','s'): {"cap": 4},
    #                 ('d','c'): {"cap": 1},
    #                 ('d','s'): {"cap": 6},
    #                 }

    #     myGraph = GraphFactory.create_graph("Generic", edge_dict=edgeDict, vertex_dict=None, graph_type="directed", deep_copy=False)

    #     mf = MaxFlow(myGraph)

    # def test_max_flow_with_fordfulkerson_edkarp_simple_poor(self):

    #     #             +---------+             
    #     #      +------>         |-------+     
    #     #    3 |      |    1    |       |2    
    #     #      |      +---------+       |     
    #     # +---------+      |       +----v----+
    #     # |         |      |       |         |
    #     # |   s     |    5 |       |    t    |
    #     # +---------+      |       +----^----+
    #     #      |      +----v----+       |     
    #     #    2 |      |         |       |3    
    #     #      +------>    2    |-------+     
    #     #             +---------+   
    #     # 
    #     #   Define some edges         
    #     edgeDict = {('s','1'): {"cap": 3},
    #                 ('s','2'): {"cap": 2},
    #                 ('1','2'): {"cap": 5},
    #                 ('1','t'): {"cap": 2},
    #                 ('2','t'): {"cap": 3},
    #                 }

    #     myGraph = GraphFactory.create_graph("Generic", edge_dict=edgeDict, vertex_dict=None, graph_type="directed", deep_copy=False)

    #     # Test undefined sink, source error
    #     mf = MaxFlow(myGraph)
    #     self.assertRaises(ValueError, mf.run)

    #     # either is valid
    #     mf = MaxFlow(myGraph, source = 's', sink='t')

    #     mf = MaxFlow(myGraph)
    #     mf.set_source('s')
    #     mf.set_sink('t')

    #     mf.run()

    #     # test solution
    #     self.assertEquals(myGraph.edge_dict[('s','1')]['flow'], 3)
    #     self.assertEquals(myGraph.edge_dict[('s','2')]['flow'], 2)
    #     self.assertEquals(myGraph.edge_dict[('1','2')]['flow'], 1)
    #     self.assertEquals(myGraph.edge_dict[('1','t')]['flow'], 2)
    #     self.assertEquals(myGraph.edge_dict[('2','t')]['flow'], 3)

    def test_max_flow_with_fordfulkerson_edkarp_simple_better(self):
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
        pass
        


if __name__ == "__main__":
    unittest.main()