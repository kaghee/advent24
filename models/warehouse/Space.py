from warehouse.WarehouseObject import WarehouseObject


class Space(WarehouseObject):
        
    def __str__(self):
        return "."
    
    def __repr__(self):
        return self.__str__()

    def push(self, direction):
        return True