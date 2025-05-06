from exert.parser.tokenizer import Tokenizer
from exert.parser.tokenmanager import mk_int, mk_id
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.defmap import DefMap
from exert.parser.deflayer import DefLayer

TK = Tokenizer()

def test_deflayer_skip_all() -> None:
    dl = DefLayer(DefMap(None), 32, True)
    dl.add_map([mk_id('abc')], closing = True)
    assert dl.current == DefMap(None, skipping = True)

def test_deflayer_first() -> None:
    parent = DefMap(None, initial = {'abc': Def(DefOption([mk_int(1)]),
        DefOption([mk_int(2)]), undefined = True)})
    dl = DefLayer(parent, 32, False)
    dl.add_map(TK.tokenize('defined abc'))
    assert dl.cond_acc == TK.tokenize('!(defined abc)')
    assert dl.current is not None
    assert dl.current['abc'] == Def(DefOption([mk_int(1)]), DefOption([mk_int(2)]))
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

def test_deflayer_next() -> None:
    parent = DefMap(None, initial = {
        'abc': Def(DefOption([mk_int(1)]), DefOption([mk_int(2)]), undefined = True),
        'def': Def(undefined = True)
    })
    dl = DefLayer(parent, 32, False)
    dl.add_map(TK.tokenize('defined abc'))

    dl.add_map(TK.tokenize('!defined abc'))
    assert dl.cond == TK.tokenize('!(defined abc) && (!defined abc)')
    assert dl.cond_acc == TK.tokenize('!(defined abc) && !(!defined abc)')
    assert dl.accumulator['abc'] == Def(DefOption([mk_int(1)]), DefOption([mk_int(2)]))
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
