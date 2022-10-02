from FieldElement import FieldElement
from EllipticCurve import Point
from random import randint
from hashlib import sha256
from helpers import hash160, encode_base58_checksum

Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
P = 2**256 - 2**32 - 977
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

def doubleSHA256(s):
    return sha256(sha256(s).digest()).digest()


class S256Field(FieldElement):

    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=P)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)

    def sqrt(self):
        return self**((P + 1) // 4)


A = 0
B = 7

class S256Point(Point):

    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)

    def __rmul__(self, coef):
        return super().__rmul__(coef % N)

    def verify(self, z, sig):
        return None

    def sec(self, compressed=True):
        if compressed:
            return b'\x02'+ self.x.num.to_bytes(32, 'big') if self.y.num % 2 == 0 else b'\x03' + self.x.num.to_bytes(32, 'big')
        return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')

    def verify(self, z, sig):
        s_inv = pow(sig.s, N - 2, N)
        u = z * s_inv % N
        v = sig.r * s_inv % N
        total = u * G + v * self
        return total.x.num == sig.r

    @classmethod
    def parse(self, sec_bin):
        # case sec is uncompressed
        if sec_bin[0] == 4:
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return S256Point(x=x, y=y)
        # case sec is compressed
        is_even = sec_bin[0] == 2
        x = S256Field(int.from_bytes(sec_bin[1:], 'big'))
        # y^2 = x^3 + 7
        alpha = x**3 + S256Field(B)
        beta = alpha.sqrt()
        if beta.num % 2 == 0:
            even_beta = beta
            odd_beta = S256Field(P - beta.num)
        else:
            even_beta = S256Field(P - beta.num)
            odd_beta = beta
        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta)

    def hash160(self, compressed=True):
        return hash160(self.sec(compressed))

    def address(self, compressed=True, testnet=False):
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)

G = S256Point(Gx, Gy)

class Signature:

    def __init__(self, r, s):
        # x coordinate of kG
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature(:{x},{:x})'.format(self.r, self.s)

    def der(self):
        rbin = self.r.to_bytes(32, 'big')
        rbin = rbin.lstrip(b'\x00')
        # check high 1 or 0
        if rbin[0] & 0x80:
            rbin = b'\x00' + rbin
        result = bytes([2, len(rbin)]) + rbin
        sbin = self.s.to_bytes(32, 'big')
        if sbin[0] & 0x80:
            sbin = b'\x00' + sbin
        result += bytes([2, len(sbin)]) + sbin
        return bytes([0x30, len(result)]) + result

class PrivateKey:

    def __init__(self, secret):
        self.secret = secret
        self.point = secret * G

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        k = randint(0, N)
        r = (k*G).x.num
        k_inv = pow(k, N-2, N)
        s = (z + r*self.secret) * k_inv % N
        if s > N/2:
            s = N - s
        return Signature(r, s)

    def deterministic_k(self, z):
        # RFC 6979
        k = b'\x00'
        v = b'\x01'
        if z > N:
            z -= N
        z_bytes = z.to_bytes(32, 'big')
        secret_bytes = self.secret.to_bytes(32, 'big')
        s256 = hashlib.sha256
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, 'big')
            if candidate >= 1 and candidate < N:
                return candidate
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()

    def wif(self, compressed=True, testnet=False):
        secret_bytes = self.secret.to_bytes(32, 'big')
        prefix = b'\xef ' if testnet else b'\x80'
        suffix = b'\x01' if compressed else b'\x01'
        return encode_base58_checksum(prefix + secret_bytes + suffix)







# P -> public key, coordinate (x, y), x and y being 256 bit numbers
# e -> private key, 256 bit number
# P = e * G
