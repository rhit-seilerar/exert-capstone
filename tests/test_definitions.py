from exert.parser.tokenizer import Tokenizer
from exert.parser import tokenmanager as tm
from exert.parser import definitions
from exert.parser.definitions import DefOption, Def, DefMap, DefLayer, DefState

TK = Tokenizer()

def test_substitute():
    defstate = DefState(64)

    nosubst = TK.tokenize('static int a = b;')
    tokmgr = tm.TokenManager(nosubst)
    assert defstate.substitute(tokmgr) == [tm.mk_kw('static')]
    assert tokmgr.index == 1

    defstate.on_define('STRING', [('string', '%d', '"')])
    assert defstate.substitute(tm.mk_id('STRING')) == [('string', '%d', '"')]

    defstate.on_undef('STRING')
    assert defstate.substitute(tm.mk_id('STRING')) == [tm.mk_id('STRING')]

    defstate.on_undef('STRING')
    defstate.on_define('STRING', [tm.mk_id('SECOND')])
    defstate.on_define('SECOND', [tm.mk_id('THIRD')])
    assert defstate.substitute(tm.mk_id('STRING')) == [tm.mk_id('THIRD')]

    defstate.on_undef('SECOND')
    defstate.on_define('SECOND', [tm.mk_id('STRING')])
    assert defstate.substitute(tm.mk_id('STRING')) == [tm.mk_id('STRING')]

    defstate.on_undef('STRING')
    defstate.on_define('STRING', [])
    assert defstate.substitute(tm.mk_id('STRING')) == []

    defstate.on_undef('STRING')
    assert defstate.layers[-1].current is not None
    defstate.layers[-1].current['STRING'] = Def()
    assert defstate.substitute(tm.mk_id('STRING')) == [tm.mk_id('STRING')]
    defstate.layers[-1].current['STRING'] = Def(undefined = True)
    assert defstate.substitute(tm.mk_id('STRING')) == [tm.mk_id('STRING')]
    defstate.layers[-1].current['STRING'] = Def(defined = True)
    assert defstate.substitute(tm.mk_id('STRING')) == [('any', 'STRING', set())]
    defstate.on_undef('SECOND')
    defstate.on_undef('THIRD')
    defstate.layers[-1].current['STRING'] = Def(
        DefOption([('string', '%d', '"')]),
        DefOption([tm.mk_id('SECOND'), tm.mk_id('THIRD')]),
        undefined = True,
        defined = True)
    result = defstate.substitute(tm.mk_id('STRING'))
    assert len(result) == 1
    assert result[0] is not None
    assert len(result[0]) > 2
    assert result[0][0] == 'any'
    assert result[0][1] == 'STRING'
    assert isinstance(result[0][2], set)
    opts = [opt.tokens for opt in result[0][2]]
    assert [('string', '%d', '"')] in opts
    assert [tm.mk_id('STRING')] in opts
    assert [tm.mk_id('SECOND'), (tm.mk_id('THIRD'))] in opts

    defstate.layers[-1].current['SECOND'] = Def(
        DefOption([tm.mk_int(0)]),
        DefOption([tm.mk_int(1)]),
    )

    new_result = defstate.substitute(tm.mk_id('SECOND'))
    assert new_result[0] is not None
    assert new_result[0][0] == 'any'

def test_substitute_func():
    defstate = DefState(64)
    defstate.on_define('DEFN', [tm.mk_id('a'), tm.mk_op('*'), tm.mk_int(3)], ['a'])

    assert defstate.substitute(tm.TokenManager(TK.tokenize('DEFN(1)'))) == \
        TK.tokenize('1 * 3')

def test_defevaluator_none():
    de = definitions.DefEvaluator(64, DefMap(None))
    assert de.evaluate([tm.mk_int(0)]) == (False, False, DefMap(de.defs))
    assert de.evaluate([tm.mk_int(1)]) == (True, True, DefMap(de.defs))
    assert de.evaluate([tm.mk_id('abc')]) == (False, False, DefMap(de.defs))
    assert de.evaluate([tm.mk_id('true')]) == (True, True, DefMap(de.defs))
    de.defs['abc'] = Def(DefOption([tm.mk_int(1)]), undefined = True)
    assert de.evaluate(TK.tokenize('abc == 2')) == (False, False, DefMap(de.defs))

