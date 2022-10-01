import pytest
from EllipticCurve import Point
from FieldElement import FieldElement

def test_on_curve():
    prime = 223
    a = FieldElement(num=0, prime=prime)
    b = FieldElement(num=7, prime=prime)
    x = FieldElement(num=192, prime=prime)
    y = FieldElement(num=105, prime=prime)
    p1 = Point(x, y, a, b)
    on_curve_points = [(192, 105), (17, 56), (1, 193)]
    not_on_curve_points = [(200, 119), (42, 99)]
    for x, y in on_curve_points:
        c_x = FieldElement(x, prime)
        c_y = FieldElement(y, prime)
        p2 = Point(c_x, c_y, a, b)
        assert p2.x is not None

    for x, y in not_on_curve_points:
        c_x = FieldElement(x, prime)
        c_y = FieldElement(y, prime)
        with pytest.raises(ValueError):
            Point(c_x, c_y, a, b)

def test_addition_points_on_curve():
    prime = 223
    a = FieldElement(num=0, prime=prime)
    b = FieldElement(num=7, prime=prime)
    x1 = FieldElement(num=192, prime=prime)
    y1 = FieldElement(num=105, prime=prime)
    x2 = FieldElement(num=17, prime=prime)
    y2 = FieldElement(num=56, prime=prime)
    p1 = Point(x1, y1, a, b)
    p1 = Point(x2, y2, a, b)
    p3 = p1 + p1
    expected = Point(FieldElement(13, prime), FieldElement(190, prime), a, b)
    assert p3.x.num == expected.x.num
    assert p3.y.num == expected.y.num

def test_add_points():
    prime = 223
    a = FieldElement(num=0, prime=prime)
    b = FieldElement(num=7, prime=prime)
    p1_points = [(170, 142), (47, 71), (143, 98)]
    p2_points = [(60, 139), (17, 56), (76, 66)]
    expected = [(220, 181), (215, 68), (47, 71)]
    for idx, (p1, p2) in enumerate(zip(p1_points, p2_points)):
        x1 = FieldElement(num=p1[0], prime=prime)
        y1 = FieldElement(num=p1[1], prime=prime)
        x2 = FieldElement(num=p2[0], prime=prime)
        y2 = FieldElement(num=p2[1], prime=prime)
        point1 = Point(x1, y1, a, b)
        point2 = Point(x2, y2, a, b)
        point3 = point1 + point2
        assert point3.x.num == expected[idx][0]
        assert point3.y.num == expected[idx][1]

def test_mul_with_addition():
    prime = 223
    a = FieldElement(num=0, prime=prime)
    b = FieldElement(num=7, prime=prime)
    p1_points = [(192, 105), (143, 98), (47, 71), (47, 71), (47, 71), (47, 71)]
    p1_multiplicator = [2, 2, 2, 4, 8, 21]
    expected = [(66, 111), (8, 96), (194, 51), (126, 127), (194, 51), (116, 55)]
    for idx, (p1, multiplicator) in enumerate(zip(p1_points, p1_multiplicator)):
        x1 = FieldElement(num=p1[0], prime=prime)
        y1 = FieldElement(num=p1[1], prime=prime)
        point1 = Point(x1, y1, a, b)
        for _ in range(multiplicator):
            point1 += point1
        assert point1.x.num == expected[idx][0]
        assert point1.y.num == expected[idx][1]


def test_group_order_infinity():
    prime = 223
    a = FieldElement(num=0, prime=prime)
    b = FieldElement(num=7, prime=prime)
    x = FieldElement(num=15, prime=prime)
    y = FieldElement(num=86, prime=prime)
    p = Point(x, y, a, b)
    result = 7 * p
    assert result.x == None
    assert result.y == None
