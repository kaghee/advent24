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
    def __init__(self, robots, map_size):
        self.robots = robots
        self.map_size = map_size
        self.map = [[0 for i in range(self.map_size[0])]
                    for j in range(self.map_size[1])]

    def get_coords(self, robot: str):
        nums = [int(m.group()) for m in re.finditer(r"-?\d+", robot)]
        return (nums[0], nums[1]), (nums[2], nums[3])

    def update_map(self, new_pos):
        """ Updates the map with the new coordinate for a robot.
        Coordinates are swapped as we have the rows first in the 2d list. """
        updated = self.map[:]
        updated[new_pos[1]][new_pos[0]] += 1
        self.map = updated

    def move_all_for_time(self, seconds):
        for robot in self.robots:
            new_pos, vel = self.get_coords(robot)
            if seconds == 0:
                new_pos = self.move_robot((0, 0), new_pos)
            else:
                for i in range(seconds):
                    new_pos = self.move_robot(new_pos, vel)
            self.update_map(new_pos)

    def move_robot(self, pos, vel):
        new_x = pos[0] + vel[0]
        new_y = pos[1] + vel[1]

        if new_x >= self.map_size[0]:
            new_x -= self.map_size[0]
        if new_y >= self.map_size[1]:
            new_y -= self.map_size[1]

        if new_x < 0:
            new_x = self.map_size[0] + new_x
        if new_y < 0:
            new_y = self.map_size[1] + new_y

        return (new_x, new_y)

    def visualize(self):
        for line in self.map:
            print(line)

    def get_result(self):
        counter = [0 for _ in range(4)]

        for line in self.map[:self.map_size[1]//2]:
            counter[0] += sum(line[:self.map_size[0]//2])

        for line in self.map[:self.map_size[1]//2]:
            counter[1] += sum(line[self.map_size[0]//2+1:])

        for line in self.map[self.map_size[1]//2+1:]:
            counter[2] += sum(line[:self.map_size[0]//2])

        for line in self.map[self.map_size[1]//2+1:]:
            counter[3] += sum(line[self.map_size[0]//2+1:])

        return math.prod(counter)

    def run_task(self):
        self.move_all_for_time(100)
        return self.get_result()


if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '14')
    map_size = [11, 7] if use_example else [101, 103]
    lines = get_lines(input)

    print("Part I:")
    rr = RestroomRedoubt(lines, map_size)
    res = rr.run_task()
    print("Safety factor:", res)
