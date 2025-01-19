import sys
from input_parsers import get_line_chars, parse_input


# total price 1930 / 1206
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
        self.graph = {}
        self.DIR_DIFFS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, node_1, node_2, weight):
        node_2_coords = (node_2[0], node_2[1])
        if node_1 in self.graph and node_2_coords in self.graph:
            self.graph[node_1].append((node_2_coords, weight))
            self.graph[node_2_coords].append((node_1, weight))

    def is_on_map(self, cell: tuple[int, int]) -> bool:
        """ Checks if the cell is within the map boundaries. """
        size = len(self.garden)
        return cell[0] >= 0 and cell[1] >= 0 and cell[0] < size and cell[1] < size

    def are_same_group(self, a, b):
        """ Checks if two cells belong to the same group. """
        return self.garden[a[0]][a[1]] == self.garden[b[0]][b[1]]

    def get_neighbours(self, cell: tuple[int, int], in_same_group: bool = False):
        """ Gathers all neighbour coordinates of a cell. """
        neighbours = []

        for diff in self.DIR_DIFFS:
            next_cell = (cell[0] + diff[0], cell[1] + diff[1])
            neighbours.append(next_cell if self.is_on_map(next_cell) else None)

        if in_same_group:
            return [nb if nb and self.are_same_group(cell, nb) else None for nb in neighbours]
        else:
            return neighbours

    def get_discount(self, cell, next_cell):
        """ Calculates how much discount a pair of cells will get,
        based on the number of sides they share on the map (i.e.
        if they're on the edge of the map or if they have non-group cells
        on their same side.)"""
        cell_neighbours = [nb for nb in self.get_neighbours(
            cell, in_same_group=True)]
        next_cell_neighbours = [nnb for nnb in self.get_neighbours(
            next_cell, in_same_group=True)]

        discount = len(
            [i for i, j in zip(cell_neighbours, next_cell_neighbours) if i is None and j is None])
        return discount

    def add_nodes_to_graph(self, cell, neighbours):
        """ Adds node and edges to the graph based on neighbours.
        Discounts are stored as edge weights."""
        self.add_node(cell)
        same_group_neighbours = [
            nb for nb in neighbours if nb and self.are_same_group(cell, nb)]

        for nb_cell in same_group_neighbours:
            discount = self.get_discount(cell, nb_cell)
            self.add_edge(cell, nb_cell, discount)

    def dfs(self, cell: tuple[int, int], visited: set):
        """ Returns all the nodes that belong to a group
        by checking the neighbouring cells. """
        nodes_in_group = []
        if cell not in visited and cell is not None:
            neighbours = [nb for nb in self.get_neighbours(
                cell, in_same_group=True) if nb is not None]

            visited.add(cell)
            nodes_in_group.append(cell)

            for neighbour in neighbours:
                nbs = self.dfs(neighbour, visited)
                if nbs:
                    nodes_in_group.extend(nbs)

            return nodes_in_group

    def calculate_price(self, groups, with_discount: bool = False):
        total_price = 0
        for group in groups:
            area = len(group)
            fences = 0
            discount = 0
            for node in group:
                fences += 4 - len(self.graph[node])
                discount += sum([n[1] for n in self.graph[node]])

            if with_discount:
                total_price += area * (fences - discount // 2)
            else:
                total_price += area * fences

        return total_price

    def run_task(self):
        # Create a graph from the map, where the cells are the nodes and
        # edges exist between nodes that make up a connected graph.
        visited = set()
        for i, row in enumerate(self.garden):
            for j, _ in enumerate(row):
                cell = (i, j)
                neighbours = self.get_neighbours(cell)
                self.add_nodes_to_graph(cell, neighbours)

        # Traverse the graph recursively to collect data. Store every
        # new group (= every new disconnected graph within the graph).
        groups = []
        for g in list(self.graph):
            if g not in visited:
                nodes_in_group = self.dfs(g, visited)
                groups.append(nodes_in_group)

        # Calculate the total price of all the groups.
        total_price = self.calculate_price(groups)
        discount_price = self.calculate_price(groups, with_discount=True)

        print("Total price:", total_price)
        print("Total price with discount:", discount_price)


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '12')
    garden = get_line_chars(input)

    print("Part I and II:")
    gg = GardenGroups(garden)
    gg.run_task()
