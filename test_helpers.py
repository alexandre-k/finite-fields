from helpers import encode_base58, encode_base58_checksum, hash160
import pytest

def test_base58():
    assert encode_base58(b'00ll') == '2ESfto'
    assert encode_base58(b'0') == 'q'
    assert encode_base58(b'l') == '2s'
    assert encode_base58(bytes.fromhex('7c076ff316692a3d7eb3c3bb0f8b1488cf72e1afcd929e29307032997a838a3d')) == '9MA8fRQrT4u8Zj8ZRd6MAiiyaxb2Y1CMpvVkHQu5hVM6'
    assert encode_base58(bytes.fromhex('eff69ef2b1bd93a66ed5219add4fb51e11a840f404876325a1e8ffe0529a2c')) == '4fE3H2E6XMp4SsxtwinF7w9a34ooUrwWe4WsW1458Pd'
    assert encode_base58(bytes.fromhex('c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6')) == 'EQJsjkd6JaGwxrjEhfeqPenqHwrBmPQZjJGNSCHBkcF7'
    assert encode_base58_checksum(bytes.fromhex('c7207fee197d27c618aea621406f6bf5ef6fca38681d82b2f06fddbdce6feab6')) == '2WhRyzK3iKFveq4hvQ3VR9uau26t6qZCMhADPAVMeMR6S5dV2q'

def test_hash160():
    assert hash160(bytes.fromhex('00')).hex() == '9f7fd096d37ed2c0e3f7f0cfc924beef4ffceb68'
