import unittest

from graph_instances import MaxFlowGraphsTests

class TestMaxFlowCorrespondence(unittest.TestCase):

    def test_equivalence_answers(self):
        # returns a tuple (str, function_object)
        algs = ["edmonds_karp", "push_relabel"]
        sols = []
        for alg in algs:
            sols.append(MaxFlowGraphsTests.return_alg_sol(alg))

        for j in range(len(sols[0])):
            val = []
            for i, alg in enumerate(algs):            
                val.append(sols[i][j])
            if not all(val):
                raise ValueError("Not All values are the same!")

if __name__ == "__main__":  
    unittest.main()