class Tokenizer:
    def __init__(self):
        self.keywords = [
            'void', 'char', 'int', 'float', 'double',
            'signed', 'unsigned', 'short', 'long',
            'enum', 'struct', 'union',
            'if', 'else', 'switch', 'case', 'default', 'goto',
            'for', 'while', 'do', 'continue', 'break',
            'const', 'volatile', 'auto', 'static', 'extern', 'register',
            'inline', 'return', 'restrict',
            'typedef', 'sizeof',
            '_Alignas', '_Alignof', '_Atomic', '_Bool', '_Complex', '_Generic',
            '_Imaginary', '_Noreturn', '_Static_assert', '_Thread_local',
        ]

    def has_next(self):
        return self.index < self.len

    def peek(self, size = 1, offset = 0):
        if size == 1 and self.index + offset < self.len:
            return self.data[self.index + offset]
        return self.data[self.index+offset:self.index+offset+size]

    def bump(self, dist = 1):
        self.index += dist

    def consume(self, *strings):
        for string in strings:
            dist = len(string)
            if self.peek(dist) == string:
                self.bump(dist)
                return string
        return None

    def consume_comment(self):
        if self.consume('//'):
            while not self.consume('\r\n', '\n', ''):
                if not self.consume('\\\r\n', '\\\n'):
                    self.bump()
            return True
        elif self.consume('/*'):
            while not self.consume('*/'):
                assert self.has_next(), \
                    "[Tokenizer::Comment] Reached EOF without finding the closing '*/'"
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
            return ('identifier', value)
        return None

    def parse_integer(self):
        start = self.index

        sign = -1 if self.consume('+', '-') == '-' else 1

        digits = '0123456789'
        radix = 10
        if self.consume('0b', '0B'):
            digits = '01'
            radix = 2
        elif self.consume('0x', '0X'):
            digits = '0123456789abcdefABCDEF'
            radix = 16
        elif self.peek() == '0' and self.peek(1, 1).isdigit():
            self.bump()
            digits = '01234567'
            radix = 8

        if not self.peek().isdigit():
            self.index = start
            return None

        num = 0
        while (d := self.peek().lower()) in digits:
            v = ord(d) - ord('a') if d.isalpha() else ord(d) - ord('0')
            num = num * radix + v
            self.bump()
        num = num * sign

        if self.peek().isalnum():
            if not (suffix := self.consume('u', 'U', 'l', 'L', 'll', 'LL')):
                self.index = start
                return None
            return ('integer', num, suffix)

        return ('integer', num, '')

    def parse_string(self):
        # String combination not implemented
        old = self.index
        modifier = self.consume('u8', 'u', 'U', 'L')
        delim = self.consume('"')
        if not delim and self.in_directive:
            if self.consume('<'):
                modifier = '<'
                delim = '>'
        if delim:
            start = self.index
            while not self.consume(delim):
                assert self.has_next(), \
                    '[Tokenizer::String] Reached EOF without finding the closing quation mark'
                if not self.consume('\\"'):
                    self.bump()
            return ('string', self.data[start:self.index-1], modifier)
        self.index = old
        return None

    def parse_operator(self):
        if (op3 := self.peek(3)) in ['||=', '&&=', '<<=', '>>=', '...']:
            self.bump(3)
            return ('operator', op3)
        if (op2 := self.peek(2)) in ['++', '--', '+=', '-=', '*=', '/=',
                '%=', '&=', '|=', '^=', '||', '&&', '//', '/*', '*/', '##',
                '<<', '>>', '<=', '>=', '!=', '==', '->']:
            self.bump(2)
            return ('operator', op2)
        if (op1 := self.peek(1)) in '-=[]\\;,./~!#%^&*()+{}|:<>?':
            self.bump()
            if self.can_be_directive and op1 == '#':
                self.in_directive = True
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

    def tokenize(self, data):
        self.data = data
        self.len = len(data)
        self.index = 0
        self.in_directive = False
        self.can_be_directive = True
        self.tokens = []

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
