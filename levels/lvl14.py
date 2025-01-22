import sys
import re
import math
from input_parsers import parse_input, get_lines

EXAMPLE = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3\
"""


class RestroomRedoubt:
    def __init__(self, lines, map_size):
        self.lines = lines
        self.robots = []
        self.width = map_size[0]
        self.height = map_size[1]

    def initialize_robots(self):
        for line in self.lines:
            start, vel = self.get_coords_from_line(line)
            self.robots.append({"pos": start, "vel": vel})

    def get_coords_from_line(self, line: str):
        """ Reads the position and velocity coordinates for a robot. """
        nums = [int(m.group()) for m in re.finditer(r"-?\d+", line)]
        return (nums[0], nums[1]), (nums[2], nums[3])

    def move_all_robots(self, seconds):
        """ Determines the new position of each robot after the specified
        no. of seconds, and updates the map with their new position. """
        for robot in self.robots:
            robot["pos"] = self.move_robot(robot["pos"], robot["vel"], seconds)

    def move_robot(self, pos, vel, seconds):
        """ Calculates the new position of a robot after n seconds,
        considering jumping to the other edge when reaching the end of the map. """
        new_x = (pos[0] + vel[0] * seconds) % self.width
        new_y = (pos[1] + vel[1] * seconds) % self.height

        return (new_x, new_y)

    def visualize(self):
        """ Prints the map in a grid. """
        r_map = [[0 for _ in range(self.width)]
                 for _ in range(self.height)]
        for robot in self.robots.values():
            x, y = robot["pos"]
            r_map[y][x] += 1

        for line in r_map:
            print(line)

    def get_result(self):
        """ Calculates the product of the no. of robots in each quadrant. """
        quadrants = [0] * 4
        width = self.width // 2
        height = self.height // 2

        for rob in self.robots:
            x = rob["pos"][0]
            y = rob["pos"][1]

            if x < width and y < height:
                quadrants[0] += 1
            elif x > width and y < height:
                quadrants[1] += 1
            elif x < width and y > height:
                quadrants[2] += 1
            elif x > width and y > height:
                quadrants[3] += 1

        return math.prod(quadrants)

    def run_task(self):
        self.move_all_robots(100)
        return self.get_result()

    def is_in_frame(self, rob, k):
        frame_w = self.width // 2
        frame_h = self.height // 2
        x, y = rob["pos"]
        return k <= x <= k + frame_w and k <= y <= k + frame_h

    def find_xmas_tree(self):
        i = 1
        frame_size = 50
        threshold = len(self.robots) * 0.5
        while True:
            self.move_all_robots(1)
            for k in range(self.width - frame_size):
                bots_in_block = [
                    rob for rob in self.robots if self.is_in_frame(rob, k)]

                if len(bots_in_block) > threshold:
                    return i

            i += 1


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '14')
    map_size = [11, 7] if use_example else [101, 103]
    lines = get_lines(input)

    print("Part I:")
    rr = RestroomRedoubt(lines, map_size)
    rr.initialize_robots()
    res = rr.run_task()
    print("Safety factor:", res)

    print("Part II:")
    res = rr.find_xmas_tree()
    print("Tree found at:", res)
