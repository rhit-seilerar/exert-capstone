import os
import sys
import glob
from exert.parser.tokenizer import Tokenizer
from exert.parser.tokenmanager import tok_str, mk_kw, mk_op, mk_id, TokenManager
from exert.parser.preprocessor import Preprocessor
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
    parser.parse(preprocessor.tokens)

class Parser(TokenManager):
    def __init__(self, types = None):
        super().__init__()
        self.types = types.copy() if types is not None else {}

#     def add(self, values, key, value):
#         values[key] = (arr := values.get(key, list()))
#         arr.append(value)

#     def set(self, values, key, value):
#         values[key] = value

#     def pop(self, values, key):
#         values.pop(key)

#     def get(self, values, key):
#         arr = values.get(key)
#         return rules.Any(list(arr)) if arr else None

#     def has(self, values, key):
#         return key in values

    def unwrap(self, k):
        while isinstance(k, tuple) and len(k) == 3:
            k = k[0](k[1], k[2])
        return k

    def chkpt(self, clause):
        def env():
            index = self.index
            def pop(p, f):
                self.index = index
                return f
            def intl(p, f):
                return clause, p, (pop, p, f)
            return intl
        return env()

    def opt(self, clause):
        def intl(p, f):
            return clause, p, p
        return intl

    def por(self, *clauses):
        def intl(p, f):
            def intl1(p1, f1, rest):
                def nex(p2, f2):
                    return intl1(p2, f2, rest[1:])
                if len(rest) == 0:
                    return f1
                return rest[0], p1, (nex, p1, f1)
            return intl1(p, f, clauses)
        return intl

    def pand(self, *clauses):
        def intl(p, f):
            def intl1(p1, f1, rest):
                def nex(p2, f2):
                    return intl1(p2, f2, rest[1:])
                if len(rest) == 0:
                    return p1
                return rest[0], (nex, p1, f1), f1
            return intl1(p, f, clauses)
        return self.chkpt(intl)

    def check_for_any(self, p, f):
        acc = set()
        if self.peek_type() == 'any':
            # Parse the rest of the file with each option
            anytok = self.next()
            for opt in anytok[2]:
                # Back up state and insert the option
                index = self.index
                self.len += len(opt)
                self.tokens[self.index:self.index] = opt.tokens

                # Try it out
                result = self.unwrap(p)

                # Revert state and remove the option
                self.index = index
                del self.tokens[self.index:self.index+len(opt)]
                self.len -= len(opt)
                acc |= result
            return acc

        # No any here, continue on
        return p

    def tok(self, tok):
        return self.pand(
            self.check_for_any,
            lambda p, f: p if self.peek() == tok else f
        )

    def typ(self, typ):
        return self.pand(
            self.check_for_any,
            lambda p, f: p if self.peek_type() == typ else f
        )

    # ===== Other =====

    def parse_expression(self, p, f):
        return p

    def parse_attribute_specifier_sequence(self, p, f):
        return p

    def parse_declaration(self, p, f):
        return p

    def parse_declarator(self, p, f):
        return p

    def parse_declaration_specifiers(self, p, f):
        return p

    def parse_constant_expression(self, p, f):
        return p

    # ===== A.3.2 Expressions =====

    # ===== A.3.3 Statements =====

    def parse_statement(self, p, f):
        return self.por(
            self.parse_labeled_statement,
            self.parse_unlabeled_statement
        ), p, f

    def parse_unlabeled_statement(self, p, f):
        return self.por(
            self.parse_expression_statement,
            self.pand(
                self.opt(self.parse_attribute_specifier_sequence),
                self.parse_primary_block
            ),
            self.pand(
                self.opt(self.parse_attribute_specifier_sequence),
                self.parse_jump_statement
            )
        ), p, f

    def parse_primary_block(self, p, f):
        return self.por(
            self.parse_compound_statement,
            self.parse_selection_statement,
            self.parse_iteration_statement
        ), p, f

    def parse_secondary_block(self, p, f):
        return self.parse_statement, p, f

    def parse_label(self, p, f):
        return self.por(
            self.pand(
                self.opt(self.parse_attribute_specifier_sequence),
                self.typ('identifier'),
                self.tok(mk_op(':'))
            ),
            self.pand(
                self.opt(self.parse_attribute_specifier_sequence),
                self.tok(mk_kw('case')),
                self.parse_constant_expression,
                self.tok(mk_op(':'))
            ),
            self.pand(
                self.opt(self.parse_attribute_specifier_sequence),
                self.tok(mk_kw('default')),
                self.tok(mk_op(':'))
            )
        ), p, f

    def parse_labeled_statement(self, p, f):
        return self.pand(
            self.parse_label,
            self.parse_statement
        ), p, f

    def parse_compound_statement(self, p, f):
        return self.pand(
            self.tok(mk_op('{')),
            self.opt(self.parse_block_item_list),
            self.tok(mk_op('}'))
        ), p, f

    def parse_block_item_list(self, p, f):
        return self.pand(
            self.parse_block_item,
            self.opt(self.parse_block_item_list)
        ), p, f

    def parse_block_item(self, p, f):
        return self.por(
            self.parse_declaration,
            self.parse_unlabeled_statement,
            self.parse_label
        ), p, f

    def parse_expression_statement(self, p, f):
        return self.pand(
            self.opt(self.pand(
                self.opt(self.parse_attribute_specifier_sequence),
                self.parse_expression
            )),
            self.tok(mk_op(';'))
        ), p, f

    def parse_selection_statement(self, p, f):
        return self.por(
            self.pand(
                self.tok(mk_kw('if')),
                self.tok(mk_op('(')),
                self.parse_expression,
                self.tok(mk_op(')')),
                self.parse_secondary_block,
                self.opt(self.pand(
                    self.tok(mk_kw('else')),
                    self.parse_secondary_block
                ))
            ),
            self.pand(
                self.tok(mk_kw('switch')),
                self.tok(mk_op('(')),
                self.parse_expression,
                self.tok(mk_op(')')),
                self.parse_secondary_block
            )
        ), p, f

    def parse_iteration_statement(self, p, f):
        return self.por(
            self.pand(
                self.tok(mk_kw('while')),
                self.tok(mk_op('(')),
                self.parse_expression,
                self.tok(mk_op(')')),
                self.parse_secondary_block
            ),
            self.pand(
                self.tok(mk_kw('do')),
                self.parse_secondary_block,
                self.tok(mk_kw('while')),
                self.tok(mk_op('(')),
                self.parse_expression,
                self.tok(mk_op(')')),
                self.tok(mk_op(';'))
            ),
            self.pand(
                self.tok(mk_kw('for')),
                self.tok(mk_op('(')),
                self.por(
                    self.parse_declaration,
                    self.opt(self.parse_expression),
                ),
                self.tok(mk_op(';')),
                self.opt(self.parse_expression),
                self.tok(mk_op(';')),
                self.opt(self.parse_expression),
                self.tok(mk_op(')')),
                self.parse_secondary_block
            )
        ), p, f

    def parse_jump_statement(self, p, f):
        return self.por(
            self.pand(self.tok(mk_kw('goto')), self.typ('identifier'),
                self.tok(mk_op(';'))),
            self.pand(self.tok(mk_kw('continue')), self.tok(mk_op(';'))),
            self.pand(self.tok(mk_kw('break')), self.tok(mk_op(';'))),
            self.pand(self.tok(mk_kw('return')), self.opt(self.parse_expression),
                self.tok(mk_op(';')))
        ), p, f

    # ===== A.3.4 External Definitions =====

    def parse_translation_unit(self, p, f):
        return self.pand(
            self.parse_external_declaration,
            self.opt(self.parse_translation_unit)
        ), p, f

    def parse_external_declaration(self, p, f):
        return self.por(
            self.parse_function_definition,
            self.parse_declaration
        ), p, f

    def parse_function_definition(self, p, f):
        return self.pand(
            self.opt(self.parse_attribute_specifier_sequence),
            self.parse_declaration_specifiers,
            self.parse_declarator,
            self.parse_function_body
        ), p, f

    def parse_function_body(self, p, f):
        return self.parse_compound_statement, p, f

    def parse(self, tokens):
        super().reset()
        self.tokens = tokens
        self.len = len(tokens)
        self.outstr = ''

        cont = self.unwrap((self.parse_translation_unit, True, False))
        print(cont)
        print(self.outstr)

if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
