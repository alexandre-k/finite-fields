class Point:

    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if x is None and y is None:
            return
        if y**2 != x**3 + a * x +b:
            raise ValueError(f'({x}, {y}) are not on the curve.')

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b

    def __neq__(self, other):
        return not (self == other)

    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            raise TypeError(f'Points {self}, {other} are not on the same curve.')
        if self.x is None:
            return other
        if other.x is None:
            return self
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)
        if self.x != other.x:
            slope = (other.y - self.y) / (other.x - self.x)
            x = slope**2 - self.x - other.x
            y = slope * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        return
