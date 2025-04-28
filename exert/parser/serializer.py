from io import BufferedReader, BufferedWriter
from exert.parser.definitions import DefOption
from exert.utilities.types.global_types import TokenType

TOK_TYPES: list[str] = [
    'string', 'integer', 'identifier', 'keyword',
    'operator', 'directive', 'any'
]

def write_number(file: BufferedWriter, number: int, length: int = 8, signed: bool = False) -> None:
    file.write(number.to_bytes(length = length, byteorder = 'little', signed = signed))

def write_string(file: BufferedWriter, string: str, sizelength: int = 4) -> None:
    write_number(file, len(string), length = sizelength)
    file.write(string.encode('utf-8'))

def read_number(file: BufferedReader, length: int = 8, signed: bool = False) -> int:
    return int.from_bytes(file.read(length), byteorder = 'little', signed = signed)

def read_string(file: BufferedReader, sizelength: int = 4) -> str:
    length = read_number(file, length = sizelength)
    return file.read(length).decode('utf-8')

def read_token(file: BufferedReader) -> TokenType:
    tok_id = read_number(file, length = 1)
    if tok_id < len(TOK_TYPES):
        tok_type = TOK_TYPES[tok_id]
        if tok_type == 'string':
            return (
                tok_type,
                read_string(file),
                read_string(file, sizelength = 1)
            )
        if tok_type == 'integer':
            return (
                tok_type,
                read_number(file, length = 9, signed = True),
                read_string(file, sizelength = 1)
            )
        if tok_type == 'identifier':
            return (tok_type, read_string(file))
        if tok_type == 'keyword':
            return (tok_type, read_string(file, sizelength = 1))
        if tok_type == 'operator':
            return (tok_type, read_string(file, sizelength = 1))
        if tok_type == 'directive':
            return (tok_type, read_string(file, sizelength = 1))
        if tok_type == 'any':
            name = read_string(file)
            options = set()
            for _ in range(read_number(file)):
                option_tokens = []
                for _ in range(read_number(file)):
                    option_tokens.append(read_token(file))
                options.add(DefOption(option_tokens))
            return (tok_type, name, options)
    assert False

def read_tokens(path: str) -> list[TokenType]:
    tokens = []
    with open(path, 'rb') as file:
        file.seek(0, 2)
        end = file.tell()
        file.seek(0)
        while file.tell() < end:
            tokens.append(read_token(file))
        file.close()
    return tokens

def write_tokens(file: BufferedWriter, tokens: list[TokenType]) -> None:
    for token in tokens:
        write_number(file, TOK_TYPES.index(token[0]), length = 1)
        if token[0] == 'string':
            assert isinstance(token[1], str)
            write_string(file, token[1])
            assert len(token) > 2
            assert isinstance(token[2], str)
            write_string(file, token[2], sizelength = 1)
        elif token[0] == 'integer':
            assert isinstance(token[1], int)
            write_number(file, token[1], length = 9, signed = True)
            assert len(token) > 2
            assert isinstance(token[2], str)
            write_string(file, token[2], sizelength = 1)
        elif token[0] == 'identifier':
            assert isinstance(token[1], str)
            write_string(file, token[1])
        elif token[0] == 'keyword':
            assert isinstance(token[1], str)
            write_string(file, token[1], sizelength = 1)
        elif token[0] == 'operator':
            assert isinstance(token[1], str)
            write_string(file, token[1], sizelength = 1)
        elif token[0] == 'directive':
            assert isinstance(token[1], str)
            write_string(file, token[1], sizelength = 1)
        elif token[0] == 'any':
            assert isinstance(token[1], str)
            write_string(file, token[1])
            assert len(token) > 2
            write_number(file, len(token[2]))
            for option in token[2]:
                assert isinstance(option, DefOption)
                write_number(file, len(option.tokens))
                write_tokens(file, option.tokens)
