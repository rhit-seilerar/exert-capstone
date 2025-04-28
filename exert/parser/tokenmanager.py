from typing import NoReturn
from exert.utilities.types.global_types import TokenType

def tok_str(token: TokenType,
            newlines: bool = False) -> str:
    n = token

    if len(token) == 2:
        n = token + ('',)

    assert len(n) != 2
    string = '<NONE> ' if n is None \
        else n[1] if n[0] == 'directive' \
        else f'{n[1]}\n' if n[0] == 'operator' and n[1] in [';', '{', '}'] \
        else f'{n[1]} ' if n[0] == 'operator' \
        else f'{n[1]} ' if n[0] in ['keyword', 'identifier'] \
        else f'{n[1]}{n[2]} ' if n[0] == 'integer' \
        else f'{n[2]}{n[1]}{">" if n[2] == "<" else n[2]} ' if n[0] == 'string' \
        else f'<ANY {n[1]}>[{len(n[2])}]{{ {", ".join(str(v) for v in n[2])} }} ' \
            if n[0] == 'any' \
        else str(n[1])
    assert isinstance(string, str)
    if newlines:
        return string

    assert isinstance(string, str)
    return string.replace('\n', ' ')

def tok_seq(tokens: list[TokenType],
            newlines: bool = False) -> str:
    return ''.join(tok_str(n, newlines) for n in tokens).strip() \
        if isinstance(tokens, list) else tokens

def mk_int(num: int, suffix: str = '') -> TokenType:
    return ('integer', num, suffix)

def mk_id(sym: str | int) -> TokenType:
    return ('identifier', sym)

def mk_kw(sym: str) -> TokenType:
    return ('keyword', sym)

def mk_op(op: str) -> TokenType:
    return ('operator', op)

def mk_str(string:str, suffix: str = '"') -> TokenType:
    return ('string', string, suffix)

class TokenManager:
    def __init__(self, tokens: (list[TokenType] | None) = None):
        self.reset()
        if tokens is not None:
            self.tokens = tokens
            self.len = len(tokens)

    def reset(self) -> None:
        self.has_error = False
        self.tokens = []
        self.index = 0
        self.len = 0
        self.tokens_consumed = 0
        self.tokens_added = 0
        self.progress_counter = 0

    def has_next(self) -> bool:
        return self.index < self.len

    def bump(self) -> None:
        self.tokens_consumed += 1
        self.index += 1

    def peek(self, offset: int = 0) -> (TokenType | None):
        if 0 <= self.index + offset and self.index + offset < self.len:
            return self.tokens[self.index+offset]
        return None

    def peek_type(self, offset: int = 0) -> (str | None):
        return tok[0] if (tok := self.peek(offset)) else None

    def next(self, offset: int = 0) -> (TokenType | None):
        if (token := self.peek(offset)):
            self.bump()
            return token
        return None

    def consume_type(self, typ: str) -> (TokenType | None):
        return self.next() if (token := self.peek()) and token[0] == typ else None

    def consume(self, token: TokenType) -> (TokenType | None):
        if self.peek() == token:
            return self.next()
        return None

    def consume_directive(self, name: str) -> (TokenType | None):
        return self.consume(('directive', name))

    def consume_operator(self, name: str) -> (TokenType | None):
        return self.consume(('operator', name))

    def consume_keyword(self, name: str) -> (TokenType | None):
        return self.consume(('keyword', name))

    def consume_identifier(self, name: str) -> (TokenType | None):
        return self.consume(('identifier', name))

    def parse_identifier(self) -> (str | int):
        if (token := self.consume_type('identifier')):
            return token[1]
        return ''

    def parse_ident_or_keyword(self) -> str:
        if (self.peek_type() in ['identifier', 'keyword']):
            res = self.next()
            assert res is not None
            assert isinstance(res[1], str)
            return res[1]
        return ''

    def print_current(self, width: int = 5, fancy_print: bool = True) -> str:
        low = max(self.index - width, 0)
        high = min(self.index + width + 1, self.len + 1)
        context = self.tokens[low:high]
        ctx_str = ''
        offset = ''
        for i in range(low, high):
            idx = i - low
            addend = 'EOF'
            if i < self.len:
                if fancy_print:
                    addend = tok_str(context[idx], newlines = True)
                else:
                    addend = str(context[idx])
            addend = addend.replace('\n', '\\n')
            if i == self.index:
                offset = ' ' * len(ctx_str) + '^' * len(addend)
            ctx_str += addend
        out = ctx_str + '\n' + offset
        print(out)
        return out

    def print_progress(self) -> str:
        self.progress_counter += 1
        if self.progress_counter % 2000 == 0:
            out = f'Processed {self.tokens_consumed} of {self.tokens_added} tokens ' \
                f'({self.tokens_consumed / self.tokens_added * 100:.2f}%) ' \
                f'with a running buffer ({self.index} / {self.len})'
            print(out)
            self.progress_counter = 0
            return out
        return ''

    def err(self, *message: object) -> NoReturn:
        print(*message)
        self.print_current()
        assert False
