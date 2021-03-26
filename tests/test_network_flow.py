import unittest

from simpleGraphM.graph import GraphFactory

class TestGenericGraph(unittest.TestCase):

    def max_flow_with_fordfulkerson(self):
        # Define some edges
        edgeDict = {('r','p'): {"cap": 6, "flow": 0},
                    ('r','a'): {"cap": 1, "flow": 0},
                    ('r','q'): {"cap": 4, "flow": 0},
                    ('p','b'): {"cap": 3, "flow": 0},
                    ('p','q'): {"cap": 2, "flow": 0},
                    ('q','p'): {"cap": 1, "flow": 0},
                    ('q','b'): {"cap": 2, "flow": 0},
                    ('q','d'): {"cap": 6, "flow": 0},
                    ('b','a'): {"cap": 1, "flow": 0},
                    ('b','s'): {"cap": 8, "flow": 0},
                    ('a','c'): {"cap": 8, "flow": 0},
                    ('a','d'): {"cap": 1, "flow": 0},
                    ('c','q'): {"cap": 1, "flow": 0},
                    ('c','b'): {"cap": 2, "flow": 0},
                    ('c','s'): {"cap": 4, "flow": 0},
                    ('d','c'): {"cap": 1, "flow": 0},
                    ('d','s'): {"cap": 6, "flow": 0},
                    }

if __name__ == "__main__":
    unittest.main()