import pytest
from EllipticCurveCryptography import (
    S256Point,
    N,
    G,
    doubleSHA256,
    PrivateKey,
    Signature)
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

# def test_s256_point():
#     # private key
#     e = int.from_bytes(doubleSHA256(b'secret'), 'big')
#     z = int.from_bytes(doubleSHA256(b'message'), 'big')
#     k = 1234567890
#     r = (k*G).x.num
#     k_inv = pow(k, N-2, N)
#     s = (z+r*e) * k_inv % N
#     point = e*G
#     # TODO
#     assert point == ""
#     assert hex(z) == ""
#     assert hex(e) == ""
#     assert hex(s) == ""

def test_sec():
    private_key = PrivateKey(5000)
    assert private_key.secret == 5000
    assert private_key.point.x.num == 0xffe558e388852f0120e46af2d1b370f85854a8eb0841811ece0e3e03d282d57c
    assert private_key.point.y.num == 0x315dc72890a4f10a1481c031b03b351b0dc79901ca18a00cf009dbdb157a1d10
    assert private_key.point.sec(compressed=False).hex() == '04ffe558e388852f0120e46af2d1b370f85854a8eb0841811ece0e3e03d282d57c315dc72890a4f10a1481c031b03b351b0dc79901ca18a00cf009dbdb157a1d10'

    private_key = PrivateKey(0xdeadbeef12345)
    assert private_key.point.sec(compressed=False).hex() == '04d90cd625ee87dd38656dd95cf79f65f60f7273b67d3096e68bd81e4f5342691f842efa762fd59961d0e99803c61edba8b3e3f7dc3a341836f97733aebf987121'

    private_key = PrivateKey(2018**5)
    expected_y = private_key.point.y.num
    assert private_key.point.sec(compressed=False).hex() == '04027f3da1918455e03c46f659266a1bb5204e959db7364d2f473bdf8f0a13cc9dff87647fd023c13b4a4994f17691895806e1b40b57f4fd22581a4f46851f3b06'

    assert len(private_key.point.sec(compressed=False).hex()) == 130
    assert len(private_key.point.sec().hex()) == 66
    assert private_key.point.sec().hex() == '02027f3da1918455e03c46f659266a1bb5204e959db7364d2f473bdf8f0a13cc9d'
    x = bytes.fromhex('02027f3da1918455e03c46f659266a1bb5204e959db7364d2f473bdf8f0a13cc9d')
    assert private_key.point.parse(x).y.num == expected_y

def test_der():
    r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
    s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
    sig = Signature(r, s)
    assert sig.der().hex() == '3045022037206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c60221008ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec'

def test_address():
    assert PrivateKey(5000).point.address() == '15A8MkDwDQg7BnD6iqMFeeSAM3VVoNMKnp'
    assert PrivateKey(2020**5).point.address() == '19JYTuj9fg6aeS7apjuDpJoN9g7Y6kYwXZ'
    assert PrivateKey(0x12345deadbeef).point.address() == '1F1Pn2y6pDb68E5nYJJeba4TLg2U9QHEgK'

def test_wif():
    assert PrivateKey(5000).wif() == 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgd9M7rFUqyEBAPBYN'
    assert PrivateKey(2020**5).wif() == 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjisvWR8hVo4BoghwjX'
    assert PrivateKey(0x12345deadbeef).wif() == 'KwDiBf89QgGbjEhKnhXJuH7LrciVrZi3qYjgePaN7fzA6Jqng6EW'

