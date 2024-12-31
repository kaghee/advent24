from utils import get_file_lines


class GuardGallivant:
    def __init__(self, lines=None):
        self.DIRECTIONS = ["up", "right", "down", "left"]
        self.map = lines
        self.pos = None
        self.direction = "up"
        self.covered_map = [[col for col in row] for row in self.map]

    def locate_guard(self):
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                if col == "^":
                    self.pos = (y, x)
                    break

    def move_up(self, pos):
        self.pos = pos[0] - 1, pos[1]

    def move_down(self, pos):
        self.pos = pos[0] + 1, pos[1]

    def move_left(self, pos):
        self.pos = pos[0], pos[1] - 1

    def move_right(self, pos):
        self.pos = pos[0], pos[1] + 1

    def turn(self):
        try:
            self.direction = self.DIRECTIONS[self.DIRECTIONS.index(
                self.direction) + 1]

        except IndexError:
            self.direction = self.DIRECTIONS[0]

    def move_or_turn(self):
        """ Move one step.
        If there's a wall, revert to the previous position and turn 90deg.
        If it's the edge of the map, return the current position.
        Otherwise mark the path with X."""
        covered_area = 0
        self.covered_map[self.pos[0]][self.pos[1]] = "X"

        try:
            while self.pos[0] > 0 and self.pos[1] > 0:
                move_forward = getattr(self, f"move_{self.direction}")
                current_pos = self.pos[:]

                move_forward(self.pos)
                if self.map[self.pos[0]][self.pos[1]] == "#":
                    self.pos = current_pos
                    self.turn()
                else:
                    self.covered_map[self.pos[0]][self.pos[1]] = "X"
        except IndexError:
            print("Reached the end of the map at", self.pos)
        print("Reached the end of the map at", self.pos)

        for line in self.covered_map:
            covered_area += line.count("X")
        print("Covered area:", covered_area)


    def run_first_task(self):
        self.locate_guard()
        self.move_or_turn()


def run_first_task(file_name):
    lines = get_file_lines(file_name)
    GuardGallivant(lines).run_first_task()
