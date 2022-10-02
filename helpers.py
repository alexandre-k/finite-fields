from hashlib import sha256, new

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def encode_base58(s):
    count = 0
    # count 0s on front
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result

def encode_base58_checksum(b):
    return encode_base58(b + sha256(b).digest()[:4])

def hash160(s):
    return new('ripemd160', sha256(s).digest()).digest()

def little_endian_to_int(b):
    return int.from_bytes(b, 'little')

def int_to_little_endian(i, length):
    return int.to_bytes(length, 'little')
