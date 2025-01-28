import os
import sys
import glob
from exert.utilities.tokenizer import Tokenizer
from exert.usermode import rules
from exert.utilities.command import run_command

REPO_URL = 'git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git'
SOURCE_PATH = './cache/linux'
PARSE_CACHE = './cache/parsed'

def generate(version):
    switch_to_version(version)
    print('Parsing files...')
    if not os.path.exists(PARSE_CACHE):
        os.mkdir(PARSE_CACHE)
    parse(f'{SOURCE_PATH}/include/uapi/asm-generic/posix_types.h')

def get_files():
    return glob.glob(f'{SOURCE_PATH}/include/linux/**/*.h', recursive = True)

def switch_to_version(version):
    if not os.path.exists(SOURCE_PATH):
        print('Cloning Linux...')
        run_command(f'git clone {REPO_URL} {SOURCE_PATH}', True, True)
    print(f'Checking out version {version}...')
    run_command(f'git checkout v{version}', True, True, './cache/linux')

def parse(filename):
    tokenizer = Tokenizer(filename)
    tokenizer.tokenize()
    print(tokenizer.tokens)
    parser = Parser(tokenizer.tokens, types = {
        '__s8': [rules.Int(size = 1, signed = True)],
        '__s16': [rules.Int(size = 2, signed = True)],
        '__s32': [rules.Int(size = 4, signed = True)],
        '__s64': [rules.Int(size = 8, signed = True)],
        '__u8': [rules.Int(size = 1, signed = False)],
        '__u16': [rules.Int(size = 2, signed = False)],
        '__u32': [rules.Int(size = 4, signed = False)],
        '__u64': [rules.Int(size = 8, signed = False)]
    })
    parser.parse()
    print(parser.types)

