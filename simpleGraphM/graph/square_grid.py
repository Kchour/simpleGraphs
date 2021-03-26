import numpy as np
import matplotlib.pyplot as plt

from .graph import Graph
from .grid_utils import init_grid
from .grid_utils import get_index
from .grid_utils import get_world

class SquareGrid(Graph):
    """Class for defining SquareGrid type graphs, to be subclassed to use properly

    Attributes:
        self.xwidth
        self.yheight 
        self.grid (2D numpy array)

    """
    def __init__(self, grid=None, grid_dim=None, grid_size=None, neighbor_type=4, init_val=0):
        self.xwidth = grid_dim[1] - grid_dim[0]  + 1
        self.yheight = grid_dim[3] - grid_dim[2] + 1
        self.grid_size = grid_size
        self.grid_dim = grid_dim
        self.neighbor_type = neighbor_type

        if grid is not None:
            self.grid = grid
        else:
            self.grid = init_grid(grid_dim, grid_size, init_val=init_val)

    def neighbors(self):
        pass

    def cost(self):
        pass

    def set_node_value(self, x, y, values):
        self.grid[y][x] = values

class OccupancySquareGrid(SquareGrid):
    """A grid-based occupancy graph class. Physical coordinates origin (0,0) starts at the lower-left corner,
        while the index coordinate origin starts at the top-left. To add obstacles, the user has a couple of options.
        First, they may pass in a numpy array 'grid' with (index coordinates) indicies already specified as 1
        Second, users may pass in a list of obstacles (in physical coordinates) 
        Third, users may call the "set_obstacles(o)" function, where 'o' is a list of obstacles

    Parameters:
        grid (numpy 2d Array): Optional, 0s indicate free space, 1s indicate obstacles
        grid_dim (tuple): In the form of (minX, maxX, minY ,maxY) 
        grid_size (float or int): Discrete size of each grid block (assumed uniform)
        n_type (int): Number of neighbors for each node, 4 or 8
        obstacles (list): Each element is a tuple, representing the obstacles on the graph 

    Attributes:
        obstacles (list): A list of tuples, representing obstacles (x,y)
        xwidth (int): the width of the grid
        yheight (int): the height of the grid
        grid (numpy.ndarray): an numpy array grid
        grid_dim (tuple): The physical coord limits expressed as (minX, maxX, minY ,maxY) 
        grid_size (float or int): Discrete size of each grid block (assumed uniform)
        neighbor_type (int): Number of neighbors for each node, 4 or 8 

    Todo:
        - Allow for grid transformations?
        - Fix height and width

    """
    def __init__(self, grid=None, grid_dim=None, grid_size=None, neighbor_type=4, obstacles=None):
        super().__init__(grid=grid, grid_dim=grid_dim, grid_size=grid_size, neighbor_type=neighbor_type)
        self.obstacles = obstacles

        # if obstacles are defined, add ogm. Else init an empty grid
        if obstacles is not None and obstacles:
            # ogm = OccupancyGridMap(grid_size, grid_dim, obstacles)
            # self.grid = ogm.grid 
            self.set_obstacles(obstacles)
        else:
            self.grid = init_grid(grid_dim, grid_size, init_val=0)

    def set_obstacles(self, obs):
        """ 
        parameter:
            obs (list): a list of tuples, where tuple is an obstacle (x,y)

        """
        # convert to numpy if not already
        if 'numpy' not in str(type(obs)):
            obs = np.array(obs)

        obj_inds = get_index(obs[:, 0], obs[:, 1], self.grid_size, self.grid_dim)
        self.grid[obj_inds[1], obj_inds[0]] = 1.0

        # Store obs list
        self.obstacles = obs

    def in_bounds(self, ind, type_='map'):
        """ Test whether a coordinate is inside the grid boundaries

        Parameters:
            ind (tuple): x,y coordinate
            type_ (str): either map coordinates 'map', or physical world coordinates 'world'
        
        Returns:
            True: if coordinate is inside the boundaries
            False: otherwise

        """
        if type_ == 'world':
            (x, y) = ind
            return self.grid_dim[0] <= x <= self.grid_dim[1] and self.grid_dim[2] <= y <= self.grid_dim[3]
        else:
            # grid indices
            (indx, indy) = ind
            xcells = int(np.floor((self.xwidth) / self.grid_size))
            ycells = int(np.floor((self.yheight) / self.grid_size))
            return 0 <= indx <= xcells and 0 <= indy <= ycells

    def not_obstacles(self, ind, type_='map'):
        """ Test whether a coordinate coincides with an obstacle

        Parameters:
            ind (tuple): x,y coordinate
            type_ (str): either map coordinates 'map', or physical world coordinates 'world'
        
        Returns:
            True: if not an obstacle
            False: otherwise

        """
        if type_ == 'world':
            # convert world to ind first
            (indx, indy) = get_index(ind[0], ind[1], self.grid_size, self.grid_dim)
            return self.grid[indy, indx] == 0
        else:
            (indx, indy) = ind
            return self.grid[indy, indx] == 0
            

    def neighbors(self, node):
        """ Compute neighbors of a node, keep working in world coordinates 
      
        Parameter:
            node (tuple): node that we want to find neighbors about

        Returns:
            results (iterable): an iterable generator of neighbors
            
        """
        (x, y) = node
        if self.neighbor_type == 4:
            results = [(x + self.grid_size, y), (x, y - self.grid_size),
                       (x - self.grid_size, y), (x, y + self.grid_size)]
        elif self.neighbor_type == 8:
            results = [(x + self.grid_size, y), (x, y - self.grid_size),
                       (x - self.grid_size, y), (x, y + self.grid_size),
                       (x + self.grid_size, y + self.grid_size), (x + self.grid_size, y - self.grid_size),
                       (x - self.grid_size, y - self.grid_size), (x - self.grid_size, y + self.grid_size)]

        # Only return coordinates that are in range
        results = filter(lambda x: self.in_bounds(x, type_='world'), results)

        # Only return coordinates that are not obstacles
        results = filter(lambda x: self.not_obstacles(x, type_='world'), results)

        return results

    # Cost of moving from one node to another (edge cost)
    def cost(self, from_node, to_node):
        """edge cost based on grid-based calculations """
        (x1, y1) = from_node
        (x2, y2) = to_node
        dmax = max(abs(x1 - x2), abs(y1 - y2))
        dmin = min(abs(x1 - x2), abs(y1 - y2))
        return 1.414*dmin + (dmax - dmin)

    def show_grid(self):
        """A method to display the current occupancy grid"""

        # Get grid dims
        minX, maxX, minY, maxY = self.grid_dim

        # get fig, ax objects
        self.fig = plt.figure()
        self.ax = self.fig.gca()

        # plotting in a non-blocking manner
        # plt.ion()
        # plt.draw()

        plt.pause(0.75)

        self.fig.canvas.draw_idle() 
        plt.show(block=False)

        # if interacting with canvas directly, must flush events after drawing
        # self.fig.canvas.flush_events()
        background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

        # show grid as an image i.e. on a 2d raster
        # cmap _r indicates reversed (i.e. Blues_r, Black_r)
        # plt.draw()
        im = self.ax.imshow(
            self.grid,
            origin='lower',
            interpolation='none',
            alpha=1,
            vmin=0,
            vmax=1,
            extent=[
                minX,
                maxX,
                minY,
                maxY],
            cmap='Blues')
        plt.title("Occupancy Grid Map")
        plt.axis('scaled')  #equal is another one
        plt.grid()
        
        self.fig.canvas.restore_region(background)
        # Draw artists on helper objects
        self.ax.draw_artist(im)

        self.fig.canvas.blit(self.ax.bbox)

        # must call fig.canvas.flush_events() (called by pause internally)
        self.fig.canvas.flush_events()
        plt.pause(0.001)