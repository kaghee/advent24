from utils import get_file_lines


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

    def is_within_map(self):
        return self.pos[0] > 0 and self.pos[1] > 0 and self.pos[0] < len(self.map) - 1 and self.pos[1] < len(self.map[0]) - 1

    def move_or_turn(self):
        """ Moves forward until a wall is hit.
        Returns the covered path and a boolean indicating if a loop was found. """
        covered_in_current_run = []

        while self.is_within_map():
            current_pos = self.pos[:]
            # Take one step forward.
            move_forward = getattr(self, f"move_{self.direction}")
            move_forward(self.pos)

            # If there's a wall, turn 90 degrees instead of moving.
            if self.map[self.pos[0]][self.pos[1]] == "#":
                self.pos = current_pos
                self.turn()
            else:
                # Mark the path (with direction) as covered.
                if [self.pos, self.direction] not in covered_in_current_run:
                    covered_in_current_run.append([self.pos, self.direction])
                else:
                    # This path has been covered before, we're in a loop.
                    return covered_in_current_run, True

        return covered_in_current_run, False

    def run_first_task(self):
        self.locate_guard()
        self.reset()
        covered, _ = self.move_or_turn()
        return covered

    def run_second_task(self):
        loop_counter = 0
        covered_positions = self.run_first_task()

        for item in covered_positions:
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

        return loop_counter


def run_first_task(file_name):
    lines = get_file_lines(file_name)
    result = GuardGallivant(lines).run_first_task()
    print("Covered area:", len(result))


def run_second_task(file_name):
    lines = get_file_lines(file_name)
    result = GuardGallivant(lines).run_second_task()
    print("Loops found:", result)
