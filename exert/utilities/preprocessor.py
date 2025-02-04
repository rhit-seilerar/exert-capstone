import os
from exert.utilities.tokenmanager import TokenManager

class Preprocessor(TokenManager):
    def __init__(self, tokenizer, includes):
        super().__init__()
        self.tokenizer = tokenizer
        self.includes = includes
        self.definitions = dict()

    def load_file(self, path, is_relative):
        includes = [os.path.dirname(self.file)] if is_relative else []
        includes += self.includes
        for include in includes:
            load_path = os.path.join(include, path)
            data = self.load_data(load_path)
            print(f'Loading path: {load_path}')
            prefix = f'#line 1 "{load_path}"\n'
            suffix = f'\n#line 1 "{self.file}"\n'
            to_insert = prefix + data + suffix
            self.insert(to_insert)
            return True
        return self.err(f"Failed to include '{path}'")

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
        if not (name := self.parse_identifier()):
            return self.err('#define must be followed by an identifier')
        if not (tokens := self.skip_to_newline(1)):
            return False
        self.definitions[name] = (arr := self.definitions.get(name, list()))
        arr.append(tokens)
        return True

    def handle_undef(self):
        if not self.parse_identifier():
            return self.err('#undef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        return True

    def handle_ifdef(self):
        if not (name := self.parse_identifier()):
            return self.err('#ifdef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        self.push_optional(f'defined({name})')
        return True

    def handle_ifndef(self):
        if not (name := self.parse_identifier()):
            return self.err('#ifndef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        self.push_optional(f'!defined({name})')
        return True

    def handle_if(self):
        if not (tokens := self.skip_to_newline()):
            return False
        self.push_optional(' '.join(str(n[1]) for n in tokens))
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
        # print(f'\n================================================\n'
        #     f'Inserted {size} tokens {"before" if before else "after"}'
        #     f' index {self.index}:\n{" ".join(str(n[1]) for n in tokens)}'
        #     f'\n================================================\n')
        self.tokens = prefix + tokens + suffix
        self.len += size
        if before:
            self.index += size

    def remove(self, count):
        del self.tokens[self.index-count:self.index]
        self.len -= count
        self.index -= count

    def load_data(self, filename):
        try:
            with open(filename, 'r', encoding = 'utf-8') as file:
                data = file.read()
                return data
        except IOError:
            return ''

    def preprocess(self, filename):
        super().reset()
        self.conditions = []
        self.file = ''
        self.load_file(filename, True)

        while self.has_next() and not self.has_error:
            if self.consume(('directive', '#')):
                self.parse_directive()
            else:
                self.bump()

        return self

    def __str__(self):
        return ''.join(
            '#endif\n' if n == ('optional', None)
            else f'#if {n[1]}\n' if n[0] == 'optional'
            else '\n#' if n[0] == 'directive'
            else ';\n' if n == ('operator', ';')
            else f'{n[1]} ' if n[0] == 'operator'
            else f'{n[1]} ' if n[0] in ['keyword', 'identifier', 'integer', 'string']
            else str(n[1])
            for n in self.tokens
        )
