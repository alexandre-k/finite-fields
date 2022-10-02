
class FieldElement:
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            raise ValueError(f'Num {num} not in field range 0 to {prime - 1}')
        self.num = num
        self.prime = prime

    def __repr__(self):
        return f'FieldElement_{self.prime}({self.num})'

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __neq__(self, other):
        return not (self == other)

    def __add__(self, other):
        return self.__class__((self.num + other.num) % self.prime, self.prime)

    def __sub__(self, other):
        return self.__class__((self.num - other.num) % self.prime, self.prime)

    def __mul__(self, other):
        self._check_other(other)
        return self.__class__((self.num * other.num) % self.prime, self.prime)

    def __rmul__(self, coef):
        return self.__class__(num=(self.num * coef) % self.prime, prime=self.prime)

    def __pow__(self, exponent):
        if not isinstance(exponent, int):
            raise ValueError('Exponent needs to be an integer.')
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__((num) % self.prime, self.prime)

    def __truediv__(self, other):
        self._check_other(other)
        return self.__class__(self.num * pow(other.num, self.prime - 2, self.prime) % self.prime, self.prime)

    def _check_other(self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot add 2 numbers in different Fields.')


primes = [7, 11, 17, 31]

for p in primes:
    print([pow(s, p-1, p) % p for s in range(1, p)])
