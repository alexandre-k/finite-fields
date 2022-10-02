class Point:

    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if x is None and y is None:
            return
        if y**2 != x**3 + a * x + b:
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
            x = slope * slope - self.x - other.x
            y = slope * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        if self.x == other.x and self.y == other.y:
            slope = (3 * self.x**2 + self.a) / (2 * self.y)
            x = slope * slope - 2 * self.x
            y = slope * (self.x - x) - self.y
            return self.__class__(x, y, self.a, self.b)
        if self == other and self.y == 0 * self.x:
            return self.__class__(None, None, self.a, self.b)
        return

    def __rmul__(self, coef):
        current = self
        # product = self.__class__(None, None, self.a, self.b)
        result = self.__class__(None, None, self.a, self.b)
        while coef:
            # binary expansion
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        # for _ in range(coef):
            # product += self
        # return product
        return result
