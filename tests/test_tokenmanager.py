from exert.parser import tokenmanager as tm
from exert.parser.tokenmanager import tok_str, TokenManager
from exert.parser.defoption import DefOption

def test_mk() -> None:
    assert tm.mk_op('&!=') == ('operator', '&!=')
    assert tm.mk_id('hello') == ('identifier', 'hello')
    assert tm.mk_int(123) == ('integer', 123, '')
    assert tm.mk_int(465, 'ull') == ('integer', 465, 'ull')
    assert tm.mk_str('abc') == ('string', 'abc', '"')
    assert tm.mk_str('abc', '<') == ('string', 'abc', '<')

def test_tok_str() -> None:
    assert tok_str(('directive', '#')) == '#'
    assert tok_str(('keyword', 'abcdef')) == 'abcdef '
    assert tok_str(('identifier', 'ghi')) == 'ghi '
    assert tok_str(('integer', '1234', 'ull')) == '1234ull '
    assert tok_str(('string', 'abc', '"')) == '"abc" '
    assert tok_str(('string', 'abc', '<')) == '<abc> '
    assert tok_str(('operator', '<<=')) == '<<= '
    assert tok_str(('operator', ';')) == '; '
    assert tok_str(('operator', ';'), True) == ';\n'
    assert tok_str(('any', 'a2', {
        DefOption([('integer', 1, 'u')]),
        DefOption([('string', '123', '"')])
    })) in ['<ANY a2>[2]{ $1u, $"123" } ', '<ANY a2>[2]{ $"123", $1u } ']

def test_reset() -> None:
    mgr = TokenManager()
    mgr.has_error = True
    mgr.tokens = [("Howdy", "Howdy")]
    mgr.index = 999
    mgr.len = 999
    mgr.tokens_consumed = 999
    mgr.tokens_added = 999
    mgr.progress_counter = 999
    mgr.reset()
    assert not mgr.has_error
    assert not mgr.tokens
    assert mgr.index == 0
    assert mgr.len == 0
    assert mgr.tokens_consumed == 0
    assert mgr.tokens_added == 0
    assert mgr.progress_counter == 0

def test() -> None:
    mgr = TokenManager()
    mgr.tokens = [
        ('keyword', 'if'),
        ('operator', '('),
        ('identifier', 'strlen'),
        ('operator', '('),
        ('string', 'a', '"'),
        ('operator', ')'),
        ('operator', '=='),
        ('integer', 1, ''),
        ('operator', ')'),
        ('operator', '{'),
        ('operator', '}')
    ]
    mgr.len = len(mgr.tokens)
    mgr.tokens_added = len(mgr.tokens)
    assert mgr.print_progress() == ''
    mgr.progress_counter = 1999
    assert mgr.print_progress() == \
        f'Processed 0 of {mgr.len} tokens (0.00%) with a running buffer' \
        f' (0 / {mgr.len})'
    assert mgr.print_current(width = 2) == 'if ( strlen \n^^^'
    assert mgr.print_current(width = 2, fancy_print = False) == \
        "('keyword', 'if')('operator', '(')('identifier', 'strlen')\n^^^^^^^^^^^^^^^^^"

    try:
        mgr.err('Hello there!')
    except AssertionError:
        pass

    assert mgr.peek() == ('keyword', 'if')
    assert mgr.next() == ('keyword', 'if')
    assert mgr.next() == ('operator', '(')
    assert mgr.peek() == ('identifier', 'strlen')
    assert mgr.peek(-1) == ('operator', '(')
    assert mgr.peek(-100) is None
    assert mgr.peek(100) is None
    assert mgr.next(100) is None
    assert mgr.peek_type() == 'identifier'
    assert mgr.consume_type('integer') is None
    assert mgr.consume_type('identifier') == ('identifier', 'strlen')
    assert mgr.peek_type() == 'operator'

    mgr.index = 0
    assert mgr.consume_directive('if') is None
    assert mgr.consume_keyword('typedef') is None
    assert mgr.consume_keyword('if') == ('keyword', 'if')
    assert mgr.consume_operator(')') is None
    assert mgr.consume_operator('(') == ('operator', '(')
    assert mgr.consume_identifier('strlen') == ('identifier', 'strlen')
    assert mgr.consume_operator('(') == ('operator', '(')
    assert mgr.consume(('string', 'a', '"')) is not None
    assert mgr.consume_operator(')') == ('operator', ')')
    assert mgr.consume_operator('==') == ('operator', '==')
    assert mgr.consume(('integer', 1, '')) is not None
    assert mgr.consume_operator(')') is not None
    assert mgr.consume_operator('{') is not None
    assert mgr.has_next()
    assert mgr.consume_operator('}') is not None
    assert not mgr.has_next()

    mgr.index = 0
    assert mgr.parse_identifier() == ''
    assert mgr.parse_ident_or_keyword() == 'if'
    assert mgr.parse_ident_or_keyword() == ''
    mgr.index += 1
    assert mgr.parse_ident_or_keyword() == 'strlen'
    mgr.index -= 1
    assert mgr.parse_identifier() == 'strlen'
