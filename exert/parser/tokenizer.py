from typing import Any, Optional
import exert.parser.tokenmanager as tm

class Tokenizer:
    def __init__(self):
        self.keywords = [
            'alignas', 'alignof', 'auto', 'bool', 'break', 'case', 'char',
            'const', 'constexpr', 'continue', 'default', 'do', 'double',
            'else', 'enum', 'extern', 'false', 'float', 'for', 'goto', 'if',
            'inline', 'int', 'long', 'nullptr', 'register', 'restrict',
            'return', 'short', 'signed', 'sizeof', 'static', 'static_assert',
            'struct', 'switch', 'thread_local', 'true', 'typedef', 'typeof',
            'typeof_unqual', 'union', 'unsigned', 'void', 'volatile', 'while',
            '_Atomic', '_BitInt', '_Complex', '_Decimal128', '_Decimal32',
            '_Decimal64', '_Generic', '_Imaginary', '_Noreturn'
        ]

    def has_next(self):
        return self.index < self.len

    def peek(self, size: int = 1, offset: int = 0):
        if size == 1 and self.index + offset < self.len:
            return self.data[self.index + offset]
        return self.data[self.index+offset:self.index+offset+size]

    def bump(self, dist: int = 1):
        self.index += dist

    def consume(self, *strings: str):
        for string in strings:
            dist = len(string)
            if self.peek(dist) == string:
                self.bump(dist)
                return string
        return None

    def consume_comment(self):
        if self.consume('//'):
            while self.has_next() and not self.peek() == '\n' \
                and not self.peek(2) == '\r\n':
                if not self.consume('\\\r\n', '\\\n'):
                    self.bump()
            return True
        if self.consume('/*'):
            while not self.consume('*/'):
                assert self.has_next(), \
                    "Reached EOF without finding the closing '*/'"
                self.bump()
            return True
        return False

    def parse_identifier(self):
        start = self.index
        if self.peek().isalpha() or self.peek() == '_':
            self.bump()
            while self.peek().isalnum() or self.peek() == '_':
                self.bump()
            value = self.data[start:self.index]
            if value in self.keywords:
                return ('keyword', value)
            if len(self.tokens) > 0 and self.in_directive \
                and self.tokens[-1] == tm.mk_id('define') and self.peek() == '(':
                self.next_parenthesis_is_directive = True
            return ('identifier', value)
        return None

    def parse_integer(self):
        start = self.index

        digits = '0123456789'
        radix = 10
        if self.consume('0b', '0B'):
            digits = '01'
            radix = 2
        elif self.consume('0x', '0X'):
            digits = '0123456789abcdef'
            radix = 16
        elif self.peek() == '0' and self.peek(1, 1).isdigit():
            self.bump()
            digits = '01234567'
            radix = 8

        if not self.peek().lower() in digits:
            self.index: int = start
            return None

        num = 0
        while self.has_next() and (d := self.peek().lower()) in digits:
            v = ord(d) - ord('a') + 10 if d.isalpha() else ord(d) - ord('0')
            num = num * radix + v
            self.bump()

        if self.peek().isalnum() or self.peek() == '_':
            if not (suffix := self.consume('u', 'U', 'l', 'L', 'll', 'LL')) \
                or self.peek().isalnum() or self.peek() == '_':
                self.index = start
                return None
            return ('integer', num, suffix.lower())

        return ('integer', num, '')

    def parse_string(self):
        old = self.index
        modifier = self.consume('u8', 'u', 'U', 'L') or ''
        delim = self.consume('"')
        if not delim and self.in_directive and self.tokens[-1] == ('identifier', 'include'):
            if self.consume('<'):
                modifier = '<'
                delim = '>'
        if delim:
            start = self.index
            while self.has_next():
                if self.consume(delim):
                    return ('string', self.data[start:self.index-1], modifier)
                if not self.consume('\\"'):
                    self.bump()
        self.index = old
        return None

    def parse_operator(self):
        if (op3 := self.peek(3)) in ['||=', '&&=', '<<=', '>>=', '...']:
            self.bump(3)
            return ('operator', op3)
        #TODO Alternative operators (<:, :>, etc)
        if (op2 := self.peek(2)) in ['++', '--', '+=', '-=', '*=', '/=',
                '%=', '&=', '|=', '^=', '||', '&&', '//', '/*', '*/', '##',
                '<<', '>>', '<=', '>=', '!=', '==', '->', '::']:
            self.bump(2)
            return ('operator', op2)
        if (op1 := self.peek(1)) in '-=[]\\;,./~!#%^&*()+{}|:<>?':
            self.bump()

            if op1 == '(' and self.next_parenthesis_is_directive:
                self.next_parenthesis_is_directive = False
                return ('directive', '(')

            if self.can_be_directive and op1 == '#':
                self.in_directive: bool = True
                return ('directive', '#')

            return ('operator', op1)
        return None

    def parse_token(self):
        token = None
        token = token or self.parse_identifier()
        # token = token or self.parse_character()
        token = token or self.parse_integer()
        # token = token or self.parse_float()
        token = token or self.parse_string()
        token = token or self.parse_operator()
        return token

    def tokenize(self, data: str):
        self.data = data
        self.len = len(data)
        self.index = 0
        self.in_directive = False
        self.can_be_directive = True
        self.next_parenthesis_is_directive = False
        self.tokens: list = []

        while self.has_next():
            if self.consume(' ', '\t'):
                continue

            if self.consume_comment():
                continue

            if self.consume('\\\n', '\\\r\n'):
                continue
            if (newline := self.consume('\n', '\r\n')):
                if self.in_directive:
                    self.can_be_directive = True
                    self.in_directive = False
                    self.tokens.append(('newline', newline))
                else:
                    self.can_be_directive = True
                continue

            token = self.parse_token()
            self.can_be_directive = False
            if token:
                self.tokens.append(token)
            else:
                self.bump()

        if self.in_directive:
            self.tokens.append(('newline', ''))

        return self.tokens
