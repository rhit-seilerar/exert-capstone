from exert.parser.tokenizer import Tokenizer
from exert.parser.tokenmanager import TokenManager, mk_id, mk_kw, mk_op, mk_int
from exert.parser.substitute import substitute, parse_macro
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.defmap import DefMap
from exert.utilities.types.global_types import TokenType

TK = Tokenizer()

def test_substitute_parse_macro_empty() -> None:
    tm = TokenManager([])
    dm = DefMap(None)
    assert parse_macro(tm, dm) == (None, None)

def test_substitute_parse_macro_non_identifier() -> None:
    tm = TokenManager([mk_int(3)])
    dm = DefMap(None)
    assert parse_macro(tm, dm) == (None, None)

def test_substitute_parse_macro_undefined() -> None:
    tm = TokenManager([mk_id('abc')])
    dm = DefMap(None, initial = {'abc': Def()})
    assert parse_macro(tm, dm) == (None, None)
    dm = DefMap(None, initial = {'abc': Def(undefined = True)})
    assert parse_macro(tm, dm) == (None, None)

def test_substitute_parse_macro_variable() -> None:
    tm = TokenManager(TK.tokenize('abc()'))
    dm = DefMap(None, initial = {'abc': Def(DefOption([mk_id('def')]))})
    assert parse_macro(tm, dm) == (mk_id('abc'), None)
    assert tm.next() == mk_op('(')

def test_substitute_parse_macro_function_no_parens() -> None:
    tm = TokenManager(TK.tokenize('none'))
    dm = DefMap(None, initial = {'none': Def(DefOption([], []))})
    assert parse_macro(tm, dm) == (None, None)
    assert tm.next() == mk_id('none')

def test_substitute_parse_macro_function_no_args() -> None:
    tm = TokenManager(TK.tokenize('none()'))
    dm = DefMap(None, initial = {'none': Def(DefOption([], []))})
    assert parse_macro(tm, dm) == (mk_id('none'), [])
    assert not tm.has_next()

def test_substitute_parse_macro_function_one_arg() -> None:
    tm = TokenManager(TK.tokenize('one(1)'))
    dm = DefMap(None, initial = {'one': Def(DefOption([], ['a']))})
    assert parse_macro(tm, dm) == (mk_id('one'), [[mk_int(1)]])
    assert not tm.has_next()

def test_substitute_parse_macro_function_several_args() -> None:
    tm = TokenManager(TK.tokenize('multi(1, (2), 3)'))
    dm = DefMap(None, initial = {'multi': Def(DefOption([], ['a', 'b', 'c']))})
    assert parse_macro(tm, dm) == (mk_id('multi'), [[mk_int(1)], TK.tokenize('(2)'), [mk_int(3)]])
    assert not tm.has_next()

def test_substitute_parse_macro_function_mismatched_parens() -> None:
    tm = TokenManager(TK.tokenize('multi(1, ((2), 3)'))
    dm = DefMap(None, initial = {'multi': Def(DefOption([], ['a', 'b', 'c']))})
    assert parse_macro(tm, dm) == (None, None)
    assert tm.has_next()

def test_substitute_parse_macro_function_vararg_not() -> None:
    tm = TokenManager(TK.tokenize('not(1, 2)'))
    dm = DefMap(None, initial = {'not': Def(DefOption([], ['a']))})
    assert parse_macro(tm, dm) == (mk_id('not'), [TK.tokenize('1, 2')])
    assert not tm.has_next()

def test_substitute_parse_macro_function_vararg_only() -> None:
    tm = TokenManager(TK.tokenize('only(1, 2, 3)'))
    dm = DefMap(None, initial = {'only': Def(DefOption([], ['__VA_ARGS__']))})
    assert parse_macro(tm, dm) == (mk_id('only'), [TK.tokenize('1, 2, 3')])
    assert not tm.has_next()

