from tests import utils
import exert.parser.tokenmanager as tm
from exert.parser.serializer import write_tokens, read_tokens
from exert.parser.definitions import DefOption

def test_roundtrip():
    tokens = [
        ('integer', 10923827539238, 'U'),
        ('integer', -947891238, 'L'),
        ('string', 'ABCDE', ''),
        ('string', 'HIJKL', 'u'),
        ('identifier', 'hello_world'),
        ('operator', '>>>'),
        ('keyword', 'while'),
        ('directive', '#'),
        ('optional', []),
        ('optional', [
            tm.mk_ident('defined'), tm.mk_op('('), tm.mk_ident('TEST'), tm.mk_op(')')]),
        ('any', 'a1', {
            DefOption([('identifier', 'a'), ('identifier', 'b')]),
            DefOption([('any', 'a2', {
                DefOption([])
            })])
        }),
        ('any', 'a3', set())
    ]

    new_tokens = []

    with open('./cache/test-tokenmanager-round-trip', mode = 'bw') as file:
        write_tokens(file, tokens)

    new_tokens = read_tokens('./cache/test-tokenmanager-round-trip')

    assert tokens == new_tokens

def test_invalid():
    with open('./cache/test-tokenmanager-round-trip', mode = 'bw') as file:
        utils.expect_error(lambda: write_tokens(file, [('abc')]), ValueError)
        file.write(b'\x08')
    utils.expect_error(lambda: read_tokens('./cache/test-tokenmanager-round-trip'))
