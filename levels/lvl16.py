import sys

from input_parsers import get_line_chars, parse_input
from map_utils import is_on_map
import numpy as np
import networkx as nx
from networkx.algorithms.shortest_paths.weighted import single_source_dijkstra
from pprint import pprint

# lowest: 7036
EXAMPLE = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############\
"""


class ReindeerMaze:

    def __init__(self, maze_str: list[str]):
        self.maze_str = maze_str
        self.maze = []
        self.start = None
        self.end = None
        self.graph = nx.Graph()
        self.line_graph = nx.Graph()
        self.DIR_DIFFS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def get_neighbours(self, cell: tuple[int, int]):
        """ Gathers all neighbour coordinates of a cell. """
        neighbours = []

        for diff in self.DIR_DIFFS:
            next_cell = (cell[0] + diff[0], cell[1] + diff[1])
            if is_on_map(self.maze, next_cell) and self.maze[next_cell] == 0:
                neighbours.append(next_cell)

        return neighbours

    def generate_graph(self):
        self.maze = np.ones(
            (len(self.maze_str), len(self.maze_str)), dtype=int)

        for x, row in enumerate(self.maze_str):
            for y, col in enumerate(row):
                if col == "#":
                    self.maze[x][y] = 1
                else:
                    self.maze[x][y] = 0

                    if col == "S":
                        self.start = (x, y)
                    if col == "E":
                        self.end = (x, y)

                    cell = (x, y)
                    for nb_cell in self.get_neighbours(cell):
                        self.graph.add_edge(cell, nb_cell)

    def get_weight(self, u, v) -> int:
        """ Determines if the path between 2 given cells are in line or include a turn. """
        is_turning = u[0] != v[0] and u[1] != v[1]
        return 1001 if is_turning else 1

    def generate_line_graph(self):
        for node in self.graph.nodes:
            neighbours = list(self.graph[node].keys())

            if len(neighbours) == 1:
                continue

            # If the cell has 2 neighbours, we add 1 edge
            # (the path from neighbour 1 through node to neighbour 2)
            weight = self.get_weight(neighbours[0], neighbours[1])

            connection_AS = tuple(sorted([node, neighbours[0]]))
            connection_BS = tuple(sorted([node, neighbours[1]]))
            self.line_graph.add_edge(
                connection_AS, connection_BS, weight=weight)

            # If the cell has 3 neighbours, we need 2 additional paths/edges
            if len(neighbours) > 2:
                connection_CS = tuple(sorted([node, neighbours[2]]))
                weight = self.get_weight(neighbours[0], neighbours[2])
                self.line_graph.add_edge(
                    connection_AS, connection_CS, weight=weight)

                weight = self.get_weight(neighbours[1], neighbours[2])
                self.line_graph.add_edge(
                    connection_BS, connection_CS, weight=weight)

            # If the cell has 4 neighbours, we need 3 additional paths/edges
            if len(neighbours) > 3:
                connection_DS = tuple(sorted([node, neighbours[3]]))
                weight = self.get_weight(neighbours[0], neighbours[3])
                self.line_graph.add_edge(
                    connection_AS, connection_DS, weight=weight)

                weight = self.get_weight(neighbours[1], neighbours[3])
                self.line_graph.add_edge(
                    connection_BS, connection_DS, weight=weight)

                weight = self.get_weight(neighbours[2], neighbours[3])
                self.line_graph.add_edge(
                    connection_CS, connection_DS, weight=weight)

    def run_task(self):
        self.generate_graph()

        # Starting path/edge is the cell left of our start,
        # since our initial direction is East
        virtual_start = (self.start[0], self.start[1] - 1)

        self.graph.add_edge(virtual_start, self.start)
        self.generate_line_graph()

        end_neighbours = self.get_neighbours(self.end)
        for potential_last_step in end_neighbours:
            try:
                result = single_source_dijkstra(
                    self.line_graph, tuple(sorted([virtual_start, self.start])), tuple(sorted([potential_last_step, self.end])))
                print("Shortest path:", result[0])
            except Exception as e:
                print(e)


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '16')

    maze_str = get_line_chars(input)

    print("Part I:")
    rm = ReindeerMaze(maze_str)
    rm.run_task()
