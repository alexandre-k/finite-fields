import pytest
from EllipticCurve import Point


a = 5
b = 7

def test_point_eq():
    p1 = Point(-1, -1, a, b)
    p2 = Point(-1, -1, a, b)
    p3 = Point(18, 77, a, b)

    assert p1 == p2
    assert p2 != p3

    with pytest.raises(ValueError):
        Point(-1, -2, a, b)
        Point(2, 4, a, b)
        Point(5, 7, a, b)

def test_point_addition():
    p1 = Point(-1, -1, a, b)
    p2 = Point(-1, 1, a, b)
    infinity = Point(None, None, a, b)
    assert p1 + infinity == p1
    assert infinity + p1 == p1

def test_point_x1_diff_x2():
    p1 = Point(2, 5, a, b)
    p2 = Point(-1, -1, a, b)
    p3 = p1 + p2
    assert p3.x == 3.0
    assert p3.y == -7.0
