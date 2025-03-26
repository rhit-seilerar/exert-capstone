import os
import sys
import glob
from exert.parser.tokenizer import Tokenizer
from exert.parser.tokenmanager import TokenManager
from exert.parser.preprocessor import Preprocessor
from exert.parser import serializer
from exert.usermode import rules
from exert.utilities.command import run_command

REPO_URL = 'git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git'
VERSION_PATH = './cache/linux-version.txt'
SOURCE_PATH = './cache/linux'
PARSE_CACHE = './cache/parsed'

def generate(version, arch):
    switch_to_version(version)
    print('Parsing files...')
    if not os.path.exists(PARSE_CACHE):
        os.mkdir(PARSE_CACHE)
    parse(f'{SOURCE_PATH}/include/linux/sched/prio.h', arch)

def get_files():
    return glob.glob(f'{SOURCE_PATH}/include/linux/**/*.h', recursive = True)

def switch_to_version(version):
    old_version = None
    try:
        with open(VERSION_PATH, 'r', encoding = 'utf-8') as file:
            old_version = file.read()
    except FileNotFoundError:
        pass
    if old_version != version:
        with open(VERSION_PATH, 'w', encoding = 'utf-8') as file:
            file.write(version)
        print(f'Checking out linux v{version}')
        run_command(f'git clone --depth 1 {REPO_URL} -b v{version} {SOURCE_PATH}')

SOURCE = """
#include <linux/types.h>
"""

PREPROCESSOR_CACHE = './cache/linux-preprocessor'

def parse(filename, arch):
    tokenizer = Tokenizer()

    preprocessor = Preprocessor(
        tokenizer,
        64, #TODO bitsize
        includes = [
            f'{SOURCE_PATH}/include/',
            f'{SOURCE_PATH}/arch/{arch}/include/',
            lambda path: f'{SOURCE_PATH}/include/asm-generic/{path[4:]}'
                if path.startswith('asm/') else None
        ],
        defns = {
            '__signed__': 'signed',
            '__extension__': ''
        }
    )
    preprocessor.preprocess(SOURCE, PREPROCESSOR_CACHE, False)
    preprocessor.load(PREPROCESSOR_CACHE)
    print(str(preprocessor))

    parser = Parser()
    parser.parse(PREPROCESSOR_CACHE)

class Parser(TokenManager):
    def __init__(self, types = None):
        super().__init__()
        self.types = types.copy() if types is not None else {}

    def add(self, values, key, value):
        values[key] = (arr := values.get(key, list()))
        arr.append(value)

    def set(self, values, key, value):
        values[key] = value

    def pop(self, values, key):
        values.pop(key)

    def get(self, values, key):
        arr = values.get(key)
        return rules.Any(list(arr)) if arr else None

    def has(self, values, key):
        return key in values

    def consume_terminators(self):
        if not self.consume_operator(';'):
            return False
        while self.consume_operator(';'):
            pass
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
            if len(mods) != 1:
                return self.err(f"Unknown void type '{' '.join(mods)}'")
            return rules.Rule()

        if mods.count(('keyword', 'char')):
            if not (len(mods) == 1 or len(mods) == 2 and (num_signed or num_unsigned)):
                return self.err(f"Unknown char type '{' '.join(mods)}'")
            return rules.Int(size = 1, signed = num_signed)

        if mods.count(('keyword', 'float')):
            if len(mods) != 1:
                return self.err(f"Unknown float type '{' '.join(mods)}'")
            return self.err('Floats are not yet handled')

        if mods.count(('keyword', 'double')):
            if not (len(mods) == 1 or len(mods) == 2 and num_long):
                return self.err(f"Unknown double type '{' '.join(mods)}'")
            return self.err('Doubles are not yet handled')

        valid_type = num_int <= 1
        valid_sign = num_unsigned + num_signed <= 1
        valid_size = (num_short == 1 and not num_long) or (not num_short and num_long <= 2)
        valid_count = num_int + num_unsigned + num_signed + num_short + num_long == len(mods)
        if not (valid_type and valid_sign and valid_size and valid_count):
            return self.err(f"Unknown int type '{' '.join(mods)}'")
        size = 2 if num_short else 8 if num_long == 2 else None if num_long == 1 else 4
        return rules.Int(size = size, signed = not num_unsigned)

    def parse_struct(self):
        if not self.consume_keyword('struct'):
            return None
        name = self.parse_identifier()
        if not self.consume(('operator', '{')):
            if not name:
                return self.err("No identifier for body-less struct")
            return self.get(self.types, name)
        groups = []
        fields = []
        while self.has_next():
            if self.consume_terminators():
                continue
            decls = self.parse_type_declarations()
            if not decls:
                break
            for decl in decls:
                fields.append(rules.Field(decl[0], decl[1]))
        if not self.consume_operator('}'):
            return self.err("Struct body did not close")
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
            if not rule:
                return self.err(f"No type found for '{ident}'")
            return rule

    def parse_type_declarations(self):
        def parse_per_ident_type(base_type):
            if self.consume_operator('('):
                #TODO
                return self.err("Function pointers not yet implemented")
            while self.consume_operator('*'):
                base_type = rules.Pointer(rule = base_type)
            if not (name := self.parse_identifier()):
                return self.err("Expected an identifier here")
            if self.consume_operator('['):
                value = self.consume_type('integer')[1]
                if not value:
                    return self.err(f"Unknown array bounds {self.peek()}")
                if not self.consume_operator(']'):
                    return self.err("Array must close")
                base_type = rules.Array(rule = base_type, count_min = value, count_max = value)
            if self.consume_operator('['):
                #TODO
                return self.err("Multi-dimensional arrays not yet supported")
            return (name, base_type)
        if not (base_type := self.parse_base_type()):
            return None
        decls = [parse_per_ident_type(base_type)]
        while self.consume_operator(','):
            decls.append(parse_per_ident_type(base_type))
        if not self.consume_terminators():
            return self.err('Type did not terminate')
        return decls

    def parse(self, filename):
        super().reset()
        tokens = serializer.read_tokens(filename)
        while self.has_next() and not self.has_error:
            if self.consume_terminators():
                continue
            if self.consume_keyword('typedef'):
                decls = self.parse_type_declarations()
                if not decls:
                    return self.err("Expected a type declaration after typedef")
                for decl in decls:
                    self.add(self.types, decl[0], decl[1])
                continue
            return self.err('Unrecognized syntax, cannot proceed.')

if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
