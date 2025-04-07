import os
import sys
import time
import glob
from typing import Any, Literal, Optional, List
from exert.parser.tokenizer import Tokenizer
from exert.parser.tokenmanager import tok_seq, mk_kw, mk_op, mk_id, TokenManager
from exert.parser.preprocessor import Preprocessor
# from exert.usermode import rules
from exert.utilities.debug import dprint
from exert.utilities.command import run_command

REPO_URL: str = 'git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git'
VERSION_PATH: str = './cache/linux-version.txt'
SOURCE_PATH: str = './cache/linux'
PARSE_CACHE: str = './cache/parsed'

def generate(version: Optional[str], arch: str):
    switch_to_version(version)
    print('Parsing files...')
    if not os.path.exists(PARSE_CACHE):
        os.mkdir(PARSE_CACHE)
    parse(f'{SOURCE_PATH}/include/linux/sched/prio.h', arch)

def get_files() -> List[str]:
    return glob.glob(f'{SOURCE_PATH}/include/linux/**/*.h', recursive = True)

def switch_to_version(version: Optional[str]):
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

SOURCE: Literal['\n#include <linux/types.h>\n'] = """
#include <linux/types.h>
"""

PREPROCESSOR_CACHE: Literal['./cache/linux-preprocessor'] = './cache/linux-preprocessor'

