import os
import sys
import glob
from exert.utilities.tokenizer import Tokenizer
from exert.utilities.tokenmanager import TokenManager
from exert.utilities.preprocessor import Preprocessor
from exert.usermode import rules
from exert.utilities.command import run_command

REPO_URL = 'git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git'
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
    if not os.path.exists(SOURCE_PATH):
        print('Cloning Linux...')
        run_command(f'git clone {REPO_URL} {SOURCE_PATH}', True, True)
    print(f'Checking out version {version}...')
    run_command(f'git checkout v{version}', True, True, './cache/linux')

def parse(filename, arch):
    tokenizer = Tokenizer()

    preprocessor = Preprocessor(
        tokenizer,
        includes = [
            f'{SOURCE_PATH}/include/',
            f'{SOURCE_PATH}/include/uapi/',
            f'{SOURCE_PATH}/arch/{arch}/include/',
            f'{SOURCE_PATH}/arch/{arch}/include/uapi/'
        ]
    )
    preprocessor.preprocess(f'#include "{filename}"')
    print(str(preprocessor))
    # parser = Parser(
    #     Preprocessor(
    #         Tokenizer(),
    #         includes = [
    #             f'{SOURCE_PATH}/include/',
    #             f'{SOURCE_PATH}/include/uapi/',
    #             f'{SOURCE_PATH}/arch/{arch}/include/',
    #             f'{SOURCE_PATH}/arch/{arch}/include/uapi/'
    #         ]
    #     ),
    #     types = {
    #         '__s8': [rules.Int(size = 1, signed = True)],
    #         '__s16': [rules.Int(size = 2, signed = True)],
    #         '__s32': [rules.Int(size = 4, signed = True)],
    #         '__s64': [rules.Int(size = 8, signed = True)],
    #         '__u8': [rules.Int(size = 1, signed = False)],
    #         '__u16': [rules.Int(size = 2, signed = False)],
    #         '__u32': [rules.Int(size = 4, signed = False)],
    #         '__u64': [rules.Int(size = 8, signed = False)]
    #     },
    #     definitions = {
    #         '__signed': [[('keyword', 'signed')]],
    #         '__signed__': [[('keyword', 'signed')]]
    #     }
    # )
    # parser.parse(filename)
    # print('================ TYPES ================')
    # print(parser.types)
    # print('================ DEFINITIONS ================')
    # print(parser.preprocessor.definitions)
    # print('================ UNRESOLVED ================')
    # print(parser.unresolved)

class Parser(TokenManager):
    def __init__(self, preprocessor, types = None, definitions = None):
        super().__init__()
        self.preprocessor = preprocessor
        self.directive_nesting_level = 0
        self.resolved_nesting_level = 0
        self.definitions = definitions.copy() if definitions is not None else dict()
        self.types = types.copy() if types is not None else dict()
        self.unresolved = set()

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

    def is_defined(self, key):
        return self.definitions.get(key) or self.types.get(key)

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
            # if self.parse_directives():
            #     continue
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
        self.directive_nesting_level = 0
        self.resolved_nesting_level = 0

        self.preprocessor.preprocess(filename)
        self.tokens = self.preprocessor.tokens
        self.definitions += self.preprocessor.definitions

        # while self.has_next() and not self.has_error:
        #     if self.parse_directives():
        #         continue
        #     if self.consume_terminators():
        #         continue
        #     if self.consume_keyword('typedef'):
        #         decls = self.parse_type_declarations()
        #         if not decls:
        #             return self.err("Expected a type declaration after typedef")
        #         for decl in decls:
        #             self.add(self.types, decl[0], decl[1])
        #         continue
        #     return self.err('Unrecognized syntax, cannot proceed.')
        # if self.directive_nesting_level != 0:
        #     return self.err('Mismatched #if/#endif pairs')

if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
