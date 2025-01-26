import sys
from Coordinate import Coordinate
from input_parsers import parse_input, get_lines
from warehouse.Box import Box
from warehouse.Robot import Robot
from warehouse.Space import Space
from warehouse.Wall import Wall


# sum: 2028
# EXAMPLE = """\
# ########
# #..O.O.#
# ##@.O..#
# #...O..#
# #.#.O..#
# #...O..#
# #......#
# ########

# <^^>>>vv<v>>v<<\
# """

# sum: 10092
EXAMPLE = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^\
"""


class WarehouseWoes:
    def __init__(self, wh_map: list[str], directions: str):
        self.wh_map: list[str] = wh_map
        self.directions: str = directions
        self.robot: Coordinate = None

        self.warehouse: list[list[Robot | Box | Wall | Space]] = [
            [None for i in range(len(self.wh_map[0]))] for j in range(len(self.wh_map))
        ]

    def parse_map(self):
        for x, row in enumerate(self.wh_map):
            for y, col in enumerate(row):
                if col == "@":
                    self.robot = Robot(x, y, self.warehouse)
                    self.warehouse[x][y] = self.robot
                elif col == "O":
                    self.warehouse[x][y] = Box(x, y, self.warehouse)
                elif col == "#":
                    self.warehouse[x][y] = Wall(x, y)
                elif col == ".":
                    self.warehouse[x][y] = Space(x, y)

    def visualize(self):
        print('\n\n')
        for line in self.warehouse:
            print("".join([str(x) for x in line]))

    def run_task(self):
        self.parse_map()

        for direction in self.directions:
            self.robot.push(direction)
            self.visualize()

        boxes = [obj.x * 100 + obj.y for line in self.warehouse for obj in line if type(obj) is Box]
        return sum(boxes)

if __name__ == "__main__":
    use_example = "-e" in sys.argv
    input = EXAMPLE if use_example else parse_input('2024', '15')

    lines = get_lines(input)
    warehouse_map = [list(l) for l in lines[:lines.index("")]]
    moves = "".join(lines[lines.index("") + 1:])

    print("Part I:")
    ww = WarehouseWoes(warehouse_map, moves)
    res = ww.run_task()
    print("Sum of box GPS coordinates:", res)
