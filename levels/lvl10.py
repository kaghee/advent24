import sys
from input_parsers import parse_input, get_line_chars_as_ints


EXAMPLE = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732\
"""


class HoofIt:
    def __init__(self, lines):
        self.map = lines
        self.pos = None

    def get_trailheads(self):
        """ Collects the coordinates of 0s in the map. """
        trailheads = []
        for row, line in enumerate(self.map):
            coords = [(row, idx) for idx, x in enumerate(line) if x == 0]
            trailheads.extend(coords)
        return trailheads

    def can_proceed(self, pos, next_pos):
        """ Determines if the next position is part of the path, i.e. 
        the value at the next position is the value of the original position + 1. """
        return self.map[next_pos[0]][next_pos[1]] == self.map[pos[0]][pos[1]] + 1

    def get_next_positions(self, pos: list[int]) -> list[int]:
        """ Assembles a list of coordinates of the next walkable steps
        in all 4 directions on a path. """
        next_positions = []

        if pos[1] > 0:
            left = (pos[0], pos[1] - 1)
            if self.can_proceed(pos, left):
                next_positions.append(left)

        if pos[1] < len(self.map[0]) - 1:
            right = (pos[0], pos[1] + 1)
            if self.can_proceed(pos, right):
                next_positions.append(right)

        if pos[0] > 0:
            up = (pos[0] - 1, pos[1])
            if self.can_proceed(pos, up):
                next_positions.append(up)

        if pos[0] < len(self.map) - 1:
            down = (pos[0] + 1, pos[1])
            if self.can_proceed(pos, down):
                next_positions.append(down)

        return next_positions

    def proceed_on_path(self, pos):
        path_ends = []
        next_positions = self.get_next_positions(pos)

        for next_pos in next_positions:
            # If we're standing on a 9, it's the end of the path, return the coordinates.
            if self.map[next_pos[0]][next_pos[1]] == 9:
                path_ends.append(next_pos)

            # If we're not at 9, proceed on the path (in all directions).
            else:
                path_ends.extend(self.proceed_on_path(next_pos))

        return path_ends

    def run_task(self, count_all_paths=False):
        counter = 0
        trailheads = self.get_trailheads()
        for trailhead in trailheads:
            path_ends = self.proceed_on_path(trailhead)
            if count_all_paths:
                counter += len(path_ends)
            else:
                counter += len(set(path_ends))

        print("Sum of trailhead scores:", counter)


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '10')
    lines = get_line_chars_as_ints(input)

    print("Part I:")
    hi = HoofIt(lines)
    hi.run_task()

    print("Part II:")
    hi.run_task(count_all_paths=True)
