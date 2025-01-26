class Coordinate:
    DIRECTIONS = "^>v<"

    MOVEMENTS = {
        DIRECTIONS[0]: (-1, 0),
        DIRECTIONS[1]: (0, 1),
        DIRECTIONS[2]: (1, 0),
        DIRECTIONS[3]: (0, -1)
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()
    
    def get_next_pos_in_dir(self, direction):
        dir_x, dir_y = Coordinate.MOVEMENTS[direction]
        return self + Coordinate(dir_x, dir_y)
