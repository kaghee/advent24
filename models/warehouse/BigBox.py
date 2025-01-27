from warehouse.Box import Box


class BigBox(Box):

    def __init__(self, x, y, warehouse, is_left=False):
        super().__init__(x, y, warehouse)
        self.warehouse = warehouse
        self.is_left = is_left
        self.other_half = None
        self.try_in_progress = False
        self.push_in_progress = False

    def __str__(self):
        return "[" if self.is_left else "]"

    def __repr__(self):
        return self.__str__()

    def try_push(self, direction):
        self.try_in_progress = True

        neighbour_coords = self.get_next_pos_in_dir(direction)
        neighbour_obj = self.warehouse[neighbour_coords.x][neighbour_coords.y]

        can_move = neighbour_obj.try_push(direction)

        if not self.other_half.try_in_progress and not self.other_half.push_in_progress:
            can_move &= self.other_half.try_push(direction)

        self.try_in_progress = False
        return can_move

    def push(self, direction):
        self.push_in_progress = True

        if direction in ["<", ">"]:
            self.push_in_progress = False
            return super().push(direction)
        else:
            can_move = self.try_push(direction)
            if can_move:
                super().push(direction)
                if not self.other_half.push_in_progress:
                    self.other_half.push(direction)

            self.push_in_progress = False
            return can_move