class Parser:
    def __init__(self, tokens, types = None):
        self.tokens = tokens
        self.len = len(tokens)
        self.index = 0
        self.types = dict(types) if types else dict()

    def add(self, values, key, value):
        print(f"Parsed '{key}': {value}")
        values[key] = (arr := values.get(key, list()))
        arr.append(value)

    def get(self, values, key):
        arr = values.get(key)
        return rules.Any(list(arr)) if arr else None

    def err(self, message):
        print(message)
        context = self.tokens[self.index-5:self.index+6]
        ctx_str = str(context[0]) if len(context) else ''
        offset = '^'
        for i in range(len(context)-1):
            if context[i+1][0] != 'operator':
                ctx_str += ' '
            if i == 5:
                offset = ' ' * len(ctx_str) + '^'
            ctx_str += context[i+1][1]
        print(ctx_str)
        print(offset)
        return None

    def has_next(self):
        return self.index < self.len

    def bump(self):
        self.index += 1

    def peek(self, offset = 0):
        if self.index + offset < self.len:
            return self.tokens[self.index+offset]
        return None

    def next(self, offset = 0):
        if (token := self.peek(offset)):
            self.bump()
            return token
        return None

    def consume_type(self, typ):
        return self.next() if (token := self.peek()) and token[0] == typ else None

    def consume(self, token):
        if self.peek() == token:
            return self.next()
        return None

    def consume_operator(self, name):
        return self.consume(('operator', name))

    def consume_keyword(self, name):
        return self.consume(('keyword', name))

    def consume_identifier(self, name):
        return self.consume(('identifier', name))

    def consume_terminators(self):
        if not self.consume_operator(';'):
            return False
        while self.consume_operator(';'):
            pass
        return True

    def parse_directives(self):
        if self.peek() != ('operator', '#'):
            return False
        while self.consume(('operator', '#')):
            while self.has_next() and not self.consume_type('newline'):
                self.bump()
        return True

    def parse_identifier(self):
        if (token := self.consume_type('identifier')):
            return token[1]
        return ''

    def parse_primitive_types(self):
        prims = [
            'void', 'char', 'int', 'float', 'double',
            'long', 'short', 'unsigned', 'signed'
        ]
        mods = []
        for _ in range(4):
            tok = self.peek()
            if tok[0] != 'keyword' or tok[1] not in prims:
                break
            mods.append(self.next())

        num_int = mods.count(('keyword', 'int'))
        num_long = mods.count(('keyword', 'long'))
        num_short = mods.count(('keyword', 'short'))
        num_unsigned = mods.count(('keyword', 'unsigned'))
        num_signed = mods.count(('keyword', 'signed'))

        if len(mods) == 0:
            return None

        if mods.count(('keyword', 'void')):
            assert len(mods) == 1, f"[Parser][PrimitiveTypes] Unknown void type '{' '.join(mods)}'"
            return rules.Rule()

        if mods.count(('keyword', 'char')):
            valid = len(mods) == 1 or len(mods) == 2 and (num_signed or num_unsigned)
            assert valid, f"[Parser][PrimitiveTypes] Unknown char type '{' '.join(mods)}'"
            return rules.Int(size = 1, signed = num_signed)

        if mods.count(('keyword', 'float')):
            assert len(mods) == 1, f"[Parser][PrimitiveTypes] Unknown float type '{' '.join(mods)}'"
            assert False, '[Parser][PrimitiveTypes] Floats are not yet handled'

        if mods.count(('keyword', 'double')):
            valid = len(mods) == 1 or len(mods) == 2 and num_long
            assert valid, f"[Parser][PrimitiveTypes] Unknown double type '{' '.join(mods)}'"
            assert False, '[Parser][PrimitiveTypes] Doubles are not yet handled'

        valid_type = num_int <= 1
        valid_sign = num_unsigned + num_signed <= 1
        valid_size = (num_short == 1 and not num_long) or (not num_short and num_long <= 2)
        valid_count = num_int + num_unsigned + num_signed + num_short + num_long == len(mods)
        valid = valid_type and valid_sign and valid_size and valid_count
        assert valid, f"[Parser][PrimitiveTypes] Unknown int type '{' '.join(mods)}'"
        size = 2 if num_short else 8 if num_long == 2 else None if num_long == 1 else 4
        return rules.Int(size = size, signed = not num_unsigned)

    def parse_struct(self):
        if not self.consume_keyword('struct'):
            return None
        name = self.parse_identifier()
        if not self.consume(('operator', '{')):
            assert name, "[Parser][Structs] No identifier for body-less struct"
            return self.get(self.types, name)
        groups = []
        fields = []
        while self.has_next():
            if self.consume_terminators():
                continue
            if self.parse_directives():
                continue
            decls = self.parse_type_declarations()
            if not decls:
                break
            for decl in decls:
                fields.append(rules.Field(decl[0], decl[1]))
        if not self.consume_operator('}'):
            assert False, "[Parser][Structs] Struct body did not close"
        groups.append(rules.FieldGroup(fields))
        return rules.Struct(name, groups)

    def parse_base_type(self):
        if (struct := self.parse_struct()):
            return struct
        # if (union := self.parse_union()):
        #     return union
        # if (enum := self.parse_enum()):
        #     return enum
        if (prim := self.parse_primitive_types()):
            return prim
        if (ident := self.parse_identifier()):
            rule = self.get(self.types, ident)
            assert rule, f"[Parser][BaseTypes] No type found for '{ident}'"
            return rule

    def parse_type_declarations(self):
        def parse_per_ident_type(base_type):
            if self.consume_operator('('):
                assert False, "[Parser][TypeDeclarations] Function pointers not yet implemented"
            while self.consume_operator('*'):
                base_type = rules.Pointer(rule = base_type)
            if not (name := self.parse_identifier()):
                assert False, "[Parser][TypeDeclarations] Expected an identifier here"
            if self.consume_operator('['):
                value = self.consume_type('integer')[1]
                assert value, f"[Parser][TypeDeclarations] Unknown array bounds {self.peek()}"
                if not self.consume_operator(']'):
                    assert False, "[Parser][TypeDeclarations] Array must close"
                base_type = rules.Array(rule = base_type, count_min = value, count_max = value)
            if self.consume_operator('['):
                assert False, "[Parser][TypeDeclarations] Multi-dim arrays not yet supported"
            return (name, base_type)
        if not (base_type := self.parse_base_type()):
            return None
        decls = [parse_per_ident_type(base_type)]
        while self.consume_operator(','):
            decls.append(parse_per_ident_type(base_type))
        if not self.consume_terminators():
            assert False, '[Parser][TypeDeclarations] Type did not terminate'
        return decls

    def parse(self):
        while self.has_next():
            if self.parse_directives():
                continue
            if self.consume_terminators():
                continue
            if self.consume_keyword('typedef'):
                decls = self.parse_type_declarations()
                assert decls, "[Parser] Expected a type declaration after typedef"
                for decl in decls:
                    self.add(self.types, decl[0], decl[1])
                continue
            return self.err('[Parser] Unrecognized syntax, cannot proceed.')

if __name__ == '__main__':
    generate(sys.argv[1])
