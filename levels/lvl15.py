import sys
from Coordinate import Coordinate
from input_parsers import parse_input, get_lines
from map_utils import visualize
from warehouse.BigBox import BigBox
from warehouse.Box import Box
from warehouse.Robot import Robot
from warehouse.Space import Space
from warehouse.Wall import Wall


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
            [None for _ in range(len(self.wh_map[0]))] for _ in range(len(self.wh_map))
        ]
        self.big_warehouse: list[list[Robot | Box | Wall | Space]] = [
            [None for _ in range(len(self.wh_map[0]) * 2)] for _ in range(len(self.wh_map))
        ]

    def map_warehouse(self, with_big_warehouse=False):
        for x, row in enumerate(self.wh_map):
            for y, col in enumerate(row):
                if col == "@":
                    if with_big_warehouse:
                        self.robot = Robot(x, y*2, self.big_warehouse)
                    else:
                        self.robot = Robot(x, y, self.warehouse)

                    self.warehouse[x][y] = self.robot

                    self.big_warehouse[x][y*2] = self.robot
                    self.big_warehouse[x][y*2 + 1] = Space(x, y*2 + 1)
                elif col == "O":
                    self.warehouse[x][y] = Box(x, y, self.warehouse)

                    left_box = BigBox(x, y*2, self.big_warehouse, is_left=True)
                    right_box = BigBox(x, y*2 + 1, self.big_warehouse)

                    left_box.other_half = right_box
                    right_box.other_half = left_box
                    self.big_warehouse[x][y*2] = left_box
                    self.big_warehouse[x][y*2 + 1] = right_box
                elif col == "#":
                    self.warehouse[x][y] = Wall(x, y)

                    self.big_warehouse[x][y*2] = Wall(x, y*2)
                    self.big_warehouse[x][y*2 + 1] = Wall(x, y*2 + 1)
                elif col == ".":
                    self.warehouse[x][y] = Space(x, y)

                    self.big_warehouse[x][y*2] = Space(x, y*2)
                    self.big_warehouse[x][y*2 + 1] = Space(x, y*2 + 1)

    def run_task(self, with_big_warehouse=False):
        self.map_warehouse(with_big_warehouse)
        wh = self.big_warehouse if with_big_warehouse else self.warehouse
        visualize(wh)

        for direction in self.directions:
            self.robot.push(direction)
            visualize(wh)

        if with_big_warehouse:
            boxes = [
                obj.x * 100 + obj.y for line in wh for obj in line if type(obj) is BigBox and obj.is_left]
        else:
            boxes = [
                obj.x * 100 + obj.y for line in wh for obj in line if type(obj) is Box]
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

    print("Part II:")
    res = ww.run_task(with_big_warehouse=True)
    print("Sum of big box GPS coordinates:", res)
