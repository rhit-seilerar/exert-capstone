from exert.parser.tokenizer import Tokenizer
from exert.parser import tokenmanager as tm
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.defstate import DefState

TK = Tokenizer()

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
