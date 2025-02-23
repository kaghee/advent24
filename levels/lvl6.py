import sys
from input_parsers import parse_input, get_line_chars


EXAMPLE = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...\
"""

class GuardGallivant:
    def __init__(self, lines=None):
        self.DIRECTIONS = ["up", "right", "down", "left"]
        self.map = lines
        self.covered_positions = []
        self.start = None
        self.pos = None
        self.direction = "up"

    def locate_guard(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if col == "^":
                    self.start = (y, x)
                    break

    def reset(self):
        self.pos = self.start
        self.direction = "up"

    def get_next_pos(self):
        if self.direction == "up":
            return self.pos[0] - 1, self.pos[1]
        elif self.direction == "down":
            return self.pos[0] + 1, self.pos[1]
        elif self.direction == "left":
            return self.pos[0], self.pos[1] - 1
        elif self.direction == "right":
            return self.pos[0], self.pos[1] + 1

    def turn(self):
        try:
            self.direction = self.DIRECTIONS[self.DIRECTIONS.index(
                self.direction) + 1]

        except IndexError:
            self.direction = self.DIRECTIONS[0]

    def is_within_map(self):
        height = len(self.map) - 1
        width = len(self.map[0]) - 1
        return self.pos[0] > 0 and self.pos[1] > 0 and self.pos[0] < height and self.pos[1] < width

    def move_or_turn(self):
        """ Moves forward and turns whenever a wall is hit until the edge of the map is reached.
        Returns the covered path and a boolean indicating if a loop was found. """
        covered_path = dict()

        while self.is_within_map():
            # Determine what the next step would be.
            next_pos = self.get_next_pos()

            # If there's a wall, turn 90 degrees instead of moving.
            if self.map[next_pos[0]][next_pos[1]] == "#":
                self.turn()
            else:
                # Move forward and mark the path (with direction) as covered.
                self.pos = next_pos
                if covered_path.get(self.pos) is None:
                    covered_path[self.pos] = [self.direction]
                elif self.direction not in covered_path[self.pos]:
                    covered_path[self.pos].append(self.direction)
                else:
                    # This path has been covered before, we're in a loop.
                    return covered_path, True

        return covered_path, False

    def run_first_task(self):
        self.locate_guard()
        self.reset()
        covered, _ = self.move_or_turn()
        print("Covered area:", len(covered))
        return covered


    def run_second_task(self):
        loop_counter = 0
        covered_positions = self.run_first_task()

        for item in covered_positions.items():
            # Add an obstacle to the map.
            pos = item[0]
            self.map[pos[0]][pos[1]] = "#"
            self.reset()
            # Go through the path with the new map.
            _, is_loop = self.move_or_turn()
            if is_loop:
                loop_counter += 1
            # Restore original map
            self.map[pos[0]][pos[1]] = "."

        if self.start in [item[0] for _, item in enumerate(covered_positions)]:
            loop_counter -= 1

        print("Loops found:", loop_counter)


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '6')
    lines = get_line_chars(input)

    gg = GuardGallivant(lines)
    print("Part I:")
    gg.run_first_task()

    print("\nPart II:")
    gg.run_second_task()
