from exert.parser.tokenizer import Tokenizer
from exert.parser import tokenmanager as tm
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.defmap import DefMap
from exert.parser.defevaluator import DefEvaluator

TK = Tokenizer()

def test_defevaluator_none() -> None:
    de = DefEvaluator(64, DefMap(None))
    assert de.evaluate([tm.mk_int(0)]) == (False, False, DefMap(de.defs))
    assert de.evaluate([tm.mk_int(1)]) == (True, True, DefMap(de.defs))
    assert de.evaluate([tm.mk_id('abc')]) == (False, False, DefMap(de.defs))
    assert de.evaluate([tm.mk_id('true')]) == (True, True, DefMap(de.defs))
    de.defs['abc'] = Def(DefOption([tm.mk_int(1)]), undefined = True)
    assert de.evaluate(TK.tokenize('abc == 2')) == (False, False, DefMap(de.defs))

def test_defevaluator_single() -> None:
    de = DefEvaluator(64, DefMap(None))
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

def test_defevaluator_multiple() -> None:
    de = DefEvaluator(64, DefMap(None))
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
