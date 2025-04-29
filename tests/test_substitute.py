from exert.parser.tokenizer import Tokenizer
from exert.parser.tokenmanager import TokenManager, mk_id, mk_kw, mk_op, mk_int
from exert.parser.substitute import substitute, parse_macro
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.defmap import DefMap
from exert.parser.defstate import DefState

TK = Tokenizer()

def test_substitute_parse_macro_empty():
    tm = TokenManager([])
    dm = DefMap(None)
    assert parse_macro(tm, dm) == (None, None)

def test_substitute_parse_macro_non_identifier():
    tm = TokenManager([mk_int(3)])
    dm = DefMap(None)
    assert parse_macro(tm, dm) == (None, None)

def test_substitute_parse_macro_undefined():
    tm = TokenManager([mk_id('abc')])
    dm = DefMap(None, initial = {'abc': Def()})
    assert parse_macro(tm, dm) == (None, None)
    dm = DefMap(None, initial = {'abc': Def(undefined = True)})
    assert parse_macro(tm, dm) == (None, None)

def test_substitute_parse_macro_variable():
    tm = TokenManager([mk_id('abc')])
    dm = DefMap(None, initial = {'abc': Def(DefOption([mk_id('def')]))})
    assert parse_macro(tm, dm) == (mk_id('abc'), None)

def test_substitute_empty():
    keys = set()
    tm = TokenManager([])
    dm = DefMap(None)
    assert substitute(tm, dm, keys = keys) == []
    assert not keys

def test_substitute():
    defstate = DefState(64)

    nosubst = TK.tokenize('static int a = b;')
    tokmgr = TokenManager(nosubst)
    assert defstate.substitute(tokmgr) == [mk_kw('static')]
    assert tokmgr.index == 1

    defstate.on_define('STRING', [('string', '%d', '"')])
    assert defstate.substitute(mk_id('STRING')) == [('string', '%d', '"')]

    defstate.on_undef('STRING')
    assert defstate.substitute(mk_id('STRING')) == [mk_id('STRING')]

    defstate.on_undef('STRING')
    defstate.on_define('STRING', [mk_id('SECOND')])
    defstate.on_define('SECOND', [mk_id('THIRD')])
    assert defstate.substitute(mk_id('STRING')) == [mk_id('THIRD')]

    defstate.on_undef('SECOND')
    defstate.on_define('SECOND', [mk_id('STRING')])
    assert defstate.substitute(mk_id('STRING')) == [mk_id('STRING')]

    defstate.on_undef('STRING')
    defstate.on_define('STRING', [])
    assert defstate.substitute(mk_id('STRING')) == []

    defstate.on_undef('STRING')
    assert defstate.layers[-1].current is not None
    defstate.layers[-1].current['STRING'] = Def()
    assert defstate.substitute(mk_id('STRING')) == [mk_id('STRING')]
    defstate.layers[-1].current['STRING'] = Def(undefined = True)
    assert defstate.substitute(mk_id('STRING')) == [mk_id('STRING')]
    defstate.layers[-1].current['STRING'] = Def(defined = True)
    assert defstate.substitute(mk_id('STRING')) == [('any', 'STRING', set())]
    defstate.on_undef('SECOND')
    defstate.on_undef('THIRD')
    defstate.layers[-1].current['STRING'] = Def(
        DefOption([('string', '%d', '"')]),
        DefOption([mk_id('SECOND'), mk_id('THIRD')]),
        undefined = True,
        defined = True)
    result = defstate.substitute(mk_id('STRING'))
    assert len(result) == 1
    assert result[0] is not None
    assert len(result[0]) > 2
    assert result[0][0] == 'any'
    assert result[0][1] == 'STRING'
    assert isinstance(result[0][2], set)
    opts = [opt.tokens for opt in result[0][2]]
    assert [('string', '%d', '"')] in opts
    assert [mk_id('STRING')] in opts
    assert [mk_id('SECOND'), (mk_id('THIRD'))] in opts

    defstate.layers[-1].current['SECOND'] = Def(
        DefOption([mk_int(0)]),
        DefOption([mk_int(1)]),
    )

    new_result = defstate.substitute(mk_id('SECOND'))
    assert new_result[0] is not None
    assert new_result[0][0] == 'any'

def test_substitute_func():
    defstate = DefState(64)
    defstate.on_define('DEFN', [mk_id('a'), mk_op('*'), mk_int(3)], ['a'])

    assert defstate.substitute(TokenManager(TK.tokenize('DEFN(1)'))) == \
        TK.tokenize('1 * 3')
