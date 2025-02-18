from exert.parser.definitions import DefOption

TOK_TYPES = [
    'string', 'integer', 'identifier', 'keyword',
    'operator', 'directive', 'optional', 'any',
    'newline'
]

def write_number(file, number, length = 8, signed = False):
    file.write(number.to_bytes(length = length, byteorder = 'little', signed = signed))

def write_string(file, string, sizelength = 4):
    write_number(file, len(string), length = sizelength)
    file.write(string.encode('utf-8'))

def read_number(file, length = 8, signed = False):
    return int.from_bytes(file.read(length), byteorder = 'little', signed = signed)

def read_string(file, sizelength = 4):
    length = read_number(file, length = sizelength)
    return file.read(length).decode('utf-8')

def read_tokens(file):
    tokens = []
    for _ in range(read_number(file)):
        token = None
        tok_type = TOK_TYPES[read_number(file, length = 1)]
        if tok_type == 'string':
            token = (
                tok_type,
                read_string(file),
                read_string(file, sizelength = 1)
            )
        elif tok_type == 'integer':
            token = (
                tok_type,
                read_number(file, length = 9, signed = True),
                read_string(file, sizelength = 1)
            )
        elif tok_type == 'identifier':
            token = (tok_type, read_string(file))
        elif tok_type == 'keyword':
            token = (tok_type, read_string(file, sizelength = 1))
        elif tok_type == 'operator':
            token = (tok_type, read_string(file, sizelength = 1))
        elif tok_type == 'directive':
            token = (tok_type, read_string(file, sizelength = 1))
        elif tok_type == 'optional':
            token = (tok_type, read_string(file, sizelength = 1))
        elif tok_type == 'any':
            options = set()
            for _ in range(read_number(file)):
                options.add(DefOption(read_tokens(file)))
            token = (tok_type, options)
        elif tok_type == 'newline':
            print('Warning: deserializing a newline')
            token = (tok_type, read_string(file, sizelength = 1))
        tokens.append(token)
    return tokens

def write_tokens(file, tokens, count):
    write_number(file, count)
    for i in range(count):
        token = tokens[i]
        write_number(file, TOK_TYPES.index(token[0]), length = 1)
        if token[0] == 'string':
            write_string(file, token[1])
            write_string(file, token[2], sizelength = 1)
        elif token[0] == 'integer':
            write_number(file, token[1], length = 9, signed = True)
            write_string(file, token[2], sizelength = 1)
        elif token[0] == 'identifier':
            write_string(file, token[1])
        elif token[0] == 'keyword':
            write_string(file, token[1], sizelength = 1)
        elif token[0] == 'operator':
            write_string(file, token[1], sizelength = 1)
        elif token[0] == 'directive':
            write_string(file, token[1], sizelength = 1)
        elif token[0] == 'optional':
            write_string(file, token[1])
        elif token[0] == 'any':
            write_number(file, len(token[1]))
            for option in token[1]:
                write_tokens(file, option.tokens, len(option.tokens))
        elif token[0] == 'newline':
            print('Warning: serializing a newline')
            write_string(file, token[1], sizelength = 1)
