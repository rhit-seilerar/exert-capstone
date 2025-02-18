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
        ('optional', ''),
        ('optional', 'defined(TEST)'),
        ('any', {
            DefOption([('identifier', 'a'), ('identifier', 'b')]),
            DefOption([('any', {
                DefOption([])
            })])
        }),
        ('any', set())
    ]

    new_tokens = []

    with open('./cache/test-tokenmanager-round-trip', mode = 'bw') as file:
        write_tokens(file, tokens, len(tokens))

    with open('./cache/test-tokenmanager-round-trip', mode = 'br') as file:
        new_tokens = read_tokens(file)

    assert tokens == new_tokens