def test_defevaluator_single():
    de = definitions.DefEvaluator(64, DefMap(None))
    de.defs['abc'] = Def(defined = True)
    assert de.evaluate([tm.mk_id('defined'), tm.mk_op('('),
        tm.mk_id('abc'), tm.mk_op(')')]) == \
        (True, True, DefMap(de.defs, initial = {'abc': Def(defined = True)}))
    de.defs['abc'] = Def(DefOption([]), defined = True)
    assert de.evaluate([tm.mk_id('defined'), tm.mk_id('abc')]) == \
        (True, True, DefMap(de.defs, initial = {'abc': Def(DefOption([]), defined = True)}))
    de.defs['abc'] = Def(DefOption([tm.mk_int(3)]), defined = True)
    assert de.evaluate([tm.mk_id('defined'), tm.mk_id('abc')]) == \
        (True, True, DefMap(de.defs, initial = {
            'abc': Def(DefOption([tm.mk_int(3)]), defined = True)}))
    de.defs['abc'] = Def(undefined = True)
    assert de.evaluate([tm.mk_id('defined'), tm.mk_id('abc')]) == \
        (False, False, DefMap(de.defs))

def test_defevaluator_multiple():
    de = definitions.DefEvaluator(64, DefMap(None))
    assert de.evaluate(TK.tokenize('defined abc')) == \
        (True, False, DefMap(de.defs, initial = {'abc': Def(defined = True)}))
    de.defs['abc'] = Def(defined = True, undefined = True)
    assert de.evaluate(TK.tokenize('defined abc')) == \
        (True, False, DefMap(de.defs, initial = {'abc': Def(defined = True)}))
    assert de.evaluate(TK.tokenize('defined abc || !defined abc')) == \
        (True, True, DefMap(de.defs, initial = {
            'abc': Def(defined = True, undefined = True)}))
    de.defs['abc'] = Def(DefOption([tm.mk_int(1)]), DefOption([tm.mk_int(2)]),
        defined = True, undefined = True)
    assert de.evaluate(TK.tokenize('!defined abc || abc == 2')) == \
        (True, False, DefMap(de.defs, initial = {
            'abc': Def(DefOption([tm.mk_int(2)]), undefined = True)}))
    assert de.evaluate(TK.tokenize('abc == 1 || abc == 2')) == \
        (True, False, DefMap(de.defs, initial = {
            'abc': Def(DefOption([tm.mk_int(2)]), DefOption([tm.mk_int(1)]))}))

def test_deflayer_skip_all():
    dl = DefLayer(DefMap(None), 32, True)
    dl.add_map([tm.mk_id('abc')], closing = True)
    assert dl.current == DefMap(None, skipping = True)

def test_deflayer_first():
    parent = DefMap(None, initial = {'abc': Def(DefOption([tm.mk_int(1)]),
        DefOption([tm.mk_int(2)]), undefined = True)})
    dl = DefLayer(parent, 32, False)
    dl.add_map(TK.tokenize('defined abc'))
    assert dl.cond_acc == TK.tokenize('!(defined abc)')
    assert dl.current is not None
    assert dl.current['abc'] == Def(DefOption([tm.mk_int(1)]), DefOption([tm.mk_int(2)]))
    assert not dl.current.skipping
    assert not dl.skip_rest
    assert not dl.closed

    dl = DefLayer(parent, 32, False)
    dl.add_map(TK.tokenize('abc == 3'))
    assert dl.cond_acc == TK.tokenize('!(abc == 3)')
    assert dl.current is not None
    assert dl.current.skipping
    assert not dl.skip_rest
    assert not dl.closed

