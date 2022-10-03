import requests
from io import BytesIO
from hashlib import sha256
from helpers import (int_to_little_endian,
                     little_endian_to_int,
                     read_varint,
                     read_stream,
                     encode_varint)
from script import Script


class Tx:

    def __init__(self, version, tx_ins = [], tx_outs = [], locktime = 0xff, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
        self.testnet = testnet

    def __repr__(self):
        tx_ins = ''.join(list(self.tx_ins.map(lambda tx: tx.__repr__() + '\n')))
        tx_outs = ''.join(list(self.tx_outs.map(lambda tx: tx.__repr__() + '\n')))
        return f'tx: {self.id()}\nversion: {self.version}\ntx_ins: {tx_ins}\ntx_outs: {tx_outs}\nlocktime: {self.locktime}'

    def id(self):
        return self.hash().hex()

    def hash(self):
        return sha256(self.serialize()).digest()[::-1]

    @classmethod
    def parse(cls, stream):
        version = read_stream(stream, 8)
        print(stream, version)

        inputs = read_varint(stream)
        tx_ins = [TxIn.parse(stream) for _ in range(inputs)]
        print(tx_ins[1].prev_tx)
        print(tx_ins[1].script_sig)

        outputs = read_varint(stream)
        tx_outs = [TxOut.parse(stream) for _ in range(outputs)]

        locktime = read_stream(stream, 4)

        return cls(version, tx_ins, tx_outs, locktime)

    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))
        for tx_in in self.tx_ins:
            result += tx_in.serialize()
        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()
        result += int_to_little_endian(self.locktime, 4)
        return result

class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index
        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig
        self.sequence = sequence

    def __repr__(self):
        return f'{self.prev_tx.hex()}:{self.prev_index}'

    @classmethod
    def parse(cls, stream):
        prev_tx = stream.read(32)[::-1]
        prev_index = read_stream(stream, 4)
        script_sig = Script.parse(stream)
        sequence = read_stream(stream, 4)
        return cls(prev_tx, prev_index, script_sig, sequence)

    def serialize(self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result

    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    def value(self, testnet=False):
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].amount

    def script_pubkey(self, testnet=False):
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_index].script_pubkey


class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return f'{self.amount}:{self.script_pubkey}'

    @classmethod
    def parse(cls, stream):
        amount = read_stream(stream, 8)
        script_pubkey = Script.parse(stream)
        return cls(amount, script_pubkey)

    def serialize(self):
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result


class TxFetcher:
    cache = {}

    @classmethod
    def get_url(cls, testnet=False):
        if testnet:
            return 'http://testnet.programmingbitcoin.com'
        else:
            return 'http://mainnet.programmingbitcoin.com'

    @classmethod
    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cls.cache):
            url = f'{cls.get_url(testnet)}/tx/{tx_id}.hex'
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError(f'Unexpected response: {response.text}')
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
                tx.locktime = little_endian_to_int(raw[-4:])
            else:
                tx = Tx.parse(BytesIO(raw), testnet=testnet)
            if tx.id() != tx_id:
                raise ValueError(f'Not the same id: {tx.id()} vs {tx_id}')
        cls.cache[tx_id].testnet = testnet
        return cls.cache[tx_id]
