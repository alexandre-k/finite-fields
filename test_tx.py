from Transaction import Tx


def test_parse():
    with open('test_tx.txt', 'r') as t:
        assert Tx.parse(t) == {'version': 1 }
