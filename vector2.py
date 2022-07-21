__author__ = "Alon B.R."


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_tuple(self) -> tuple:
        return (self.x, self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
