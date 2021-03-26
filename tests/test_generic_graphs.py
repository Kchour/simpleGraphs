import unittest

from simpleGraphM.graph import GraphFactory

class TestGenericGraph(unittest.TestCase):

    # test GraphFactory in creating a Generic MyGraph object
    def test_create_generic(self):

        # Define some edges
        edgeDict = {('v1','v2'): 1,
                    ('v2','v3'): 1,
                    ('v3','v4'): 1,
                    ('v4','v5'): 1,
                    ('v5','v6'): 1,
                    ('v6','v7'): 1,
                    ('v7','v8'): 1,
                    ('v8','v5'): 1}

        vertexDict = {
                    'v1': 1,
                    'v2': 2,
                    'v3': 3,
                    'v4': 4,
                    'v5': 5,
                    'v6': 6
                }
        
        # Create a generic graph using factory method
        genG = GraphFactory.create_graph("Generic", edge_dict = edgeDict, vertex_dict=vertexDict, graph_type = "undirected", deep_copy=True)

        # test to see if genG is an instance of "GenericGraph"
        self.assertTrue("GenericGraph" in str(type(genG)))

        # test accessing edges 
        ew = genG.cost('v1', 'v2')
        self.assertEqual(ew, 1)

        # test accesing vertices
        vw = genG.cost('v6')
        self.assertEqual(vw, 6)

        # Test removal of edges. Should return a KeyError
        genG.remove_edges([('v1','v2')])
        self.assertRaises(genG.cost('v1', 'v2'))

        # Test removal of vertices. Should return a KeyError
        genG.remove_vertices(['v6'])
        self.assertRaises(genG.cost('v6'))

        # TODO return some neighbors and stuff

    # test adding attributes to a generic graph (multiiple edge or vertex weights)
    def test_generic_graph_attributes(self):
        pass
    
if __name__ == "__main__":
    unittest.main()