from warehouse.WarehouseObject import WarehouseObject


class Wall(WarehouseObject):

    def __init__(self, x, y):
        super().__init__(x, y)

    def __str__(self):
        return "#"

    def __repr__(self):
        return self.__str__()

    def push(self, direction):
        return False
    
    def try_push(self, direction):
        return False
