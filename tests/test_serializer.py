from exert.parser.serializer import write_tokens, read_tokens
from exert.parser.defoption import DefOption
from exert.utilities.types.global_types import TokenType
from tests import utils

def test_roundtrip() -> None:
    tokens: list[TokenType] = [
        ('integer', 10923827539238, 'U'),
        ('integer', -947891238, 'L'),
        ('string', 'ABCDE', ''),
        ('string', 'HIJKL', 'u'),
        ('identifier', 'hello_world'),
        ('operator', '>>>'),
        ('keyword', 'while'),
        ('directive', '#'),
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

def test_invalid() -> None:
    with open('./cache/test-tokenmanager-round-trip', mode = 'bw') as file:
        utils.expect_error(lambda: write_tokens(file, [('abc')]), ValueError) # type: ignore
        file.write(b'\x08')
    utils.expect_error(lambda: read_tokens('./cache/test-tokenmanager-round-trip'))
