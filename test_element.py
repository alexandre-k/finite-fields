import pytest
from FieldElement import FieldElement


def test_init():
    a = FieldElement(1, 7)
    assert a.prime == 7
    assert a.num == 1

    with pytest.raises(ValueError):
        FieldElement(7, 1)

def test_eq():
    res1 = FieldElement(7, 983) == FieldElement(1, 7)
    assert res1 is False
    res2 = FieldElement(7, 983) == FieldElement(7, 983)
    assert res2 is True

def test_neq__():
    res1 = FieldElement(7, 983) != FieldElement(1, 7)
    assert res1 is True
    res2 = FieldElement(7, 983) != FieldElement(7, 983)
    assert res2 is False

def test_add():
    a = FieldElement(7, 13)
    b = FieldElement(12, 13)
    c = FieldElement(6, 13)
    assert a + b == c

def test_sub():
    a = FieldElement(7, 13)
    b = FieldElement(12, 13)
    c = FieldElement(6, 13)
    assert c - a == b

def test_mul():
    eight = FieldElement(8, 19)
    res1 = eight * 17
    assert res1.num == 3
    a = FieldElement(95, 97)
    b = FieldElement(45, 97)
    c = FieldElement(31, 97)
    res2 = a*b*c
    assert res2.num == 23
    a = FieldElement(3, 13)
    b = FieldElement(12, 13)
    c = FieldElement(10, 13)
    res3 = a*b
    assert res3.num == c.num

def test_pow():
    nine = FieldElement(9, 19)
    res = nine ** 12
    assert res.num == 7

def test_truediv():
    two = FieldElement(2, 19)
    seven = FieldElement(7, 19)
    res1 = two / seven
    assert res1.num == 3
    five = FieldElement(5, 19)
    res2 = seven / five
    assert res2.num == 9
    a = FieldElement(7, 13)
    b = FieldElement(8, 13)
    res3 = a**-3
    assert res3.num == b.num
