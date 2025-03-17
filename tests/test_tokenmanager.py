from exert.parser.tokenmanager import tok_str, tok_seq, TokenManager
from exert.parser.definitions import Def, DefOption

def test_tok_str():
    assert tok_str(('optional', 'if', '!A && B + C')) == '#if !A && B + C '
    assert tok_str(('optional', 'else', '')) == '#else  '
    assert tok_str(('optional', 'else', ''), True) == '#else \n'
    assert tok_str(('optional', 'endif', '')) == '#endif  '
    assert tok_str(('directive', '#')) == '#'
    assert tok_str(('keyword', 'abcdef')) == 'abcdef '
    assert tok_str(('identifier', 'ghi')) == 'ghi '
    assert tok_str(('integer', '1234', 'ull')) == '1234ull '
    assert tok_str(('string', 'abc', '"')) == '"abc" '
    assert tok_str(('string', 'abc', '<')) == '<abc> '
    assert tok_str(('operator', '<<=')) == '<<= '
    assert tok_str(('operator', ';')) == '; '
    assert tok_str(('operator', ';'), True) == ';\n'
    assert tok_str(('any', [
        Def(DefOption([('integer', 1, 'u')])),
        Def(DefOption([('string', '123', '"')]))
    ])) == '<ANY>{{ 1u }, { "123" }} '

def test_tok_seq():
    assert tok_seq([('integer', 1, 'u'), ('string', 'abc', '<')]) == '1u <abc>'
    assert tok_seq([('optional', 'if', 'a || b'), ('optional', 'endif', '')], False) \
        == '#if a || b #endif'
    assert tok_seq([('optional', 'if', 'a || b'), ('optional', 'endif', '')], True) \
        == '#if a || b\n#endif'

def test_reset():
    mgr = TokenManager()
    mgr.has_error = 999
    mgr.tokens = 999
    mgr.index = 999
    mgr.len = 999
    mgr.tokens_consumed = 999
    mgr.tokens_added = 999
    mgr.progress_counter = 999
    mgr.reset()
    assert not mgr.has_error
    assert mgr.tokens == []
    assert mgr.index == 0
    assert mgr.len == 0
    assert mgr.tokens_consumed == 0
    assert mgr.tokens_added == 0
    assert mgr.progress_counter == 0

def test():
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