def test_substitute_parse_macro_function_vararg_combo() -> None:
    tm = TokenManager(TK.tokenize('combo(1, 2, 3)'))
    dm = DefMap(None, initial = {'combo': Def(DefOption([], ['a', '__VA_ARGS__']))})
    assert parse_macro(tm, dm) == (mk_id('combo'), [[mk_int(1)], TK.tokenize('2, 3')])
    assert not tm.has_next()

def test_substitute_empty() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager([])
    dm = DefMap(None)
    assert substitute(tm, dm, keys = keys) == []
    assert not keys

def test_substitute_not_found() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager([mk_id('var')])
    dm = DefMap(None)
    assert substitute(tm, dm, keys = keys) == [mk_id('var')]
    assert not keys

def test_substitute_variable() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager([mk_id('var')])
    dm = DefMap(None, initial = {'var': Def(DefOption([mk_op(';')]))})
    assert substitute(tm, dm, keys = keys) == [mk_op(';')]
    assert keys == {mk_id('var')}

def test_substitute_more() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager(TK.tokenize('NOTHING int a = 0;'))
    dm = DefMap(None, initial = {'NOTHING': Def(DefOption([]))})
    assert substitute(tm, dm, keys = keys) == []
    assert tm.peek() == mk_kw('int')
    assert keys == {mk_id('NOTHING')}

def test_substitute_no_repeat_expansion() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager([mk_id('var')])
    dm = DefMap(None, initial = {'var': Def(DefOption([mk_id('var')]))})
    assert substitute(tm, dm, keys = keys) == [mk_id('var')]
    assert keys == {mk_id('var')}

def test_substitute_no_repeat_expansion_pair() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager([mk_id('var1')])
    dm = DefMap(None, initial = {
        'var1': Def(DefOption([mk_id('var2')])),
        'var2': Def(DefOption([mk_id('var1')]))
    })
    assert substitute(tm, dm, keys = keys) == [mk_id('var1')]
    assert keys == {mk_id('var1'), mk_id('var2')}

def test_substitute_expand_repeat_args() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager([mk_id('var1')])
    dm = DefMap(None, initial = {
        'var1': Def(DefOption([mk_id('var2'), mk_id('var2')])),
        'var2': Def(DefOption([mk_id('var1')]))
    })
    assert substitute(tm, dm, keys = keys) == [mk_id('var1'), mk_id('var1')]
    assert keys == {mk_id('var1'), mk_id('var2')}

def test_substitute_undefined() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager([mk_id('var')])
    dm = DefMap(None, initial = {'var': Def(undefined = True)})
    assert substitute(tm, dm, keys = keys) == [mk_id('var')]
    assert keys == {mk_id('var')}

def test_substitute_unsure() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager([mk_id('var')])
    opt = DefOption([mk_int(1)])
    dm = DefMap(None, initial = {'var': Def(opt, undefined = True)})
    assert substitute(tm, dm, keys = keys) == [('any', 'var', {opt, DefOption([mk_id('var')])})]
    assert keys == {mk_id('var')}

def test_substitute_multiple_results() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager([mk_id('var')])
    options = {DefOption([mk_int(1)]), DefOption([mk_int(2)])}
    dm = DefMap(None, initial = {'var': Def(*options)})
    assert substitute(tm, dm, keys = keys) == [('any', 'var', options)]
    assert keys == {mk_id('var')}

def test_substitute_no_results() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager([mk_id('var')])
    dm = DefMap(None, initial = {'var': Def(defined = True)})
    assert substitute(tm, dm, keys = keys) == []
    assert keys == {mk_id('var')}

def test_substitute_function() -> None:
    keys: set[TokenType] = set()
    tm = TokenManager([mk_id('var(1, 2, 3)')])
    opt = DefOption(TK.tokenize('__VA_ARGS__ a'), ['a', '__VA_ARGS__'])
    dm = DefMap(None, initial = {'var': Def(opt)})
    assert substitute(tm, dm, keys = keys) == TK.tokenize('2, 3 1')
    assert keys == {mk_id('var')}
