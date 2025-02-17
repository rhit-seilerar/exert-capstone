import os
import types
from exert.utilities.tokenmanager import tok_seq, TokenManager
from exert.parser.definitions import DefState, DefOption
from exert.utilities.debug import dprint

def read_file(path):
    try:
        with open(path, 'r', encoding = 'utf-8') as file:
            return file.read()
    except IOError:
        return None

class Preprocessor(TokenManager):
    def __init__(self, tokenizer, includes, filereader = read_file):
        super().__init__()
        self.tokenizer = tokenizer
        self.includes = includes
        self.filereader = filereader
        self.invalid_paths = set()
        self.tokenized_cache = {}
        self.unresolved = []
        self.defs = DefState()

    def load_file(self, path, is_relative):
        if self.defs.is_skipping():
            dprint(2, '  ' * self.defs.depth() + f'::Skipping {path}')
            return

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
                dprint(2, '  ' * self.defs.depth() + f'::Reusing {load_path}')
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
        # self.err('Failed to include', path)
        dprint(2, '  ' * self.defs.depth() + '::Failed to include', path)
        self.invalid_paths.add(path)
        return True

    def push_optional(self, name):
        self.conditions.append(name)
        self.insert(('optional', name), True)

    def pop_optional(self):
        self.insert(('optional', None), True)
        return self.conditions.pop()

    def skip_to_newline(self, offset = 0):
        tokens = []
        while not self.peek_type() == 'newline':
            tokens.append(self.next())
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(len(tokens) + 3 + offset)
        return tokens

    def handle_line(self):
        if not (line := self.consume_type('integer')):
            return self.err('#line must be followed by a line number')
        if (file := self.consume_type('string')):
            self.file = file[1]
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        dprint(3, '  ' * self.defs.depth() + "#line", line[1], f'"{file[1]}"' if file else '')
        self.remove(5 if file else 4)
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
        self.remove(4)
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
        self.remove(4)
        self.defs.on_undef(name)
        return True

    def handle_ifdef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#ifdef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        if self.defs.on_ifdef(name):
            self.push_optional(f'defined({name})')
        return True

    def handle_ifndef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#ifndef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        if self.defs.on_ifndef(name):
            self.push_optional(f'!defined({name})')
        return True

    def handle_elifdef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#elifdef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        condition = None
        if self.defs.layers[-1].any_kept:
            condition = self.pop_optional()
        if self.defs.on_elifdef(name):
            if condition is not None:
                self.push_optional(f'!({condition}) && defined({name})')
            else:
                self.push_optional(f'defined({name})')
        return True

    def handle_elifndef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#elifndef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        condition = None
        if self.defs.layers[-1].any_kept:
            condition = self.pop_optional()
        if self.defs.on_elifndef(name):
            if condition is not None:
                self.push_optional(f'!({condition}) && !defined({name})')
            else:
                self.push_optional(f'!defined({name})')
        self.remove(4)
        return True

    def handle_if(self):
        if not (tokens := self.skip_to_newline()):
            return False
        if self.defs.on_if({}):
            self.push_optional(' '.join(str(n[1]) for n in tokens))
        return True

    def handle_elif(self):
        if not (tokens := self.skip_to_newline()):
            return False
        condition = None
        if self.defs.layers[-1].any_kept:
            condition = self.pop_optional()
        if self.defs.on_elif({}):
            cond_str = " ".join(str(n) for n in tokens)
            if condition is not None:
                self.push_optional(f'!({condition}) && ({cond_str})')
            else:
                self.push_optional(f'{cond_str}')
        return True

    def handle_else(self):
        #TODO get cond str from defmap conditions
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(3)
        condition = None
        if self.defs.layers[-1].any_kept:
            condition = self.pop_optional()
        if self.defs.on_else():
            if condition is not None:
                self.push_optional(f'!({condition})')
            else:
                self.push_optional('')
        return True

    def handle_endif(self):
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(3)
        if self.defs.layers[-1].any_kept:
            self.pop_optional()
        self.defs.on_endif()
        return True

    def handle_error(self):
        #TODO error should cancel the current block
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

    def insert(self, tokens, before = False):
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
        if before:
            self.index += size

    def remove(self, count, index = None):
        index = self.index if index is None else index
        assert index <= self.index
        del self.tokens[index-count:index]
        self.len -= count
        self.index -= count

    def substitute(self):
        expansion_stack = []
        def subst(token):
            if token[0] not in ['identifier', 'keyword']:
                return None
            if token[1] in expansion_stack:
                return None
            substitutions = set()
            opts = self.defs.get_replacements(token)
            if opts == set():
                return []
            if opts == {DefOption([token])}:
                return None
            expansion_stack.append(token[1])
            for opt in opts:
                tokens = []
                for token in opt.tokens:
                    tokens += subst(token) or [token]
                if tokens:
                    substitutions.add(DefOption(tokens))
            expansion_stack.pop()
            if len(substitutions) > 1:
                return [('any', substitutions)]
            elif len(substitutions) == 1:
                return list(substitutions)[0].tokens
            return []

        tok = self.next()
        if tok[1] == 'MAX_REG_OFFSET':
            print(self.defs.layers[-1].current['MAX_REG_OFFSET'])
        result = subst(tok)
        if result is not None:
            dprint(3, f"::Substituting {tok[0]} '{tok[1]}': {tok_seq(result)}")
            self.remove(1)
            self.insert(result, True)

    def preprocess(self, data):
        super().reset()
        self.conditions = []
        self.file = ''
        self.insert(data)

        # String combination not implemented
        # Stringification and concatenation not implemented

        remove_from = None

        while self.has_next() and not self.has_error:
            if self.consume_directive('#'):
                self.parse_directive()
                continue

            if self.defs.is_skipping():
                if remove_from is None:
                    remove_from = self.index
                self.next()
                continue

            if remove_from is not None:
                self.remove(self.index - remove_from, self.index)
                remove_from = None

            if self.peek_type() in ['identifier', 'keyword']:
                self.substitute()
                continue

            self.bump()

        if remove_from is not None:
            self.remove((self.index - 1) - remove_from, self.index - 1)

        return self

    def __str__(self):
        tokens = tok_seq(self.tokens, newlines = True)
        definitions = '\n'.join(f'{d[0]}: {str(d[1])}' for d in self.defs.flat_defines().items())
        unknowns = '\n'.join(self.defs.flat_unknowns())
        return f'\n===== TOKENS =====\n{tokens}\n' \
            f'\n===== DEFINITIONS =====\n{definitions}\n' \
            f'\n===== UNKNOWNS =====\n{unknowns}\n' \
            f'\n===== INVALID PATHS =====\n{self.invalid_paths}\n'
