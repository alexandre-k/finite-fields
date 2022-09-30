
class FieldElement:
    """
    Create a field element.
    >>> FieldElement(1, 7)
    FieldElement_7(1)
    >>> FieldElement(7, 1)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "/home/alex/bitcoin/finite-fields/FiniteField.py", line 11, in __init__
        raise ValueError(error)
    ValueError: Num 7 not in field range 0 to 0
    """
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = f'Num {num} not in field range 0 to {prime - 1}'
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        """
        >>> print(FieldElement(1, 7))
        FieldElement_7(1)
        """
        return f'FieldElement_{self.prime}({self.num})'

    def __eq__(self, other):
        """
        >>> FieldElement(7, 983) == FieldElement(1, 7)
        False
        >>> FieldElement(7, 983) == FieldElement(7, 983)
        True
        """
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __neq__(self, other):
        """
        >>> FieldElement(7, 983) != FieldElement(1, 7)
        True
        >>> FieldElement(7, 983) != FieldElement(7, 983)
        False
        """
        if other is None:
            return True
        return self.num != other.num or self.prime != other.prime