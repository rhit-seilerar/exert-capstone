"""
TODO There are still a number of optimizations that can be done for better results:
 - #defines with a replacement with no #undef preceding them guarantee only no definition from cli
 - Better guarantees from #if/#elif expressions
 - Guarantees from #if/#elif can be used in the rules system
 - #pragma
 - Macro replacement, #, ##, __VA_ARGS__, __VA_OPT__
 - __FILE__, __DATE__, __LINE__, __TIME__, __COUNT__, _Pragma
"""

import os
import types
from typing import cast, Self
from collections.abc import Callable
from exert.parser.tokenmanager import mk_int, tok_seq, TokenManager
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.defstate import DefState
from exert.parser.serializer import write_tokens, read_tokens
from exert.parser.tokenizer import Tokenizer
from exert.utilities.debug import dprint
from exert.utilities.types.global_types import TokenType, TokenType3

def read_file(path: str) -> (str | None):
    try:
        with open(path, 'r', encoding = 'utf-8') as file:
            return file.read()
    except IOError:
        return None

class Preprocessor(TokenManager):
    def __init__(self, tokenizer: Tokenizer, bitsize: int,
                 includes: list[str | Callable[[str], (str | None)]], defns: dict[str, str],
                 filereader: Callable[[str], str | None] = read_file):
        super().__init__()
        self.tokenizer = tokenizer
        self.includes = includes
        self.filereader = filereader
        self.invalid_paths: set[str] = set()
        self.tokenized_cache: dict[str, str] = {}
        self.unresolved: list[str] = []
        initdefs = {
            key: Def(DefOption(tokenizer.tokenize(defns[key]))) for key in defns
        }
        initdefs['__STDC__'] = Def(DefOption([mk_int(1)]))
        initdefs['__STDC_EMBED_NOT_FOUND__'] = Def(DefOption([mk_int(0)]))
        initdefs['__STDC_EMBED_FOUND__'] = Def(DefOption([mk_int(1)]))
        initdefs['__STDC_EMBED_EMPTY__'] = Def(DefOption([mk_int(2)]))
        initdefs['__STDC_HOSTED__'] = Def(DefOption([mk_int(0)]))
        initdefs['__STDC_UTF_16__'] = Def(DefOption([mk_int(1)]))
        initdefs['__STDC_UTF_32__'] = Def(DefOption([mk_int(1)]))
        initdefs['__STDC_VERSION__'] = Def(DefOption([mk_int(202311, 'L')]))
        self.defs = DefState(bitsize, initial = initdefs)

    def load_file(self, path: str, is_relative: bool) -> bool:
        if self.defs.is_skipping():
            dprint(1.5, '  ' * self.defs.depth() + f'::Skipping {path}')
            return True

        includes = self.includes.copy()
        if is_relative:
            includes.insert(0, os.path.dirname(self.file))

        for include in includes:
            load_path = ''
            if isinstance(include, types.FunctionType):
                load_path = include(path)
            else:
                assert isinstance(include, str)
                load_path = os.path.join(include, path)

            if load_path is None:
                continue

            data: str = ''
            if load_path in self.tokenized_cache:
                res = self.tokenized_cache.get(load_path)
                assert res is not None
                data = res
                dprint(1.5, '  ' * self.defs.depth() + f'::Reusing {load_path}')
            else:
                dprint(4, f'::Testing {load_path}')
                file_read = self.filereader(load_path)
                if file_read is None:
                    continue

                data = file_read
                if not self.defs.is_skipping():
                    dprint(1, '  ' * self.defs.depth() + f'::Included {load_path}')

                prefix = f'#line 1 "{load_path}"\n'
                suffix = f'\n#line 1 "{self.file}"' if self.file else '\n#line 1'
                data = prefix + data + suffix
                self.tokenized_cache[load_path] = data

            self.insert(data)
            return True
        self.unresolved.append(path)
        dprint(1.5, '  ' * self.defs.depth() + '::Failed to include', path)
        self.invalid_paths.add(path)
        return True

    def package_emissions(self, is_start: bool = False, is_end: bool = False) -> None:
        if is_start:
            self.defs.layers[-1].blocks = []
            self.defs.layers[-1].emitted = []
            return

        block = self.defs.layers[-1].emitted
        self.defs.layers[-1].emitted = []

        if self.defs.is_skipping():
            return

        if len(block) > 0:
            self.defs.layers[-1].blocks.append(block)

        if is_end:
            blocks = self.defs.layers[-1].blocks
            if len(blocks) == 0:
                return
            if not self.defs.layers[-1].closed:
                self.defs.layers[-1].blocks.append([])

            if len(blocks) == 1:
                self.defs.layers[-2].emitted += blocks[0]
            else:
                self.defs.layers[-2].emitted.append(('any', '',
                    {DefOption(b) for b in blocks}))

    def skip_to_newline(self, offset: int = 0) -> list[TokenType]:
        tokens: list[TokenType] = []
        while not self.peek_type() == 'newline':
            tokens.append(cast(TokenType, self.next()))
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        return tokens

    def handle_line(self) -> bool:
        if not (line := self.consume_type('integer')):
            return self.err('#line must be followed by a line number')
        if (file := self.consume_type('string')):
            self.file = cast(str, file[1])
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        dprint(3, '  ' * self.defs.depth() + "#line", line[1], f'"{file[1]}"' if file else '')
        return True

    def handle_include(self) -> bool:
        if not (file := self.consume_type('string')):
            return self.err('#include must be followed by a path')
        assert len(file) > 2
        if file[2] not in ['', '<']:
            return self.err('#include cannot have string literal modifiers')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        dprint(2, '  ' * self.defs.depth() + '#include',
            f'<{file[1]}>' if file[2] == '<' else f'"{file[1]}"')
        return self.load_file(cast(str, file[1]), file[2] != '<')

    def handle_define(self) -> bool:
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#define must be followed by an identifier')
        params = None
        index = self.index
        if self.consume_directive('('):
            params = []
            while True:
                if (ident := self.parse_identifier()):
                    params.append(ident)
                    if self.consume_operator(')'):
                        break
                    if not self.consume_operator(','):
                        return self.err(f"Expected the macro argument to be followed " \
                            f"with ',' or ')', but got {self.peek() or 'EOF'}")
                elif self.consume_operator('...'):
                    params.append('__VA_ARGS__')
                    if not self.consume_operator(')'):
                        return self.err('__VA_ARGS__ must be the last argument in a function macro')
                    break
                elif self.consume_operator(')'):
                    break
                else:
                    return self.err("Expected a parameter or '...', but got " \
                        f"{self.peek() or 'EOF'}")
        self.tokens_consumed -= self.index - index
        self.index = index
        if (tokens := self.skip_to_newline(1)) is None:
            return False
        self.defs.on_define(name, tokens, params)
        return True

    def handle_undef(self) -> bool:
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#undef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.defs.on_undef(name)
        return True

    def handle_ifdef(self) -> bool:
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#ifdef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.defs.on_ifdef(name)
        self.package_emissions(is_start = True)
        return True

    def handle_ifndef(self) -> bool:
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#ifndef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.defs.on_ifndef(name)
        self.package_emissions(is_start = True)
        return True

    def handle_if(self) -> bool:
        if not (tokens := self.skip_to_newline()):
            return False
        self.defs.on_if(tokens)
        self.package_emissions(is_start = True)
        return True

    def handle_elifdef(self) -> bool:
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#elifdef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.package_emissions()
        self.defs.on_elifdef(name)
        return True

    def handle_elifndef(self) -> bool:
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#elifndef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.package_emissions()
        self.defs.on_elifndef(name)
        return True

    def handle_elif(self) -> bool:
        if not (tokens := self.skip_to_newline()):
            return False
        self.package_emissions()
        self.defs.on_elif(tokens)
        return True

    def handle_else(self) -> bool:
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.package_emissions()
        self.defs.on_else()
        return True

    def handle_endif(self) -> bool:
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.package_emissions(is_end = True)
        self.defs.on_endif()
        return True

    def handle_error(self) -> list[TokenType]:
        if not self.defs.is_skipping():
            dprint(2, '  ' * self.defs.depth() + '#error')
        assert self.defs.layers[-1].current is not None
        self.defs.layers[-1].current.skipping = True
        return self.skip_to_newline()

    def handle_warning(self) -> list[TokenType]:
        if not self.defs.is_skipping():
            dprint(2, '  ' * self.defs.depth() + '#warning')
        return self.skip_to_newline()

    def handle_pragma(self) -> list[TokenType]:
        if not self.defs.is_skipping():
            dprint(2, '  ' * self.defs.depth() + '#pragma')
        return self.skip_to_newline()

    def parse_directive(self) -> (bool | list[TokenType]):
        result: (bool | list[TokenType]) = False
        if self.consume(('identifier', 'line')):
            result = self.handle_line()
        elif self.consume_identifier('include'):
            result = self.handle_include()
        elif self.consume_identifier('define'):
            result = self.handle_define()
        elif self.consume_identifier('undef'):
            result = self.handle_undef()
        elif self.consume_identifier('ifdef'):
            result = self.handle_ifdef()
        elif self.consume_identifier('ifndef'):
            result = self.handle_ifndef()
        elif self.consume_identifier('elifdef'):
            result = self.handle_elifdef()
        elif self.consume_identifier('elifndef'):
            result = self.handle_elifndef()
        elif self.consume_keyword('if'):
            result = self.handle_if()
        elif self.consume_identifier('elif'):
            result = self.handle_elif()
        elif self.consume_keyword('else'):
            result = self.handle_else()
        elif self.consume_identifier('endif'):
            result = self.handle_endif()
        elif self.consume_identifier('error'):
            result = self.handle_error()
        elif self.consume_identifier('warning'):
            result = self.handle_warning()
        elif self.consume_identifier('pragma'):
            result = self.handle_pragma()
        elif not self.consume_type('newline'):
            return self.err(f'Unexpected token after directive: {self.peek()}')

        return result

    def insert(self, tokens: (str | TokenType | list[TokenType])) -> None:
        if isinstance(tokens, str):
            tokens = self.tokenizer.tokenize(tokens)
        if isinstance(tokens, tuple):
            tokens = [tokens]
        dprint(5, tokens)
        prefix = self.tokens[:self.index]
        suffix = self.tokens[self.index:]
        size = len(tokens)
        assert isinstance(tokens, list)
        self.tokens = prefix + tokens + suffix
        self.len += size
        self.tokens_added += size

    def substitute(self) -> None:
        tok = self.peek()
        assert tok is not None
        result = self.defs.substitute(self)
        if result != [tok]:
            dprint(3, f"::Substituting {tok[0]} '{tok[1]}': {tok_seq(result)}")
        self.emit_tokens(result)

    def emit_tokens(self, tokens: list[TokenType]) -> None:
        if not self.defs.is_skipping():
            self.defs.layers[-1].emitted += tokens

    def preprocess(self, data: str, cache: str, reset_cache: bool = False) -> Self:
        super().reset()
        self.conditions: list[TokenType] = []
        self.file = ''
        self.insert(data)

        if os.path.exists(cache):
            if not reset_cache:
                return self
            os.remove(cache)
            assert not os.path.exists(cache)
            print('Regenerating...')
        else:
            print('Cache file not found: Generating...')

        # Stringification and concatenation not implemented

        with open(cache, mode = 'bw') as file:
            self.defs.layers[-1].emitted = []

            while self.has_next() and not self.has_error:
                self.print_progress()

                if self.consume_directive('#'):
                    self.parse_directive()
                    continue

                if self.defs.is_skipping():
                    self.next()
                    continue

                if self.peek_type() in ['identifier', 'keyword']:
                    self.substitute()
                    continue

                if self.peek_type(-1) == 'string' and self.peek_type() == 'string':
                    prev = cast(TokenType3, self.peek(-1))
                    if prev[2] != '<':
                        curr = cast(TokenType3, self.next())
                        if curr[2] and prev[2] and curr[2] != prev[2]:
                            return self.err(f'String concatenation of different encodings! \
                                ({prev[2]} and {curr[2]})')
                        newstr = ('string', cast(str, prev[1]) + cast(str, curr[1]), \
                            prev[2] or curr[2])
                        self.defs.layers[-1].emitted[-1] = newstr
                        continue

                self.emit_tokens([cast(TokenType, self.next())])

            write_tokens(file, self.defs.layers[-1].emitted)

        return self

    def load(self, cache: str) -> Self:
        self.tokens = read_tokens(cache)
        return self

    def __str__(self) -> str:
        tokens = tok_seq(self.tokens, newlines = True)
        definitions = '\n'.join(f'{d[0]}: {str(d[1])}' for d in self.defs.flat_defines().items())
        unknowns = '\n'.join(self.defs.flat_unknowns())
        return f'\n===== TOKENS =====\n{tokens}\n' \
            f'\n===== DEFINITIONS =====\n{definitions}\n' \
            f'\n===== UNKNOWNS =====\n{unknowns}\n' \
            f'\n===== INVALID PATHS =====\n{self.invalid_paths or ""}\n'
