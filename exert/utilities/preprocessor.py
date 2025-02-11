import os
from exert.utilities.tokenmanager import TokenManager

class Preprocessor(TokenManager):
    def __init__(self, tokenizer, includes):
        super().__init__()
        self.tokenizer = tokenizer
        self.includes = includes
        self.definitions = dict()
        self.unresolved = list()

    def load_file(self, path, is_relative):
        includes = self.includes.copy()
        if is_relative:
            includes.insert(0, os.path.dirname(self.file))
        for include in includes:
            load_path = ''
            if isinstance(include, tuple):
                load_path = os.path.join(include[0], include[1](path))
            else:
                load_path = os.path.join(include, path)

            data = ''
            try:
                with open(load_path, 'r', encoding = 'utf-8') as file:
                    print(f'Loading path: {load_path}')
                    data = file.read()
            except IOError:
                continue
            prefix = f'#line 1 "{load_path}"\n'
            suffix = f'\n#line 1 "{self.file}"' if self.file else '\n#line 1'
            to_insert = prefix + data + suffix
            self.insert(to_insert)
            return True
        self.unresolved.append(path)
        print(f"Failed to include '{path}'")
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
        if not self.consume_type('integer'):
            return self.err('#line must be followed by a line number')
        if (file := self.consume_type('string')):
            self.file = file[1]
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(5 if file else 4)
        return True

    def handle_include(self):
        if not (file := self.consume_type('string')):
            return self.err('#include must be followed by a path')
        if file[2] not in ['', '<']:
            return self.err('#include cannot have string literal modifiers')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        return self.load_file(file[1], file[2] != '<')

    def handle_define(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#define must be followed by an identifier')
        if (tokens := self.skip_to_newline(1)) is None:
            return False
        self.definitions[name] = (arr := self.definitions.get(name, list()))
        arr.append(tokens)
        return True

    def handle_undef(self):
        if not self.parse_ident_or_keyword():
            return self.err('#undef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        return True

    def handle_ifdef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#ifdef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        self.push_optional(f'defined({name})')
        self.depth += 1
        return True

    def handle_ifndef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#ifndef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        self.push_optional(f'!defined({name})')
        self.depth += 1
        return True

    def handle_if(self):
        if not (tokens := self.skip_to_newline()):
            return False
        self.push_optional(' '.join(str(n[1]) for n in tokens))
        self.depth += 1
        return True

    def handle_elif(self):
        if not (tokens := self.skip_to_newline()):
            return False
        condition = self.pop_optional()
        self.push_optional(f'!({condition}) && ({" ".join(str(n) for n in tokens)})')
        return True

    def handle_else(self):
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(3)
        condition = self.pop_optional()
        self.push_optional(f'!({condition})')
        return True

    def handle_endif(self):
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(3)
        self.depth -= 1
        self.pop_optional()
        return True

    def handle_error(self):
        return self.skip_to_newline()

    def handle_warning(self):
        return self.skip_to_newline()

    def handle_pragma(self):
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
        prefix = self.tokens[:self.index]
        suffix = self.tokens[self.index:]
        size = len(tokens)
        self.tokens = prefix + tokens + suffix
        self.len += size
        if before:
            self.index += size

    def remove(self, count, index = None):
        index = index if index else self.index
        assert index <= self.index
        del self.tokens[index-count:index]
        self.len -= count
        self.index -= count

    def substitute(self):
        def subst(token):
            if token[0] not in ['identifier', 'keyword']:
                return None
            substitutions = []
            definitions = self.definitions.get(token[1])
            if not definitions:
                return None
            for definition in definitions:
                tokens = []
                for token in (definition or []):
                    tokens += subst(token) or [token]
                if tokens:
                    substitutions.append(tokens)
            if len(substitutions) > 1:
                return [('any', substitutions)]
            elif len(substitutions) == 1:
                return substitutions[0]
            return []

        result = subst(self.next())
        if result is not None:
            self.remove(1)
            self.insert(result)

    def preprocess(self, data):
        super().reset()
        self.conditions = []
        self.depth = 0
        self.remove_block = None
        self.file = ''
        self.insert(data)

        # String combination not implemented
        # Stringification and concatenation not implemented

        while self.has_next() and not self.has_error:
            if self.consume_directive('#'):
                self.parse_directive()
                continue

            if self.remove_block:
                self.next()
                continue

            if self.peek_type() in ['identifier', 'keyword']:
                self.substitute()
                continue

            self.bump()

        return self

    def __str__(self):
        tokens = self.tok_seq(self.tokens)
        definitions = '\n'.join(f'{d[0]}: {self.tok_seq_list(d[1])}' \
            for d in self.definitions.items())
        return f'\n===== TOKENS =====\n{tokens}\n\n===== DEFINITIONS =====\n{definitions}\n'
