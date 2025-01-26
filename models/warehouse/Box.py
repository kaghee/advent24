from warehouse.Space import Space
from warehouse.WarehouseObject import WarehouseObject


class Box(WarehouseObject):

    def __init__(self, x, y, warehouse):
        super().__init__(x, y)
        self.warehouse = warehouse

    def __str__(self):
        return "O"

    def __repr__(self):
        return self.__str__()

    def push(self, direction):
        neighbour_coords = self.get_next_pos_in_dir(direction)
        neighbour_obj = self.warehouse[neighbour_coords.x][neighbour_coords.y]
        can_move = neighbour_obj.push(direction)

        if can_move:
            # Leave a space behind
            self.warehouse[self.x][self.y] = Space(self.x, self.y)
            # Move to the next position
            self.x = neighbour_coords.x
            self.y = neighbour_coords.y
            # Update the warehouse
            self.warehouse[self.x][self.y] = self
            return True
        else:
            return False
