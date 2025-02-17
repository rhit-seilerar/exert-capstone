from exert.utilities.debug import dprint

def tok_str(token, newlines = False):
    n = token
    string = '#endif\n' if n == ('optional', None) \
        else f'#if {n[1]}\n' if n[0] == 'optional' \
        else '#' if n[0] == 'directive' \
        else f'<{n[1]}> ' if n[0] == 'string' and n[2] == '<' \
        else f'{n[2]}"{n[1]}" ' if n[0] == 'string' \
        else f'{n[1]}\n' if n[0] == 'operator' and n[1] in [';', '{', '}'] \
        else f'{n[1]} ' if n[0] == 'operator' \
        else f'{n[1]} ' if n[0] in ['keyword', 'identifier', 'integer', 'string'] \
        else f'<ANY>{tok_seq_list(n[1])} ' if n[0] == 'any' \
        else str(n[1])
    if newlines:
        return string
    return string.replace('\n', ' ')

def tok_seq(tokens, newlines = False):
    return ''.join(tok_str(n, newlines) for n in tokens).strip() \
        if isinstance(tokens, list) else tokens

def tok_seq_list(ls, newlines = False):
    if isinstance(ls, set) or isinstance(ls, list):
        return f'[ {", ".join(tok_seq(t, newlines).strip() for t in ls)} ]'
    return ls

class TokenManager:
    def __init__(self):
        self.reset()

    def reset(self):
        self.has_error = False
        self.tokens = []
        self.index = 0
        self.len = 0

    def has_next(self):
        return self.index < self.len

    def bump(self):
        dprint(6, '--Bumping')
        self.index += 1

    def peek(self, offset = 0):
        if self.index + offset < self.len:
            dprint(6, '--Peek:', self.tokens[self.index+offset])
            return self.tokens[self.index+offset]
        return None

    def peek_type(self, offset = 0):
        return tok[0] if (tok := self.peek(offset)) else None

    def next(self, offset = 0):
        if (token := self.peek(offset)):
            self.bump()
            return token
        return None

    def consume_type(self, typ):
        return self.next() if (token := self.peek()) and token[0] == typ else None

    def consume(self, token):
        if self.peek() == token:
            return self.next()
        return None

    def consume_directive(self, name):
        return self.consume(('directive', name))

    def consume_operator(self, name):
        return self.consume(('operator', name))

    def consume_keyword(self, name):
        return self.consume(('keyword', name))

    def consume_identifier(self, name):
        return self.consume(('identifier', name))

    def consume_integer(self, name):
        return self.consume(('integer', name))

    def parse_identifier(self):
        if (token := self.consume_type('identifier')):
            return token[1]
        return ''

    def parse_ident_or_keyword(self):
        if (self.peek_type() in ['identifier', 'keyword']):
            return self.next()[1]
        return ''

    def print_current(self):
        low = max(self.index - 5, 0)
        high = min(self.index + 6, self.len+1)
        context = self.tokens[low:high]
        ctx_str = ''
        offset = ''
        for i in range(low, high):
            idx = i - low
            addend = 'EOF' if i == self.len else tok_str(context[idx]) \
                .replace('\n', '\\n')
            if i == self.index:
                offset = ' ' * len(ctx_str) + '^' * len(addend)
            ctx_str += addend
        print(ctx_str)
        print(offset)

    def err(self, *message):
        print(*message)
        self.print_current()
        assert False
        return None
