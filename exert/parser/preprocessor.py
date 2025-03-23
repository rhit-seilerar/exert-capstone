"""
TODO There are still a number of optimizations that can be done for better results:
 - #defines with a replacement with no #undef preceding them guarantee only no definition from cli
 - Guarantees from #if/#elif expressions
 - Guarantees from #if/#elif can be used in the rules system
 - #error should cancel the block
 - #pragma
 - String concatenation, token concatenation, token stringification
"""

import os
import types

from exert.parser.tokenmanager import tok_seq, TokenManager
from exert.parser.definitions import DefState, Def, DefOption
from exert.parser.serializer import write_tokens, read_tokens
from exert.utilities.debug import dprint

def read_file(path):
    try:
        with open(path, 'r', encoding = 'utf-8') as file:
            return file.read()
    except IOError:
        return None

class Preprocessor(TokenManager):
    def __init__(self, tokenizer, bitsize, includes, defns, filereader = read_file):
        super().__init__()
        self.tokenizer = tokenizer
        self.includes = includes
        self.filereader = filereader
        self.invalid_paths = set()
        self.tokenized_cache = {}
        self.unresolved = []
        self.defs = DefState(bitsize, initial = {
            key: Def(DefOption(tokenizer.tokenize(defns[key]))) for key in defns
        })

    def load_file(self, path, is_relative):
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
                load_path = os.path.join(include, path)

            if load_path is None:
                continue

            data = ''
            if load_path in self.tokenized_cache:
                data = self.tokenized_cache.get(load_path)
                dprint(1.5, '  ' * self.defs.depth() + f'::Reusing {load_path}')
            else:
                dprint(4, f'::Testing {load_path}')
                data = self.filereader(load_path)
                if data is None:
                    continue

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

    def push_optional(self):
        if not self.defs.is_skipping():
            self.emit_tokens([('optional', self.defs.get_cond_tokens())])

    def pop_optional(self):
        if not self.defs.is_skipping():
            self.emit_tokens([('optional', [])])

    def skip_to_newline(self, offset = 0):
        tokens = []
        while not self.peek_type() == 'newline':
            tokens.append(self.next())
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        return tokens

    def handle_line(self):
        if not (line := self.consume_type('integer')):
            return self.err('#line must be followed by a line number')
        if (file := self.consume_type('string')):
            self.file = file[1]
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        dprint(3, '  ' * self.defs.depth() + "#line", line[1], f'"{file[1]}"' if file else '')
        return True

    def handle_include(self):
        if not (file := self.consume_type('string')):
            return self.err('#include must be followed by a path')
        if file[2] not in ['', '<']:
            return self.err('#include cannot have string literal modifiers')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        dprint(2, '  ' * self.defs.depth() + '#include',
            f'<{file[1]}>' if file[2] == '<' else f'"{file[1]}"')
        return self.load_file(file[1], file[2] != '<')

    def handle_define(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#define must be followed by an identifier')
        params = []
        index = self.index
        if self.consume_directive('('):
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
        self.defs.on_define(name, params, tokens)
        return True

    def handle_undef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#undef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.defs.on_undef(name)
        return True

    def handle_ifdef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#ifdef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.defs.on_ifdef(name)
        self.push_optional()
        return True

    def handle_ifndef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#ifndef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.defs.on_ifndef(name)
        self.push_optional()
        return True

    def handle_elifdef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#elifdef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.pop_optional()
        self.defs.on_elifdef(name)
        self.push_optional()
        return True

    def handle_elifndef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#elifndef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.pop_optional()
        self.defs.on_elifndef(name)
        self.push_optional()
        return True

    def handle_if(self):
        if not (tokens := self.skip_to_newline()):
            return False
        self.defs.on_if(tokens)
        self.push_optional()
        return True

    def handle_elif(self):
        if not (tokens := self.skip_to_newline()):
            return False
        self.pop_optional()
        self.defs.on_elif(tokens)
        self.push_optional()
        return True

    def handle_else(self):
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.pop_optional()
        self.defs.on_else()
        self.push_optional()
        return True

    def handle_endif(self):
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.pop_optional()
        self.defs.on_endif()
        return True

    def handle_error(self):
        if not self.defs.is_skipping():
            dprint(2, '  ' * self.defs.depth() + '#error')
        return self.skip_to_newline()

    def handle_warning(self):
        if not self.defs.is_skipping():
            dprint(2, '  ' * self.defs.depth() + '#warning')
        return self.skip_to_newline()

    def handle_pragma(self):
        if not self.defs.is_skipping():
            dprint(2, '  ' * self.defs.depth() + '#pragma')
        return self.skip_to_newline()

    def parse_directive(self):
        result = None
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
        else:
            return self.err(f'Unknown preprocessor directive #{self.next()[1]}')
        return result

    def insert(self, tokens):
        if isinstance(tokens, str):
            tokens = self.tokenizer.tokenize(tokens)
        if isinstance(tokens, tuple):
            tokens = [tokens]
        dprint(5, tokens)
        prefix = self.tokens[:self.index]
        suffix = self.tokens[self.index:]
        size = len(tokens)
        self.tokens = prefix + tokens + suffix
        self.len += size
        self.tokens_added += size

    def substitute(self):
        tok = self.next()
        result = self.defs.substitute(tok)
        if result != [tok]:
            dprint(3, f"::Substituting {tok[0]} '{tok[1]}': {tok_seq(result)}")
        self.emit_tokens(result)

    def emit_tokens(self, tokens):
        if self.cache_file:
            write_tokens(self.cache_file, tokens)

    def preprocess(self, data, cache, reset_cache = False):
        super().reset()
        self.conditions = []
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

        # String combination not implemented
        # Stringification and concatenation not implemented

        with open(cache, mode = 'bw') as file:
            self.cache_file = file
            flush_size = 40000

            while self.has_next() and not self.has_error:
                self.print_progress()

                if self.index > flush_size + 20:
                    del self.tokens[:flush_size]
                    self.index -= flush_size
                    self.len -= flush_size

                if self.consume_directive('#'):
                    self.parse_directive()
                    continue

                if self.defs.is_skipping():
                    self.next()
                    continue

                if self.peek_type() in ['identifier', 'keyword']:
                    self.substitute()
                    continue

                self.emit_tokens([self.next()])
        return self

    def load(self, cache):
        self.tokens = read_tokens(cache)

    def __str__(self):
        tokens = tok_seq(self.tokens, newlines = True)
        definitions = '\n'.join(f'{d[0]}: {str(d[1])}' for d in self.defs.flat_defines().items())
        unknowns = '\n'.join(self.defs.flat_unknowns())
        return f'\n===== TOKENS =====\n{tokens}\n' \
            f'\n===== DEFINITIONS =====\n{definitions}\n' \
            f'\n===== UNKNOWNS =====\n{unknowns}\n' \
            f'\n===== INVALID PATHS =====\n{self.invalid_paths or ""}\n'
