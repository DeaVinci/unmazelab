from multipledispatch import dispatch
import numpy as np
import random
import xml.etree.ElementTree as ET

from app.grid_wanderer import GridWanderer
from app.maze_wanderer import MazeWanderer

class Maze:
    @dispatch(int, int, int)
    def __init__(self, height, width, seed):
        self.size = np.array([height, width])
        self.seed = seed

    @dispatch(np.ndarray, int)
    def __init__(self, size, seed):
        self.size = size
        self.seed = seed

    @dispatch(ET.Element)
    def __init__(self, xml_config_tree_root):
        self.load(xml_config_tree_root)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        if type(size) != np.ndarray:
            raise ValueError("Size must be numpy.ndarray")
        if size.size != 2 or size.shape[0] != 2:
            raise ValueError("Size must be one dimensional array with two values")
        if (size < 2).any():
            raise ValueError("Both values of size must be equal or greater than 2")
        self._size = size
        self._start_pos = None
        self._finish_pos = None
        self.vertical_walls = None
        self.horizontal_walls = None

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, seed):
        if type(seed) != int:
            raise ValueError("Seed must be integer")
        self._seed = seed

    @property
    def start_pos(self):
        return self._start_pos

    @start_pos.setter
    def start_pos(self, start_pos):
        if type(start_pos) != np.ndarray:
            raise ValueError("Start position must be numpy.ndarray")
        if start_pos.size != 2 or start_pos.shape[0] != 2:
            raise ValueError("Start position must be one dimensional array with two values")
        if (start_pos < 0).any() or start_pos[0] >= self.size[0] or start_pos[1] >= self.size[1]:
            raise ValueError("Start position is outside of the maze")
        self._start_pos = start_pos

    @property
    def finish_pos(self):
        return self._finish_pos

    @finish_pos.setter
    def finish_pos(self, finish_pos):
        if type(finish_pos) != np.ndarray:
            raise ValueError("Finish position must be numpy.ndarray")
        if finish_pos.size != 2 or finish_pos.shape[0] != 2:
            raise ValueError("Finish position must be one dimensional array with two values")
        if (finish_pos < 0).any() or finish_pos[0] >= self.size[0] or finish_pos[1] >= self.size[1]:
            raise ValueError("Finish position is outside of the maze")
        self._finish_pos = finish_pos
    
    def load(self, xml_config_tree_root):
        self.size = np.array([int(xml_config_tree_root.find("height").text),
                              int(xml_config_tree_root.find("width").text)])
        self.seed = int(xml_config_tree_root.find("seed").text)

    def save(self, xml_config_tree_root):
        ET.SubElement(xml_config_tree_root, "height").text = str(self.size[0])
        ET.SubElement(xml_config_tree_root, "width").text = str(self.size[1])
        ET.SubElement(xml_config_tree_root, "seed").text = str(self.seed)

    def generate(self):
        random.seed(self.seed)
        self.generate_walls()
        self.generate_start_pos()
        self.generate_finish_pos()

    def generate_start_pos(self):
        mw = MazeWanderer(self)
        g = mw.get_grid_with_distanses_from_pos(np.array([self.size[0] - 1, self.size[1] - 1]))
        pos = g.argmax()
        self.start_pos = np.array([pos // self.size[1], pos % self.size[1]])

    def generate_finish_pos(self):
        mw = MazeWanderer(self)
        g = mw.get_grid_with_distanses_from_pos(self.start_pos)
        pos = g.argmax()
        self.finish_pos = np.array([pos // self.size[1], pos % self.size[1]])

    def generate_walls(self):
        gw = GridWanderer(self.size)
        self.set_walls_everywhere()
        for row in range(0, self.size[0]):
            for col in range(0, self.size[1]):
                while(True):
                    gw.current_pos = np.array([row, col])
                    unvisited_neighbours = gw.get_unvisited_neighbours()
                    if unvisited_neighbours.size == 0:
                        break
                    while True:
                        new_pos = random.choice(unvisited_neighbours)
                        self.remove_wall_between_neighbours(gw.current_pos, new_pos)
                        gw.current_pos = new_pos
                        unvisited_neighbours = gw.get_unvisited_neighbours()
                        if unvisited_neighbours.size == 0:
                            break

    def set_walls_everywhere(self):
        self.vertical_walls   = np.ones((self.size[0],     self.size[1] - 1), dtype=bool)
        self.horizontal_walls = np.ones((self.size[0] - 1, self.size[1]    ), dtype=bool)

    def remove_wall_between_neighbours(self, pos_1, pos_2):
        vect = pos_2 - pos_1
        if vect[0] == -1 and vect[1] == 0:
            self.horizontal_walls[pos_1[0] - 1][pos_1[1]] = False
        elif vect[0] == 1 and vect[1] == 0:
            self.horizontal_walls[pos_1[0]][pos_1[1]] = False
        elif vect[0] == 0 and vect[1] == -1:
            self.vertical_walls[pos_1[0]][pos_1[1] - 1] = False
        elif vect[0] == 0 and vect[1] == 1:
            self.vertical_walls[pos_1[0]][pos_1[1]] = False

    def get_frame_for_solver(self):
        frame  = f'{self.size[0]}\n{self.size[1]}\n'
        frame += f'{self.start_pos[0]}\n{self.start_pos[1]}\n'
        frame += f'{self.finish_pos[0]}\n{self.finish_pos[1]}\n'
        for value in np.nditer(self.vertical_walls):
            frame += f'{int(value)}\n'
        for value in np.nditer(self.horizontal_walls):
            frame += f'{int(value)}\n'
        return frame