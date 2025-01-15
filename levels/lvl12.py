import sys
from input_parsers import get_line_chars, parse_input

# total price 140
# EXAMPLE = """\
# AAAA
# BBCD
# BBCC
# EEEC\
# """

# total price 772
# EXAMPLE = """\
# OOOOO
# OXOXO
# OOOOO
# OXOXO
# OOOOO\
# """

# total price 1930
EXAMPLE = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE\
"""


class GardenGroups:
    def __init__(self, garden):
        self.garden = garden
        self.groups_info = {}
        self.graph = {}
        self.unique_key = 0
        self.is_new_group = False
        self.DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)
                           ]  # up, right, down, left

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, node_1, node_2):
        if node_1 in self.graph and node_2 in self.graph:
            self.graph[node_1].append(node_2)
            self.graph[node_2].append(node_1)

    def is_on_map(self, cell: tuple[int, int]) -> bool:
        """ Checks if the cell is within the map boundaries. """
        size = len(self.garden)
        return cell[0] >= 0 and cell[1] >= 0 and cell[0] < size and cell[1] < size

    def is_valid_group_member(self, a: tuple[int, int], b: tuple[int, int]) -> bool:
        """ Checks if the second coordinate is within the map
        and if it's in the same group as the first one."""
        if not self.is_on_map(b):
            return False

        group = self.garden[a[0]][a[1]]
        other_group = self.garden[b[0]][b[1]]
        return group == other_group

    def get_neighbours_in_group(self, cell: tuple[int, int]):
        """ Gathers all neighbour coordinates that belong
        to the same group as the cell. """
        neighbours = []

        for diff in self.DIRECTIONS:
            next_cell = (cell[0] + diff[0], cell[1] + diff[1])
            if self.is_valid_group_member(cell, next_cell):
                neighbours.append(next_cell)

        return neighbours

    def add_nodes_to_graph(self, cell, neighbours):
        self.add_node(cell)
        for neighbour in neighbours:
            self.add_edge(cell, neighbour)

    def dfs(self, cell: tuple[int, int], visited: set):
        """ Checks the neighbouring cells and increases the area and number of fences
        for every cell based on how many neighbour cells belong to the same group."""
        if cell not in visited:
            neighbours = self.get_neighbours_in_group(cell)
            current_group = self.garden[cell[0]][cell[1]]

            if current_group not in self.groups_info:
                # We are in a new group. Add a new entry to our data.
                self.groups_info[current_group] = {
                    "area": 1, "fences": 4 - len(neighbours)}
            elif self.is_new_group:
                # We are in a new group but we already covered a group with this name.
                # Alter the previous group's name before storing this new one.
                self.unique_key += 1
                self.groups_info[self.unique_key] = self.groups_info[current_group]
                del self.groups_info[current_group]

                self.groups_info[current_group] = {
                    "area": 1, "fences": 4 - len(neighbours)}
            else:
                # We are still within the current group. Increase the area and fences.
                self.groups_info[current_group]["area"] += 1
                self.groups_info[current_group]["fences"] += 4 - \
                    len(neighbours)

            visited.add(cell)
            self.is_new_group = False

            for neighbour in neighbours:
                self.dfs(neighbour, visited)

    def run_task(self):
        visited = set()

        # Create a graph from the map, where nodes are the cells and
        # edges exist between nodes that make up a connected graph.
        for i, row in enumerate(self.garden):
            for j, _ in enumerate(row):
                cell = (i, j)
                neighbours = self.get_neighbours_in_group(cell)
                self.add_nodes_to_graph(cell, neighbours)

        # Traverse the graph recursively to collect data. Take note of
        # every new group (= every new disconnected graph within the graph).
        for g in list(self.graph):
            if g not in visited:
                self.is_new_group = True
                self.dfs(g, visited)

        price = sum([x["area"] * x["fences"]
                    for x in self.groups_info.values()])

        print("Total price:", price)


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '12')
    garden = get_line_chars(input)

    print("Part I:")
    gg = GardenGroups(garden)
    gg.run_task()

    # print("Part II:")
    # gg.run_task()
