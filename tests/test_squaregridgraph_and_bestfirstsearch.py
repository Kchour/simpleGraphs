import unittest

from simpleGraphM.graph import GraphFactory
from simpleGraphM.algorithms.search import BestFirstSearch

class TestSquaregridGraph(unittest.TestCase):

    ''' Test GraphFactory in creating a SquareGrid object '''
    def test_create_square_grid_obs_list(self):
        # Spec out our squareGrid
        minX = -15			# [m]
        maxX = 15           
        minY = -15
        maxY = 15
        grid = None         # pre-existing 2d numpy array?
        grid_size = 1       # grid fineness[m]
        grid_dim = [minX, maxX, minY, maxY]
        neighbor_type = 8           # neighbor type

        # Create a squareGrid using GraphFactory
        sq = GraphFactory.create_graph("OccupancySquareGrid", grid=grid, grid_dim=grid_dim, grid_size=grid_size, neighbor_type= neighbor_type)      

        # test to see if sq is an instance of SquareGrid
        self.assertTrue("OccupancySquareGrid" in str(type(sq)))

        # test if instance values are correct
        self.assertEqual(sq.grid_size, grid_size)
        self.assertEqual(sq.grid_dim, grid_dim) 
        self.assertEqual(sq.neighbor_type, neighbor_type)

        # Define obstacles (physical coordinates, origin is lower-left)
        obstacles = [(x, 0) for x in range(-10,10,1)]
        obstacles.extend([(0, y) for y in range(-10,10,1)])

        # We can either add obstacles using 'set_obstacle' method, or do it with GraphFactory
        sq.set_obstacles(obstacles)

        # Show image (comment this out if it blocks)
        sq.show_grid()
        print("")

        # TODO: test the other functions in SquareGrid       

    def test_occupancy_square_grid_best_first_search(self):
        # Spec out our squareGrid
        minX = -15			# [m]
        maxX = 15           
        minY = -15
        maxY = 15
        grid = None         # pre-existing 2d numpy array?
        grid_size = 1       # grid fineness[m]
        grid_dim = [minX, maxX, minY, maxY]
        neighbor_type = 8           # neighbor type

        # Create a squareGrid using GraphFactory
        sq = GraphFactory.create_graph("OccupancySquareGrid", grid=grid, grid_dim=grid_dim, grid_size=grid_size, neighbor_type= neighbor_type)      

        # Create BFS object, with A*star
        bfs = BestFirstSearch(graph=sq, start=(-15,-15), goal=(15,15), heuristic_type='diagonal_nonuniform', visualize=False)
        parent_astar, cost_so_far_astar = bfs.run()

        # Create BFS object with Dijkstra
        bfs = BestFirstSearch(graph=sq, start=(-15,-15), goal=(15,15), heuristic_type=None, visualize=False)
        parent_dijkstra, cost_so_far_djikstra = bfs.run()

        # assert size of cost_so_far
        self.assertGreaterEqual(len(cost_so_far_djikstra), len(cost_so_far_astar))
        print("")

    #def test_IGraph_abstract(self):

    # TODO Mocks are for calls that are external to the code under test
    # https://stackoverflow.com/questions/45680483/python-unit-testing-class-properties 
    # @patch('__main__.SquareGrid')
    # def test_mock_square_grid(self, mock_squareGrid)
    # # Create a mock square grid
    # mock_squareGrid.return_value = SquareGrid(grid=grid, grid_dim=grid_dim, grid_size=grid_size, n_type= n_type)

    
if __name__ == "__main__":
    unittest.main()