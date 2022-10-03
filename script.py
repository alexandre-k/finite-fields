from helpers import (read_stream,
                     read_varint,
                     encode_varint,
                     little_endian_to_int,
                     int_to_little_endian)
from hashlib import sha256, ripemd160


def op_dup(stack):
    if len(stack) < 1:
        return False
    stack.append(stack[-1])
    return True

def op_hash256(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(sha256(element).digest())
    return True

def op_hash160(stack):
    if len(stack) < 1:
        return False
    element = stack.pop()
    stack.append(ripemd160(sha256(sha256(element).digest()).digest()).digest())


OP_CODE_FUNCTIONS = {
    118: op_dup,
    169: op_hash160,
    170: op_hash256
}

class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds

    @classmethod
    def parse(cls, stream):
        length = read_varint(stream)
        cmds = []
        count = 0
        while count < length:
            current = read_stream(stream, 1)
            count += 1
            current_byte = current[0]
            if 1 <= current_byte <= 75:
                n = current_byte
                cmds.append(read_stream(stream, n))
                count += n
            elif current_byte == 76:
                data_length = little_endian_to_int(read_stream(stream, 1))
                cmds.append(read_stream(stream, data_length))
                count += data_length + 1
            elif current_byte == 77:
                data_length = little_endian_to_int(read_stream(stream, 2))
                cmds.append(read_stream(stream, data_length))
                count += data_length + 2
            else:
                op_code = current_byte
                cmds.append(op_code)
        if count != length:
            raise SyntaxError('Parsing script failed')
        return cls(cmds)

    def raw_serialize(self):
        result = b''
        for cmd in self.cmds:
            if type(cmd) == int:
                result += int_to_little_endian(cmd, 1)
            else:
                length = len(cmd)
                if length < 75:
                    result += int_to_little_endian(length, 1)
                elif 75 < length < 0x100:
                    result += int_to_little_endian(76, 1)
                    result += int_to_little_endian(length, 1)
                elif 0x100 < length < 520:
                    result += int_to_little_endian(77, 1)
                    result += int_to_little_endian(length, 2)
                else:
                    raise ValueError('Too long an cmd')
                result += cmd
        return result

    def serialize(self):
        result = self.raw_serialize()
        total = len(result)
        return encode_varint(total) + result