def test_deflayer_next():
    parent = DefMap(None, initial = {
        'abc': Def(DefOption([tm.mk_int(1)]), DefOption([tm.mk_int(2)]), undefined = True),
        'def': Def(undefined = True)
    })
    dl = DefLayer(parent, 32, False)
    dl.add_map(TK.tokenize('defined abc'))

    dl.add_map(TK.tokenize('!defined abc'))
    assert dl.cond == TK.tokenize('!(defined abc) && (!defined abc)')
    assert dl.cond_acc == TK.tokenize('!(defined abc) && !(!defined abc)')
    assert dl.accumulator['abc'] == Def(DefOption([tm.mk_int(1)]), DefOption([tm.mk_int(2)]))
    assert dl.current is not None
    assert dl.current['abc'] == Def(undefined = True)
    assert not dl.current.skipping
    assert dl.skip_rest
    assert dl.closed

    dl = DefLayer(parent, 32, False)
    dl.add_map(TK.tokenize('1'))
    assert dl.cond_acc == TK.tokenize('!(1)')
    assert dl.current is not None
    assert not dl.current.skipping
    assert dl.skip_rest
    assert dl.closed

def test_defstate():
    ds = DefState(64, initial = {
        'abc': Def(DefOption([tm.mk_int(1)])),
        'def': Def(DefOption([]), undefined = True)
    })
    assert ds.flat_defines() == {'abc': Def(DefOption([tm.mk_int(1)]))}
    assert ds.flat_unknowns() == {'def'}

    ds.on_ifndef('abc')
    assert ds.is_skipping()
    ds.on_elif([tm.mk_id('abc'), tm.mk_op('=='), tm.mk_int(2)])
    assert ds.is_skipping()
    ds.on_else()
    assert ds.substitute(tm.mk_id('abc')) == [tm.mk_int(1)]
    assert ds.get_cond_tokens() == TK.tokenize('!(!defined abc) && !(abc == 2) && (1)')
    assert ds.get_replacements(tm.mk_id('abc')) == {DefOption([tm.mk_int(1)])}
    assert ds.layers[-1].closed
    ds.on_endif()
    assert len(ds.layers) == 1

    ds.on_ifdef('def')
    assert not ds.is_skipping()
    ds.on_elifndef('def')
    assert not ds.is_skipping()
    ds.on_elifdef('abc')
    assert ds.is_skipping()
    ds.on_endif()

def test_defstate_multilayer():
    ds = DefState(64)
    wild_abc = DefOption([('any', 'ABC', set())])
    wild_def = DefOption([('any', 'DEF', set())])
    assert ds.get_replacements(tm.mk_id('ABC')) == {wild_abc}
    ds.on_ifdef('ABC')
    assert ds.get_replacements(tm.mk_id('ABC')) == {wild_abc}
    assert not ds.is_skipping()
    assert not ds.layers[-1].skip_rest
    assert len(ds.layers) == 2
    ds.on_if(TK.tokenize('ABC == 2'))
    assert len(ds.layers) == 3
    # Currently can't make the '==' guarantee with wildcards
    assert ds.get_replacements(tm.mk_id('ABC')) == {wild_abc}
    assert not ds.is_skipping()
    assert not ds.is_guaranteed()
    ds.on_define('DEF', TK.tokenize('1'))
    assert ds.get_replacements(tm.mk_id('DEF')) == {DefOption([tm.mk_int(1)])}
    assert not ds.is_skipping()
    assert not ds.layers[-1].skip_rest
    ds.on_elifdef('DEF')
    assert len(ds.layers) == 3
    assert ds.get_replacements(tm.mk_id('DEF')) == {wild_def}
    assert not ds.is_skipping()
    assert not ds.layers[-1].skip_rest
    ds.on_endif()
    assert len(ds.layers) == 2
    assert not ds.is_skipping()
    assert not ds.layers[-1].skip_rest
    ds.on_elifndef('DEF')
    assert not ds.is_skipping()
    assert not ds.layers[-1].skip_rest
    ds.on_elif(TK.tokenize('DEF != 1'))
    assert len(ds.layers) == 2
    assert not ds.is_skipping()
    assert not ds.layers[-1].skip_rest
    ds.on_undef('DEF')
    ds.on_define('DEF', TK.tokenize('1'))
    assert not ds.is_skipping()
    assert not ds.layers[-1].skip_rest
    ds.on_else()
    assert not ds.is_skipping()
    assert not ds.layers[-1].skip_rest
    ds.on_endif()
    assert len(ds.layers) == 1