def parse(filename: str, arch: str):
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
    def __init__(self, types: Optional[dict] = None):
        super().__init__()
        self.chkptid = 0
        self.anydepth = 0
        self.in_typedef = False
        self.staged_types = {}
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

    def unwrap(self, k: tuple) -> Any:
        dprint(3, 'unwrap.start')
        while isinstance(k, tuple) and len(k) == 3:
            if self.time + 10 < time.time():
                print("Time's up!")
                break
            dprint(4, '    unwrapping', k[0])
            k = k[0](k[1], k[2])
        dprint(3, 'unwrap.end')
        return k

    def chkpt(self, clause: Any) -> tuple:
        dprint(5, 'chkpt', clause)
        def env(p: Any, f: Any) -> tuple:
            index = self.index
            idt = self.chkptid
            self.chkptid += 1
            dprint(3.5, f'chkpt.env.push({idt}): {index}')
            def pop(p: Any, f: Any) -> Any:
                dprint(3.5, f'chkpt.env.pop({idt}): {self.index} -> {index}')
                self.index = index
                return f
            return clause, p, (pop, p,f)
        return env

    def opt(self, clause: Any) -> tuple:
        dprint(5, 'opt', clause)
        return lambda p, f: (clause, p, p)

    def pnot(self, clause: Any) -> tuple:
        dprint(5, 'pnot', clause)
        return lambda p, f: (clause, p,f)

    def por(self, *clauses: tuple) -> tuple:
        dprint(5, 'por')
        def start(p: Any, f: Any)-> tuple:
            dprint(4, 'por.start')
            def getnext(p1: Any, f1: Any, rest: tuple) -> tuple:
                dprint(5, 'por.getnext')
                def nex(p2: Any, f2: Any)-> tuple:
                    dprint(4, 'por.next')
                    return getnext(p2, f2, rest[1:])
                if len(rest) == 0:
                    return f1
                return rest[0], p1, (nex, p1, f1)
            return getnext(p, f, clauses)
        return start

    def pand(self, *clauses: tuple) -> tuple:
        dprint(5, 'pand', clauses)
        def start(p: Any, f: Any)->tuple:
            dprint(4, 'pand.start')
            def getnext(p1: Any, f1: Any, rest: tuple) -> tuple:
                dprint(5, 'pand.getnext')
                def nex(p2: Any, f2: Any)-> tuple:
                    dprint(4, 'pand.next')
                    return getnext(p2, f2, rest[1:])
                if len(rest) == 0:
                    return p1
                return rest[0], (nex, p1, f1), f1
            return getnext(p, f, clauses)
        return self.chkpt(start)

    def check_for_any(self, p:Any, f:Any) -> Any:
        dprint(4, 'check_for_any')
        if self.peek_type() == 'any':
            dprint(2, f'  Entering({self.anydepth})')
            self.anydepth += 1
            result = False
            # Parse the rest of the file with each option
            anytok = self.peek()
            for opt in anytok[2]:
                # Back up state and insert the option
                index = self.index
                self.len += len(opt) - 1
                self.tokens[index:index+1] = opt.tokens
                dprint(2, '    !!TOKENS!!  ', tok_seq(self.tokens))

                # Try it out
                if self.unwrap((self.check_for_any, p,f)):
                    result = True
                self.index = index
                dprint(2, '    Result:', result)

                # Revert state and remove the option
                self.tokens[index:index+len(opt.tokens)] = [anytok]
                self.len -= len(opt) - 1
            dprint(2, f'  Returning({self.anydepth}): {result}')
            self.anydepth -= 1
            return result
        return p

    def pbump(self, p:Any, f:Any)-> Any:
        dprint(3, 'pbump')
        self.bump()
        return p

    def ptok(self, tok: Any)-> tuple:
        dprint(4, 'ptok')
        def intl(p:Any, f:Any)->tuple:
            dprint(3, 'tok.intl', tok, self.peek())
            if self.peek() == tok:
                return p
            return f
        return lambda p, f: (self.check_for_any, (intl, p, f), f)

    def tok(self, tok: Any)-> tuple:
        dprint(4, 'tok')
        return lambda p, f: (self.ptok(tok), (self.pbump, p, f), f)

    def ptyp(self, typ: tuple)-> tuple:
        dprint(4, 'ptyp')
        def intl(p:Any, f:Any)->Any:
            dprint(3, 'ptyp.intl', typ, self.peek())
            if self.peek_type() == typ:
                return p
            return f
        return lambda p, f: (self.check_for_any, (intl, p,f), f)

    def typ(self, typ: tuple)-> tuple:
        dprint(4, 'typ')
        return lambda p, f: (self.ptyp(typ), (self.pbump, p,f), f)

    # ===== Alternate Spellings & Misc =====

    def parse_alignas(self, p:Any, f:Any)-> tuple:
        dprint(3, 'parse_alignas')
        return self.por(
            self.tok(mk_kw('alignas')),
            self.tok(mk_kw('_Alignas'))
        ), p, f

    def parse_alignof(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_alignof')
        return self.por(
            self.tok(mk_kw('alignof')),
            self.tok(mk_kw('_Alignof'))
        ), p, f

    def parse_bool(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_bool')
        return self.por(
            self.tok(mk_kw('bool')),
            self.tok(mk_kw('_Bool'))
        ), p, f

    def parse_static_assert(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_static_assert')
        return self.por(
            self.tok(mk_kw('static_assert')),
            self.tok(mk_kw('_Static_assert'))
        ), p, f

    def parse_thread_local(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_thread_local')
        return self.por(
            self.tok(mk_kw('thread_local')),
            self.tok(mk_kw('_Thread_local'))
        ), p, f

    def maybe_typedef_name(self, p:Any, f:Any)->tuple:
        dprint(3, 'maybe_typedef_name')
        def addname(p:Any, f:Any)->tuple:
            if self.in_typedef:
                dprint(1.5, f'Staging: {self.peek()[1]}: {1}')
                self.staged_types[self.peek()[1]] = 1
            return p
        return self.ptyp('identifier'), (addname, (self.pbump, p,f), f), f

    def parse_typedef_declarator_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_typedef_declarator_list')
        return self.pand(
            self.parse_declarator,
            self.opt(self.pand(
                self.tok(mk_op(',')),
                self.parse_typedef_declarator_list
            ))
        ), p, f

    def parse_type_specifier_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_type_specifier_list')
        return self.pand(
            self.parse_type_specifier,
            self.opt(self.parse_type_specifier_list)
        ), p, f

    def parse_typedef(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_typedef')
        def enter(p1, f1):
            self.in_typedef = True
            self.staged_types = {}
            return p1
        def commit(p1: Any, f1: Any) -> Any:
            self.in_typedef = False
            self.types.update(self.staged_types)
            dprint(1, f'Adding types: {self.staged_types}')
            return p1
        def rollback(p1: Any, f1: Any) -> Any:
            if self.in_typedef:
                dprint(1, 'Rolling back!')
            self.in_typedef = False
            return f1
        return self.pand(
            self.tok(mk_kw('typedef')),
            enter,
            self.parse_type_specifier_list,
            self.opt(self.parse_attribute_specifier_sequence),
            self.parse_typedef_declarator_list,
            self.tok(mk_op(';'))
        ), (commit, p,f), (rollback, p,f)

    # ===== A.2.5 Constants =====

    def parse_constant(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_constant')
        return self.por(
            self.typ('integer'),
            self.typ('floating'),
            self.parse_enumeration_constant,
            self.typ('character'),
            self.parse_predefined_constant,
        ), p, f

    def parse_enumeration_constant(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_enumeration_constant')
        return self.typ('identifier'), p, f

    def parse_predefined_constant(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_predefined_constant')
        return self.por(
            self.tok(mk_kw('false')),
            self.tok(mk_kw('true')),
            self.tok(mk_kw('nullptr'))
        ), p, f

    # ===== A.3.1 Expressions =====

    def parse_primary_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_primary_expression')
        return self.por(
            self.typ('identifier'),
            self.parse_constant,
            self.typ('string'),
            self.pand(
                self.tok(mk_op('(')),
                self.parse_expression,
                self.tok(mk_op(')'))
            ),
            self.parse_generic_selection
        ), p, f

    def parse_generic_selection(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_generic_selection')
        return self.pand(
            self.tok(mk_kw('_Generic')),
            self.tok(mk_op('(')),
            self.parse_assignment_expression,
            self.tok(mk_op(',')),
            self.parse_generic_assoc_list,
            self.tok(mk_op(')'))
        ), p, f

    def parse_generic_assoc_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_generic_assoc_list')
        return self.pand(
            self.parse_generic_association,
            self.opt(self.pand(
                self.tok(mk_op(',')),
                self.parse_generic_assoc_list
            ))
        ), p, f

    def parse_generic_association(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_generic_association')
        return self.pand(
            self.por(
                self.parse_type_name,
                self.tok(mk_kw('default'))
            ),
            self.tok(mk_op(':')),
            self.parse_assignment_expression
        ), p, f

    def parse_postfix_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_postfix_expression')
        return self.por(
            self.parse_primary_expression,
            self.pand(
                self.parse_postfix_expression,
                self.por(
                    self.pand(
                        self.tok(mk_op('[')),
                        self.parse_expression,
                        self.tok(mk_op(']'))
                    ),
                    self.pand(
                        self.tok(mk_op('(')),
                        self.opt(self.parse_argument_expression_list),
                        self.tok(mk_op(')'))
                    ),
                    self.pand(
                        self.tok(mk_op('.')),
                        self.typ('identifier')
                    ),
                    self.pand(
                        self.tok(mk_op('->')),
                        self.typ('identifier')
                    ),
                    self.tok(mk_op('++')),
                    self.tok(mk_op('--'))
                )
            ),
            self.parse_compound_literal
        ), p, f

    def parse_argument_expression_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_argument_expression_list')
        return self.pand(
            self.parse_assignment_expression,
            self.opt(self.pand(
                self.tok(mk_op(',')),
                self.parse_argument_expression_list
            ))
        ), p, f

    def parse_compound_literal(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_compound_literal')
        return self.pand(
            self.tok(mk_op('(')),
            self.opt(self.parse_storage_class_specifiers),
            self.parse_type_name,
            self.tok(mk_op(')')),
            self.parse_braced_initializer
        ), p, f

    def parse_storage_class_specifiers(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_storage_class_specifiers')
        return self.pand(
            self.parse_storage_class_specifier,
            self.opt(self.parse_storage_class_specifiers)
        ), p, f

    def parse_unary_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_unary_expression')
        return self.por(
            self.parse_postfix_expression,
            self.pand(
                self.tok(mk_op('++')),
                self.parse_unary_expression
            ),
            self.pand(
                self.tok(mk_op('--')),
                self.parse_unary_expression
            ),
            self.pand(
                self.parse_unary_operator,
                self.parse_cast_expression
            ),
            self.pand(
                self.tok(mk_kw('sizeof')),
                self.parse_unary_expression
            ),
            self.pand(
                self.tok(mk_kw('sizeof')),
                self.tok(mk_op('(')),
                self.parse_type_name,
                self.tok(mk_op(')'))
            ),
            self.pand(
                self.parse_alignof,
                self.tok(mk_op('(')),
                self.parse_type_name,
                self.tok(mk_op(')'))
            )
        ), p, f

    def parse_unary_operator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_unary_operator')
        return self.por(
            self.tok(mk_op('&')),
            self.tok(mk_op('*')),
            self.tok(mk_op('+')),
            self.tok(mk_op('-')),
            self.tok(mk_op('~')),
            self.tok(mk_op('!'))
        ), p, f

    def parse_cast_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_cast_expression')
        return self.por(
            self.parse_unary_expression,
            self.pand(
                self.tok(mk_op('(')),
                self.parse_type_name,
                self.tok(mk_op(')')),
                self.parse_cast_expression
            )
        ), p, f

    def parse_multiplicative_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_multiplicative_expression')
        return self.por(
            self.parse_cast_expression,
            self.pand(
                self.parse_multiplicative_expression,
                self.por(
                    self.tok(mk_op('*')),
                    self.tok(mk_op('/')),
                    self.tok(mk_op('%'))
                ),
                self.parse_cast_expression
            )
        ), p, f

    def parse_additive_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_additive_expression')
        return self.por(
            self.parse_multiplicative_expression,
            self.pand(
                self.parse_additive_expression,
                self.por(
                    self.tok(mk_op('+')),
                    self.tok(mk_op('-'))
                ),
                self.parse_multiplicative_expression
            )
        ), p, f

    def parse_shift_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_shift_expression')
        return self.por(
            self.parse_additive_expression,
            self.pand(
                self.parse_shift_expression,
                self.por(
                    self.tok(mk_op('<<')),
                    self.tok(mk_op('>>'))
                ),
                self.parse_additive_expression
            )
        ), p, f

    def parse_relational_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_relational_expression')
        return self.por(
            self.parse_shift_expression,
            self.pand(
                self.parse_relational_expression,
                self.por(
                    self.tok(mk_op('<')),
                    self.tok(mk_op('>')),
                    self.tok(mk_op('<=')),
                    self.tok(mk_op('>='))
                ),
                self.parse_shift_expression
            )
        ), p, f

    def parse_equality_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_equality_expression')
        return self.por(
            self.parse_relational_expression,
            self.pand(
                self.parse_equality_expression,
                self.por(
                    self.tok(mk_op('==')),
                    self.tok(mk_op('!='))
                ),
                self.parse_relational_expression
            )
        ), p, f

    def parse_and_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_and_expression')
        return self.por(
            self.parse_equality_expression,
            self.pand(
                self.parse_and_expression,
                self.tok(mk_op('&')),
                self.parse_equality_expression
            )
        ), p, f

    def parse_exclusive_or_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_exclusive_or_expression')
        return self.por(
            self.parse_and_expression,
            self.pand(
                self.parse_exclusive_or_expression,
                self.tok(mk_op('^')),
                self.parse_and_expression
            )
        ), p, f

    def parse_inclusive_or_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_inclusive_or_expression')
        return self.por(
            self.parse_exclusive_or_expression,
            self.pand(
                self.parse_inclusive_or_expression,
                self.tok(mk_op('|')),
                self.parse_exclusive_or_expression
            )
        ), p, f

    def parse_logical_and_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_logical_and_expression')
        return self.por(
            self.parse_inclusive_or_expression,
            self.pand(
                self.parse_logical_and_expression,
                self.tok(mk_op('&&')),
                self.parse_inclusive_or_expression
            )
        ), p, f

    def parse_logical_or_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_logical_or_expression')
        return self.por(
            self.parse_logical_and_expression,
            self.pand(
                self.parse_logical_or_expression,
                self.tok(mk_op('||')),
                self.parse_logical_and_expression
            )
        ), p, f

    def parse_conditional_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_conditional_expression')
        return self.pand(
            self.parse_logical_or_expression,
            self.opt(self.pand(
                self.tok(mk_op('?')),
                self.parse_expression,
                self.tok(mk_op(':')),
                self.parse_conditional_expression
            ))
        ), p, f

    def parse_assignment_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_assignment_expression')
        return self.por(
            self.parse_conditional_expression,
            self.pand(
                self.parse_unary_expression,
                self.parse_assignment_operator,
                self.parse_assignment_expression
            )
        ), p, f

    def parse_assignment_operator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_assignment_operator')
        return self.por(
            self.tok(mk_op('=')),
            self.tok(mk_op('*=')),
            self.tok(mk_op('/=')),
            self.tok(mk_op('%=')),
            self.tok(mk_op('+=')),
            self.tok(mk_op('-=')),
            self.tok(mk_op('<<=')),
            self.tok(mk_op('>>=')),
            self.tok(mk_op('&=')),
            self.tok(mk_op('^=')),
            self.tok(mk_op('|='))
        ), p, f

    def parse_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_expression')
        return self.pand(
            self.parse_assignment_expression,
            self.opt(self.pand(
                self.tok(mk_op(',')),
                self.parse_expression
            ))
        ), p, f

    def parse_constant_expression(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_constant_expression')
        return self.parse_conditional_expression, p, f

    # ===== A.3.2 Declarations =====

    def parse_declaration(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_declaration')
        return self.por(
            self.parse_typedef,
            self.pand(
                self.parse_declaration_specifiers,
                self.opt(self.parse_init_declarator_list),
                self.tok(mk_op(';'))
            ),
            self.pand(
                self.parse_attribute_specifier_sequence,
                self.parse_declaration_specifiers,
                self.parse_init_declarator_list,
                self.tok(mk_op(';'))
            ),
            self.parse_static_assert_declaration,
            self.parse_attribute_declaration
        ), p, f

    def parse_declaration_specifiers(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_declaration_specifiers')
        return self.pand(
            self.parse_declaration_specifier,
            self.por(
                self.parse_declaration_specifiers,
                self.opt(self.parse_attribute_specifier_sequence)
            )
        ), p, f

    def parse_declaration_specifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_declaration_specifier')
        return self.por(
            self.parse_storage_class_specifier,
            self.parse_type_specifier_qualifier,
            self.parse_function_specifier
        ), p, f

    def parse_init_declarator_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_init_declarator_list')
        return self.pand(
            self.parse_init_declarator,
            self.opt(self.pand(
                self.tok(mk_op(',')),
                self.parse_init_declarator_list
            ))
        ), p, f

    def parse_init_declarator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_init_declarator')
        return self.por(
            self.pand(
                self.parse_declarator,
                self.tok(mk_op('=')),
                self.parse_initializer
            ),
            self.parse_declarator
        ), p, f

    def parse_attribute_declaration(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_attribute_declaration')
        return self.pand(
            self.parse_attribute_specifier_sequence,
            self.tok(mk_op(';'))
        ), p, f

    def parse_storage_class_specifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_storage_class_specifier')
        return self.por(
            self.tok(mk_kw('auto')),
            self.tok(mk_kw('constexpr')),
            self.tok(mk_kw('extern')),
            self.tok(mk_kw('register')),
            self.tok(mk_kw('static')),
            self.parse_thread_local
        ), p, f

    def parse_type_specifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_type_specifier')
        return self.por(
            self.tok(mk_kw('void')),
            self.tok(mk_kw('char')),
            self.tok(mk_kw('short')),
            self.tok(mk_kw('int')),
            self.tok(mk_kw('long')),
            self.tok(mk_kw('float')),
            self.tok(mk_kw('double')),
            self.tok(mk_kw('signed')),
            self.tok(mk_kw('unsigned')),
            self.pand(
                self.tok(mk_kw('_BitInt')),
                self.tok(mk_op('(')),
                self.parse_constant_expression,
                self.tok(mk_op(')'))
            ),
            self.parse_bool,
            self.tok(mk_kw('_Complex')),
            self.tok(mk_kw('_Decimal32')),
            self.tok(mk_kw('_Decimal64')),
            self.tok(mk_kw('_Decimal128')),
            self.parse_atomic_type_specifier,
            self.parse_struct_or_union_specifier,
            self.parse_enum_specifier,
            self.parse_typedef_name,
            self.parse_typeof_specifier
        ), p, f

    def parse_struct_or_union_specifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_struct_or_union_specifier')
        return self.pand(
            self.parse_struct_or_union,
            self.opt(self.parse_attribute_specifier_sequence),
            self.por(
                self.pand(
                    self.opt(self.typ('identifier')),
                    self.tok(mk_op('{')),
                    self.parse_member_declaration_list,
                    self.tok(mk_op('}'))
                ),
                self.typ('identifier')
            )
        ), p, f

    def parse_struct_or_union(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_struct_or_union')
        return self.por(
            self.tok(mk_kw('struct')),
            self.tok(mk_kw('union'))
        ), p, f

    def parse_member_declaration_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_member_declaration_list')
        return self.pand(
            self.parse_member_declaration,
            self.opt(self.parse_member_declaration_list)
        ), p, f

    def parse_member_declaration(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_member_declaration')
        return self.por(
            self.pand(
                self.opt(self.parse_attribute_specifier_sequence),
                self.parse_specifier_qualifier_list,
                self.opt(self.parse_member_declarator_list),
                self.tok(mk_op(';'))
            ),
            self.parse_static_assert_declaration
        ), p, f

    def parse_specifier_qualifier_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_specifier_qualifier_list')
        return self.pand(
            self.parse_type_specifier_qualifier,
            self.por(
                self.parse_specifier_qualifier_list,
                self.opt(self.parse_attribute_specifier_sequence)
            )
        ), p, f

    def parse_type_specifier_qualifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_type_specifier_qualifier')
        return self.por(
            self.parse_type_specifier,
            self.parse_type_qualifier,
            self.parse_alignment_specifier
        ), p, f

    def parse_member_declarator_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_member_declarator_list')
        return self.pand(
            self.parse_member_declarator,
            self.opt(self.pand(
                self.tok(mk_op(',')),
                self.parse_member_declarator_list,
            ))
        ), p, f

    def parse_member_declarator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_member_declarator')
        return self.por(
            self.parse_declarator,
            self.pand(
                self.opt(self.parse_declarator),
                self.tok(mk_op(':')),
                self.parse_constant_expression
            )
        ), p, f

    # e.g. enum someenum : int { SOME_ENUM_1 = 1, SOME_ENUM_2 }
    def parse_enum_specifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_enum_specifier')
        return self.pand(
            self.tok(mk_kw('enum')),
            self.por(
                self.pand(
                    self.opt(self.parse_attribute_specifier_sequence),
                    self.opt(self.typ('identifier')),
                    self.opt(self.parse_enum_type_specifier),
                    self.tok(mk_op('{')),
                    self.parse_enumerator_list,
                    self.opt(self.tok(mk_op(','))),
                    self.tok(mk_op('}'))
                ),
                self.pand(
                    self.typ('identifier'),
                    self.opt(self.parse_enum_type_specifier)
                )
            )
        ), p, f

    # e.g. SOME_ENUM_1, SOME_ENUM_2,
    def parse_enumerator_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_enumerator_list')
        return self.pand(
            self.parse_enumerator,
            self.opt(self.pand(
                self.tok(mk_op(',')),
                self.parse_enumerator_list
            ))
        ), p, f

    # e.g. SOME_ENUM = 1 << 2
    def parse_enumerator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_enumerator')
        return self.pand(
            self.parse_enumeration_constant,
            self.opt(self.parse_attribute_specifier_sequence),
            self.opt(self.pand(
                self.tok(mk_op('=')),
                self.parse_constant_expression
            ))
        ), p, f

    # e.g. : unsigned long long
    def parse_enum_type_specifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_enum_type_specifier')
        return self.pand(
            self.tok(mk_op(':')),
            self.parse_specifier_qualifier_list
        ), p, f

    def parse_atomic_type_specifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_atomic_type_specifier')
        return self.pand(
            self.tok(mk_kw('_Atomic')),
            self.tok(mk_op('(')),
            self.parse_type_name,
            self.tok(mk_op(')'))
        ), p, f

    def parse_typeof_specifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_typeof_specifier')
        return self.pand(
            self.por(
                self.tok(mk_kw('typeof')),
                self.tok(mk_kw('typeof_unqual')),
            ),
            self.tok(mk_op('(')),
            self.parse_typeof_specifier_argument,
            self.tok(mk_op(')'))
        ), p, f

    def parse_typeof_specifier_argument(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_typeof_specifier_argument')
        return self.por(
            self.parse_expression,
            self.parse_type_name
        ), p, f

    def parse_type_qualifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_type_qualifier')
        return self.por(
            self.tok(mk_kw('const')),
            self.tok(mk_kw('restrict')),
            self.tok(mk_kw('volatile')),
            self.tok(mk_kw('_Atomic'))
        ), p, f

    def parse_function_specifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_function_specifier')
        return self.por(
            self.tok(mk_kw('inline')),
            self.tok(mk_kw('_Noreturn'))
        ), p, f

    def parse_alignment_specifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_alignment_specifier')
        return self.pand(
            self.parse_alignas,
            self.tok(mk_op('(')),
            self.por(
                self.parse_type_name,
                self.parse_constant_expression
            ),
            self.tok(mk_op(')')),
        ), p, f

    def parse_declarator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_declarator')
        return self.pand(
            self.opt(self.parse_pointer),
            self.parse_direct_declarator
        ), p, f

    def parse_direct_declarator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_direct_declarator')
        return self.por(
            self.pand(
                self.maybe_typedef_name,
                self.opt(self.parse_attribute_specifier_sequence),
                self.opt(self.parse_direct_postfix_declarator)
            ),
            self.pand(
                self.tok(mk_op('(')),
                self.parse_declarator,
                self.tok(mk_op(')')),
                self.opt(self.parse_direct_postfix_declarator)
            )
        ), p, f

    def parse_direct_postfix_declarator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_direct_postfix_declarator')
        return self.por(
            self.parse_array_declarator,
            self.parse_function_declarator
        ), p, f

    def parse_array_declarator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_array_declarator')
        return self.pand(
            self.tok(mk_op('[')),
            self.por(
                self.pand(
                    self.tok(mk_kw('static')),
                    self.opt(self.parse_type_qualifier_list),
                    self.parse_assignment_expression
                ),
                self.pand(
                    self.parse_type_qualifier_list,
                    self.tok(mk_kw('static')),
                    self.parse_assignment_expression
                ),
                self.pand(
                    self.opt(self.parse_type_qualifier_list),
                    self.tok(mk_op('*'))
                ),
                self.pand(
                    self.opt(self.parse_type_qualifier_list),
                    self.opt(self.parse_assignment_expression)
                )
            ),
            self.tok(mk_op(']')),
            self.opt(self.parse_attribute_specifier_sequence),
            self.parse_direct_postfix_declarator
        ), p, f

    def parse_function_declarator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_function_declarator')
        return self.pand(
            self.tok(mk_op('(')),
            self.opt(self.parse_parameter_type_list),
            self.tok(mk_op(')')),
            self.opt(self.parse_attribute_specifier_sequence),
            self.parse_direct_postfix_declarator
        ), p, f

    def parse_pointer(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_pointer')
        return self.pand(
            self.tok(mk_op('*')),
            self.opt(self.parse_attribute_specifier_sequence),
            self.opt(self.parse_type_qualifier_list),
            self.opt(self.parse_pointer)
        ), p, f

    def parse_type_qualifier_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_type_qualifier_list')
        return self.pand(
            self.parse_type_qualifier,
            self.opt(self.parse_type_qualifier_list)
        ), p, f

    def parse_parameter_type_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_parameter_type_list')
        return self.pand(
            self.tok(mk_op('...')),
            self.pand(
                self.parse_parameter_list,
                self.opt(self.pand(
                    self.tok(mk_op(',')),
                    self.tok(mk_op('...')),
                ))
            )
        ), p, f

    def parse_parameter_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_parameter_list')
        return self.pand(
            self.parse_parameter_declaration,
            self.opt(self.pand(
                self.tok(mk_op(',')),
                self.parse_parameter_list
            ))
        ), p, f

    def parse_parameter_declaration(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_parameter_declaration')
        return self.pand(
            self.opt(self.parse_attribute_specifier_sequence),
            self.parse_declaration_specifiers,
            self.por(
                self.parse_declarator,
                self.opt(self.parse_abstract_declarator)
            )
        ), p, f

    def parse_type_name(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_type_name')
        return self.pand(
            self.parse_specifier_qualifier_list,
            self.opt(self.parse_abstract_declarator)
        ), p, f

    def parse_abstract_declarator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_abstract_declarator')
        return self.por(
            self.parse_pointer,
            self.pand(
                self.opt(self.parse_pointer),
                self.parse_direct_abstract_declarator
            )
        ), p, f

    def parse_direct_abstract_declarator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_direct_abstract_declarator')
        return self.por(
            self.pand(
                self.tok(mk_op('(')),
                self.parse_abstract_declarator,
                self.tok(mk_op(')'))
            ),
            self.pand(
                self.parse_array_abstract_declarator,
                self.opt(self.parse_attribute_specifier_sequence)
            ),
            self.pand(
                self.parse_function_abstract_declarator,
                self.opt(self.parse_attribute_specifier_sequence)
            )
        ), p, f

    def parse_array_abstract_declarator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_array_abstract_declarator')
        return self.pand(
            self.opt(self.parse_direct_abstract_declarator),
            self.tok(mk_op('[')),
            self.por(
                self.pand(
                    self.opt(self.parse_type_qualifier_list),
                    self.opt(self.parse_assignment_expression)
                ),
                self.pand(
                    self.tok(mk_kw('static')),
                    self.opt(self.parse_type_qualifier_list),
                    self.parse_assignment_expression
                ),
                self.pand(
                    self.parse_type_qualifier_list,
                    self.tok(mk_kw('static')),
                    self.parse_assignment_expression
                ),
                self.tok(mk_op('*'))
            ),
            self.tok(mk_op(']'))
        ), p, f

    def parse_function_abstract_declarator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_function_abstract_declarator')
        return self.pand(
            self.opt(self.parse_direct_abstract_declarator),
            self.tok(mk_op('(')),
            self.opt(self.parse_parameter_type_list),
            self.tok(mk_op(')'))
        ), p, f

    def parse_typedef_name(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_typedef_name')
        def intl(p1, f1):
            if (ident := self.parse_identifier()) and ident in self.types:
                return p1
            return f1
        return self.pand(self.check_for_any, intl), p, f

    def parse_braced_initializer(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_braced_initializer')
        return self.pand(
            self.tok(mk_op('{')),
            self.opt(self.pand(
                self.parse_initializer_list,
                self.opt(self.tok(mk_op(',')))
            )),
            self.tok(mk_op('}'))
        ), p, f

    def parse_initializer(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_initializer')
        return self.por(
            self.parse_assignment_expression,
            self.parse_braced_initializer
        ), p, f

    def parse_initializer_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_initializer_list')
        return self.pand(
            self.opt(self.parse_designation),
            self.parse_initializer,
            self.opt(self.pand(
                self.tok(mk_op(',')),
                self.parse_initializer_list
            ))
        ), p, f

    def parse_designation(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_designation')
        return self.pand(
            self.parse_designator_list,
            self.tok(mk_op('='))
        ), p, f

    def parse_designator_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_designator_list')
        return self.pand(
            self.parse_designator,
            self.opt(self.parse_designator_list)
        ), p, f

    def parse_designator(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_designator')
        return self.por(
            self.pand(
                self.tok(mk_op('[')),
                self.parse_constant_expression,
                self.tok(mk_op(']'))
            ),
            self.pand(
                self.tok(mk_op('.')),
                self.typ('identifier')
            )
        ), p, f

    def parse_static_assert_declaration(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_static_assert_declaration')
        return self.pand(
            self.parse_static_assert,
            self.tok(mk_op('(')),
            self.parse_constant_expression,
            self.opt(self.pand(
                self.tok(mk_op(',')),
                self.typ('string')
            )),
            self.tok(mk_op(')')),
            self.tok(mk_op(';'))
        ), p, f

    def parse_attribute_specifier_sequence(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_attribute_specifier_sequence')
        return self.pand(
            self.parse_attribute_specifier,
            self.opt(self.parse_attribute_specifier_sequence)
        ), p, f

    def parse_attribute_specifier(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_attribute_specifier')
        return self.por(
            self.pand(
                self.tok(mk_id('__attribute__')),
                self.tok(mk_op('(')),
                self.tok(mk_op('(')),
                self.parse_attribute_list,
                self.tok(mk_op(')')),
                self.tok(mk_op(')'))
            ),
            self.pand(
                self.tok(mk_op('[')),
                self.tok(mk_op('[')),
                self.parse_attribute_list,
                self.tok(mk_op(']')),
                self.tok(mk_op(']'))
            )
        ), p, f

    def parse_attribute_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_attribute_list')
        return self.opt(self.pand(
            self.parse_attribute,
            self.opt(self.pand(
                self.tok(mk_op(',')),
                self.parse_attribute_list
            ))
        )), p, f

    def parse_attribute(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_attribute')
        return self.pand(
            self.parse_attribute_token,
            self.opt(self.parse_attribute_argument_clause)
        ), p, f

    def parse_attribute_token(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_attribute_token')
        return self.por(
            self.parse_standard_attribute,
            self.parse_attribute_prefixed_token
        ), p, f

    def parse_standard_attribute(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_standard_attribute')
        return self.typ('identifier'), p, f

    def parse_attribute_prefixed_token(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_attribute_prefixed_token')
        return self.pand(
            self.parse_attribute_prefix,
            self.tok(mk_op('::')),
            self.typ('identifier')
        ), p, f

    def parse_attribute_prefix(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_attribute_prefix')
        return self.typ('identifier'), p, f

    def parse_attribute_argument_clause(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_attribute_argument_clause')
        return self.pand(
            self.tok(mk_op('(')),
            self.opt(self.parse_balanced_token_sequence),
            self.tok(mk_op(')'))
        ), p, f

    def parse_balanced_token_sequence(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_balanced_token_sequence')
        return self.pand(
            self.parse_balanced_token,
            self.opt(self.parse_balanced_token_sequence)
        ), p, f

    def parse_balanced_token(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_balanced_token_sequence')
        return self.por(
            self.pand(
                self.tok(mk_op('(')),
                self.opt(self.parse_balanced_token_sequence),
                self.tok(mk_op(')'))
            ),
            self.pand(
                self.tok(mk_op('[')),
                self.opt(self.parse_balanced_token_sequence),
                self.tok(mk_op(']'))
            ),
            self.pand(
                self.tok(mk_op('{')),
                self.opt(self.parse_balanced_token_sequence),
                self.tok(mk_op('}'))
            ),
            self.pnot(
                self.por(
                    self.tok(mk_op('(')),
                    self.tok(mk_op(')')),
                    self.tok(mk_op('[')),
                    self.tok(mk_op(']')),
                    self.tok(mk_op('{')),
                    self.tok(mk_op('}'))
                )
            )
        ), p, f

    # ===== A.3.3 Statements =====

    def parse_statement(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_statement')
        return self.por(
            self.parse_labeled_statement,
            self.parse_unlabeled_statement
        ), p, f

    def parse_unlabeled_statement(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_unlabeled_statement')
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

    def parse_primary_block(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_primary_block')
        return self.por(
            self.parse_compound_statement,
            self.parse_selection_statement,
            self.parse_iteration_statement
        ), p, f

    def parse_secondary_block(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_secondary_block')
        return self.parse_statement, p, f

    def parse_label(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_label')
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

    def parse_labeled_statement(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_labeled_statement')
        return self.pand(
            self.parse_label,
            self.parse_statement
        ), p, f

    def parse_compound_statement(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_compound_statement')
        return self.pand(
            self.tok(mk_op('{')),
            self.opt(self.parse_block_item_list),
            self.tok(mk_op('}'))
        ), p, f

    def parse_block_item_list(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_block_item_list')
        return self.pand(
            self.parse_block_item,
            self.opt(self.parse_block_item_list)
        ), p, f

    def parse_block_item(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_block_item')
        return self.por(
            self.parse_declaration,
            self.parse_unlabeled_statement,
            self.parse_label
        ), p, f

    def parse_expression_statement(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_expression_statement')
        return self.pand(
            self.opt(self.pand(
                self.opt(self.parse_attribute_specifier_sequence),
                self.parse_expression
            )),
            self.tok(mk_op(';'))
        ), p, f

    def parse_selection_statement(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_selection_statement')
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

    def parse_iteration_statement(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_iteration_statement')
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
                    self.pand(
                        self.opt(self.parse_expression),
                        self.tok(mk_op(';'))
                    )
                ),
                self.opt(self.parse_expression),
                self.tok(mk_op(';')),
                self.opt(self.parse_expression),
                self.tok(mk_op(')')),
                self.parse_secondary_block
            )
        ), p, f

    def parse_jump_statement(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_jump_statement')
        return self.por(
            self.pand(self.tok(mk_kw('goto')), self.typ('identifier'),
                self.tok(mk_op(';'))),
            self.pand(self.tok(mk_kw('continue')), self.tok(mk_op(';'))),
            self.pand(self.tok(mk_kw('break')), self.tok(mk_op(';'))),
            self.pand(self.tok(mk_kw('return')), self.opt(self.parse_expression),
                self.tok(mk_op(';')))
        ), p, f

    # ===== A.3.4 External Definitions =====

    def parse_translation_unit(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_translation_unit')
        return self.pand(
            self.parse_external_declaration,
            self.opt(self.parse_translation_unit)
        ), p, f

    def parse_external_declaration(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_external_declaration')
        return self.por(
            self.parse_function_definition,
            self.parse_declaration
        ), p, f

    def parse_function_definition(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_function_definition')
        return self.pand(
            self.opt(self.parse_attribute_specifier_sequence),
            self.parse_declaration_specifiers,
            self.parse_declarator,
            self.parse_function_body
        ), p, f

    def parse_function_body(self, p:Any, f:Any)->tuple:
        dprint(3, 'parse_function_body')
        return self.parse_compound_statement, p, f

    def parse(self, tokens: list):
        super().reset()
        self.tokens = tokens
        self.len = len(tokens)
        self.time = time.time()

        self.unwrap((self.parse_translation_unit, True, False))
        print(self.types)

if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
