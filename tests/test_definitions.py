from tests import utils
from exert.parser.tokenizer import Tokenizer
from exert.parser import tokenmanager as tm
from exert.parser import definitions
from exert.parser.definitions import DefOption, Def, DefMap, DefLayer, DefState

def test_defoption_eq():
    empty = DefOption([])
    defoption12 = DefOption([('number', 1), ('number', 2)])
    defoptionab = DefOption([('identifier', 'a'), ('identifier', 'b')])
    assert empty != defoption12
    assert empty != 'abc'
    assert empty == DefOption([])
    assert defoption12 != defoptionab
    assert defoption12 == DefOption([('number', 1), ('number', 2)])

def test_defoption_hash():
    options = {
        DefOption([]),
        DefOption([('number', 1), ('number', 2)]),
        DefOption([('identifier', 'a'), ('identifier', 'b')])
    }
    options_dup = set()
    for defoption in options:
        options_dup.add(defoption)
        options_dup.add(defoption)
    assert options == options_dup

def test_defoption_len():
    assert len(DefOption([])) == 0
    assert len(DefOption([('number', 1)])) == 1
    assert len(DefOption([('identifier', 'a'), ('identifier', 'b')])) == 2

def test_defoption_str():
    assert str(DefOption([])) == ''
    assert str(DefOption([('identifier', 'a'), ('identifier', 'b')])) == 'a b'

def make_def_variants():
    option1 = DefOption([('number', 1)])
    option2 = DefOption([('number', 2)])
    return [
        Def(),
        Def(undefined = True),
        Def(option1, option2, defined = True),
        Def(option1, option2, defined = True, undefined = True)
    ]

def test_def_states():
    try:
        assert Def(DefOption([]), defined = False)
    except ValueError:
        pass
    defs = make_def_variants()
    assert defs[0].is_initial() and not defs[0].is_undefined() \
        and not defs[0].is_defined() and not defs[0].is_uncertain() \
        and defs[0].options == set()
    assert not defs[1].is_initial() and defs[1].is_undefined() \
        and not defs[1].is_defined() and not defs[1].is_uncertain() \
        and defs[0].options == set()
    assert not defs[2].is_initial() and not defs[2].is_undefined() \
        and defs[2].is_defined() and not defs[2].is_uncertain() \
        and defs[2].options == {DefOption([('number', 1)]), DefOption([('number', 2)])}
    assert not defs[3].is_initial() and not defs[3].is_undefined() \
        and not defs[3].is_defined() and defs[3].is_uncertain() \
        and defs[3].options == {DefOption([('number', 1)]), DefOption([('number', 2)])}

def test_def_copy():
    defs = make_def_variants()
    for defn in defs:
        new_def = defn.copy()
        assert new_def.defined == defn.defined
        assert new_def.undefined == defn.undefined
        assert new_def.options == defn.options
        new_def.options |= {5}
        assert new_def.options != defn.options

def test_def_invalid():
    defn = Def(DefOption([('integer', 1, '')]))
    defn.defined = False
    utils.expect_error(defn.validate, ValueError)

def test_def_undefine():
    defs1 = make_def_variants()
    for defn in defs1:
        was_defined = defn.defined
        prev_options = defn.options
        defn.undefine()
        assert defn.undefined
        assert was_defined == defn.defined
        assert prev_options == defn.options
    defs2 = make_def_variants()
    for defn in defs2:
        defn.undefine(keep = False)
        assert defn.undefined
        assert not defn.defined
        assert len(defn.options) == 0

def test_def_define():
    defs1 = make_def_variants()
    try:
        assert defs1[0].define('abc')
    except TypeError:
        pass
    option = DefOption([('integer', 4, '')])
    for defn in defs1:
        was_uncertain = defn.is_uncertain()
        prev_options = defn.options
        defn.define(option)
        assert defn.options == prev_options | {option}
        assert defn.undefined == was_uncertain
        assert defn.defined
    defs2 = make_def_variants()
    for defn in defs2:
        prev_options = defn.options
        defn.define(option, keep = False)
        assert defn.options == prev_options | {option}
        assert not defn.undefined
        assert defn.defined

def test_def_get_replacements():
    defs = make_def_variants()
    sym = ('identifier', 'abc')
    options = {DefOption([('number', 1)]), DefOption([('number', 2)])}
    assert defs[0].get_replacements(sym) == {DefOption([('any', 'abc', set())])}
    assert defs[1].get_replacements(sym) == {DefOption([sym])}
    assert defs[2].get_replacements(sym) == options
    assert defs[3].get_replacements(sym) == options | {DefOption([sym])}

def test_def_combine():
    replace_defs = make_def_variants()
    other_defs = make_def_variants()
    try:
        replace_defs[0].combine('abc', replace = True)
        assert False
    except TypeError:
        pass
    for defn in replace_defs:
        for other in other_defs:
            test = defn.copy()
            test.combine(other, replace = False)
            assert test.defined == defn.defined | other.defined
            assert test.undefined == defn.undefined | other.undefined
            assert test.options == defn.options | other.options
    for defn in replace_defs:
        for other in other_defs:
            test = defn.copy()
            test.combine(other, replace = True)
            assert test.defined == other.defined
            assert test.undefined == other.undefined
            assert test.options == other.options
            if other.defined:
                other_other = other.copy()
                other_other.options = set()
                test = defn.copy()
                test.combine(other_other, replace = True)
                assert test.options == defn.options

