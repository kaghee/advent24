from warehouse.Box import Box


class Robot(Box):
        
    def __str__(self):
        return "@"

    def __repr__(self):
        return self.__str__()
