import unittest

from simpleGraphM.graph import GraphFactory

class TestGenericGraph(unittest.TestCase):

    # test GraphFactory in creating a Generic MyGraph object
    def test_create_generic_undirected(self):

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
                    'v9': 1,
                    'v10': 2,
                    'v11': 3,
                    'v12': 4,
                    'v13': 5,
                    'v14': 6
                }
        
        # Create a generic graph using factory method
        genG = GraphFactory.create_graph("Generic", edge_dict = edgeDict, vertex_dict=vertexDict, graph_type = "undirected", deep_copy=True)

        # test to see if genG is an instance of "GenericGraph"
        self.assertTrue("GenericGraph" in str(type(genG)))

        # test accessing edges 
        ew = genG.cost('v1', 'v2')
        self.assertEqual(ew, 1)

        # test accesing vertices
        vw = genG.cost('v14')
        self.assertEqual(vw, 6)

        # Test removal of edges. Should return a KeyError
        genG.remove_edges([('v1','v2')])
        genG.remove_edges([('v8','v5')])
        self.assertRaises(KeyError, genG.cost, 'v1', 'v2')
        self.assertRaises(KeyError, genG.cost, 'v8', 'v5')

        # Test removal of vertix 14. Should return a KeyError
        genG.remove_vertices(['v14'])
        self.assertRaises(KeyError, genG.cost, 'v14')

        # Test getting list of vertices. v14 just got removed
        self.assertEquals(set(genG.get_vertices()), set(['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13']))

        # try assigning a value to v1
        genG.add_vertex({'v1': 100})

        # try adding new edges from v1 and add back node v14
        genG.add_edge( {('v1','v9'): 19,
                        ('v10','v14'): 1010})

        self.assertEquals(set(genG.get_vertices()), set(['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v14']))

        # TODO return some neighbors and stuff
        pass

        # test GraphFactory in creating a Generic MyGraph object
    def test_create_generic_directed(self):

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
                    'v9': 1,
                    'v10': 2,
                    'v11': 3,
                    'v12': 4,
                    'v13': 5,
                    'v14': 6
                }
        
        # Create a generic graph using factory method
        genG = GraphFactory.create_graph("Generic", edge_dict = edgeDict, vertex_dict=vertexDict, graph_type = "directed", deep_copy=True)

        # test to see if genG is an instance of "GenericGraph"
        self.assertTrue("GenericGraph" in str(type(genG)))

        # test accessing edges 
        ew = genG.cost('v1', 'v2')
        self.assertEqual(ew, 1)

        # test accesing vertices
        vw = genG.cost('v14')
        self.assertEqual(vw, 6)

        # Test removal of edges. Should return a KeyError
        genG.remove_edges([('v1','v2')])
        genG.remove_edges([('v8','v5')])
        self.assertRaises(KeyError, genG.cost, 'v1', 'v2')
        self.assertRaises(KeyError, genG.cost, 'v8', 'v5')

        # Test removal of vertix 14. Should return a KeyError
        genG.remove_vertices(['v14'])
        self.assertRaises(KeyError, genG.cost, 'v14')

        # Test getting list of vertices. v14 just got removed
        self.assertEquals(set(genG.get_vertices()), set(['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13']))

        # try assigning a value to v1
        genG.add_vertex({'v1': 100})

        # try adding new edges from v1 and add back node v14
        genG.add_edge( {('v1','v9'): 19,
                        ('v10','v14'): 1010})

        self.assertEquals(set(genG.get_vertices()), set(['v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v14']))

    # test adding attributes to a generic graph (multiiple edge or vertex weights)
    def test_generic_graph_attribute_edges_directed(self):
        # Define edges, but give them a name
        edgeDict = {('r','p'): {"cap": 6, "flow": 0},
                    ('r','a'): {"cap": 1, "flow": 0},
                    ('r','q'): {"cap": 4, "flow": 0},
                    ('p','b'): {"cap": 3, "flow": 0},
                    ('p','q'): {"cap": 2, "flow": 0},
                    ('q','p'): {"cap": 1, "flow": 0},
                    ('q','b'): {"cap": 2, "flow": 0},
                    ('q','d'): {"cap": 6, "flow": 0},}
    
        # Try deleting specific edges
        genG = GraphFactory.create_graph("Generic", edge_dict = edgeDict, vertex_dict=None, graph_type = "directed", deep_copy=False)

        # Try adding additional keys. WARNING: existing keys will get overwritten!
        new_edges = {   ('b','a'): {"cap": 1, "flow": 0},
                        ('b','s'): {"cap": 8, "flow": 0},
                        ('a','c'): {"cap": 8, "flow": 0},
                        ('a','d'): {"cap": 1, "flow": 0},
                        ('c','q'): {"cap": 1, "flow": 0},
                        ('c','b'): {"cap": 2, "flow": 0},
                        ('c','s'): {"cap": 4, "flow": 0},
                        ('d','c'): {"cap": 1, "flow": 0},
                        ('d','s'): {"cap": 6, "flow": 0},}
        genG.add_edge(new_edges)

        # test to see if genG is an instance of "GenericGraph"
        self.assertTrue("GenericGraph" in str(type(genG)))

        # There should be 17 edges
        self.assertEqual(genG.edge_count(), 17)

        # Try getting nested weight names
        for e in edgeDict:
            val = genG.cost(e[0], e[1], name="cap")
            self.assertEqual(val, edgeDict[e]["cap"])

        # Try deleting edges
        remove_list = [('b','a'),('b','s'),('a','c')]
        genG.remove_edges(remove_list)

        # removed edges should not be in the graph. Test for error raise
        for e in remove_list:
            self.assertRaises(KeyError, genG.cost, e[0], e[1], name="cap")

        # add deep nested edge names. WARNING: existing keys will get overwritten!
        nested_edge = {('r','p'): {"level1": {"level2": {"level3": 300}}}}
        genG.add_edge(nested_edge)

        # Try getting nested_edge value
        self.assertEqual(genG.cost('r', 'p', name=["level1", "level2", "level3"]), 300)

        # Try getting only level 1
        self.assertEqual(genG.cost('r', 'p', name="level1"), {'level2': {'level3': 300}})

        # Try getting only level 1 as a list
        self.assertEqual(genG.cost('r', 'p', name=["level1"]), {'level2': {'level3': 300}})

        # checking neighbor of 
        self.assertEqual(set(genG.neighbors('r')), set(['p', 'a', 'q']) )
        self.assertEqual(set(genG.neighbors('q')), set(['p', 'b', 'd']) )
        self.assertEqual(set(genG.neighbors('c')), set(['b', 'q', 's']) )

    # test adding attributes to a generic graph (multiiple edge or vertex weights)
    def test_generic_graph_attribute_vertices_only(self):
        # Define edges, but give them a name
        vertexDict={    ('r','p'): {"cap": 6, "flow": 0},
                        ('r','a'): {"cap": 1, "flow": 0},
                        ('r','q'): {"cap": 4, "flow": 0},
                        ('p','b'): {"cap": 3, "flow": 0},
                        ('p','q'): {"cap": 2, "flow": 0},
                        ('q','p'): {"cap": 1, "flow": 0},
                        ('q','b'): {"cap": 2, "flow": 0},
                        ('q','d'): {"cap": 6, "flow": 0},}
        
        # Try deleting specific edges
        genG = GraphFactory.create_graph("Generic", edge_dict = None, vertex_dict=vertexDict, deep_copy=False)

        # Try adding additional keys. WARNING: existing keys will get overwritten!
        new_vertices = {   ('b','a'): {"cap": 1, "flow": 0},
                        ('b','s'): {"cap": 8, "flow": 0},
                        ('a','c'): {"cap": 8, "flow": 0},
                        ('a','d'): {"cap": 1, "flow": 0},
                        ('c','q'): {"cap": 1, "flow": 0},
                        ('c','b'): {"cap": 2, "flow": 0},
                        ('c','s'): {"cap": 4, "flow": 0},
                        ('d','c'): {"cap": 1, "flow": 0},
                        ('d','s'): {"cap": 6, "flow": 0},}
        genG.add_vertex(new_vertices)

        # test to see if genG is an instance of "GenericGraph"
        self.assertTrue("GenericGraph" in str(type(genG)))

        # There should be 17 nodes
        self.assertEqual(genG.node_count(), 17)

        # Try getting nested weight names
        for v in vertexDict:
            val = genG.cost(v, name="cap")
            self.assertEqual(val, vertexDict[v]["cap"])

        # Try deleting edges
        remove_list = [('b','a'),('b','s'),('a','c')]
        genG.remove_vertices(remove_list)

        # removed edges should not be in the graph. Test for error raise
        for v in remove_list:
            self.assertRaises(KeyError, genG.cost, v, name="cap")

        # add deep nested edge names. WARNING: existing keys will get overwritten!
        nested_vertex = {('r','p'): {"level1": {"level2": {"level3": 300}}}}
        genG.add_vertex(nested_vertex)

        # Try getting nested_edge value
        self.assertEqual(genG.cost(('r', 'p'), name=["level1", "level2", "level3"]), 300)

        # Try getting only level 1
        self.assertEqual(genG.cost(('r', 'p'), name="level1"), {'level2': {'level3': 300}})

        # Try getting only level 1 as a list
        self.assertEqual(genG.cost(('r', 'p'), name=["level1"]), {'level2': {'level3': 300}})
        
        # Checking for any neighbors should raise KeyError
        self.assertRaises(KeyError, genG.neighbors, ('r', 'p'))

    
    
if __name__ == "__main__":
    unittest.main()