def test_def_len():
    defs = make_def_variants()
    assert len(defs[0]) == 0
    assert len(defs[1]) == 0
    assert len(defs[2]) == 2
    assert len(defs[3]) == 2

def test_def_matches():
    defs = make_def_variants()
    others = make_def_variants()
    assert defs[0].matches(others[0])
    assert defs[1].matches(others[0])
    assert defs[2].matches(others[0])
    assert defs[3].matches(others[0])
    assert defs[0].matches(others[1])
    assert defs[1].matches(others[1])
    assert not defs[2].matches(others[1])
    assert defs[3].matches(others[1])
    assert defs[0].matches(others[2])
    assert not defs[1].matches(others[2])
    assert defs[2].matches(others[2])
    assert defs[3].matches(others[2])
    assert defs[0].matches(others[3])
    assert not defs[1].matches(others[3])
    assert defs[2].matches(others[3])
    assert defs[3].matches(others[3])
    assert defs[2].matches(Def(defined = True))
    try:
        defs[0].matches('123')
        assert False
    except TypeError:
        pass

def test_def_eq():
    defs1 = make_def_variants()
    defs2 = make_def_variants()
    for i in range(0, 4):
        for j in range(0, 4):
            assert (i == j) == (defs1[i] == defs2[j])

def test_def_str():
    defs = make_def_variants()
    assert str(defs[0]) == '<initial>'
    assert str(defs[1]) == '<undefined>'
    assert str(defs[2]).startswith('{ ') and str(defs[2]).endswith(' }') \
        and set(str(defs[2])[2:-2].split(', ')) == {'1', '2'}
    assert str(defs[3]).startswith('{ ') and str(defs[3]).endswith(' }') \
        and set(str(defs[3])[2:-2].split(', ')) == {'1', '2', '<undefined>'}
    invl = Def(DefOption([('integer', 1, '')]))
    invl.defined = False
    assert str(invl) == '<invalid>'

def test_defmap_local():
    abc = Def(defined = True)
    defmap = DefMap(None, initial = {'abc': abc})
    assert defmap.getlocal('abc') == abc
    assert defmap.getlocal('def').is_initial()
    defmap.getlocal('def').undefine(keep = False)
    assert defmap.getlocal('def').is_undefined()

def test_defmap_lookup():
    abc = Def(defined = True)
    ghi = Def(undefined = True)
    parent = DefMap(None, initial = {'ghi': ghi})
    defmap = DefMap(parent, initial = {'abc': abc})
    assert defmap['abc'] == abc
    assert defmap['def'].is_initial()
    assert defmap['ghi'] == ghi
    defmap['def'].undefine(keep = False)
    assert defmap['def'].is_initial()
    defmap['def'] = ghi.copy()
    defmap['ghi'] = abc.copy()
    assert defmap['def'] == ghi
    assert defmap['ghi'] == abc
    assert parent['ghi'] == ghi
    try:
        defmap['abc'] = 'abc' # type: ignore
        # As can clearly be seen below, this is an intentional type error
        assert False
    except TypeError:
        pass

def test_defmap_undefine():
    skipping = DefMap(None, skipping = True, initial = {'abc': Def(defined = True)})
    skipping.undefine('abc')
    assert not skipping['abc'].undefined
    keeping = DefMap(None, initial = {'abc': Def(defined = True)})
    keeping.undefine('abc')
    assert keeping['abc'].undefined
    assert not keeping['abc'].defined

def test_defmap_define():
    skipping = DefMap(None, skipping = True, initial = {'abc': Def(undefined = True)})
    skipping.define('abc', DefOption([]))
    assert not skipping['abc'].defined
    keeping = DefMap(None, initial = {'abc': Def(undefined = True)})
    keeping.define('abc', DefOption([]))
    assert keeping['abc'].defined
    keeping['abc'].undefined = True
    keeping.define('abc', DefOption([]))
    assert keeping['abc'].undefined

def test_defmap_combine():
    defmap = DefMap(None, skipping = True, initial = {'abc': Def(undefined = True)})
    defn = Def(DefOption([]), defined = True)
    defmap.combine({'abc': defn}, replace = True)
    assert not defmap['abc'].defined
    assert len(defmap['abc']) == 0
    defmap.skipping = False
    defmap.combine({'abc': defn}, replace = True)
    assert defmap['abc'].defined
    assert len(defmap['abc']) == 1
    defmap.combine({'abc': defn}, replace = False)
    assert defmap['abc'].defined
    assert len(defmap['abc']) == 1
    try:
        defmap.combine(defn, replace = True)
        assert False
    except TypeError:
        pass

def test_defmap_matches():
    defmap = DefMap(None, skipping = True, initial = {
        'abc': Def(undefined = True),
        'def': Def(undefined = True, defined = True)
    })
    assert defmap.matches(DefMap(None, initial = {
        'abc': Def(),
        'def': Def(undefined = True, defined = True)
    }))
    assert not defmap.matches(DefMap(None, initial = {
        'abc': Def(DefOption([]), defined = True),
        'def': Def(undefined = True, defined = True)
    }))
    try:
        defmap.matches({'abc': Def(defined = True)})
        assert False
    except TypeError:
        pass

def test_defmap_str():
    defmap = DefMap(None, skipping = True, initial = {'abc': Def(undefined = True)})
    assert str(defmap) == 'DefMap(parent = None, skipping = True, defs = ' \
        "{'abc': <undefined>})"

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
    assert defstate.substitute(tm.mk_id('SECOND'))[0][0] == 'any'

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
