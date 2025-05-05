from exert.utilities.types.global_types import TokenType
from exert.parser.tokenizer import Tokenizer
from exert.parser.tokenmanager import mk_id, mk_kw, mk_int, mk_op, mk_dir, mk_nl
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.defmap import DefMap
from exert.parser.defevaluator import DefEvaluator

TK = Tokenizer()

def test_replace_unary_defined_none() -> None:
    de = DefEvaluator(64, DefMap(None))
    teststr = '#if 0 + 3 < 4'
    tokens = TK.tokenize(teststr)
    keys: set[TokenType] = set()
    de.replace_unary_defined(tokens, keys)
    assert tokens == TK.tokenize(teststr)
    assert not keys

def test_replace_unary_defined_without_parens() -> None:
    de = DefEvaluator(64, DefMap(None))
    teststr = '#if defined MACRO'
    tokens = TK.tokenize(teststr)
    keys: set[TokenType] = set()
    de.replace_unary_defined(tokens, keys)
    print(tokens)
    assert tokens == [mk_dir('#'), mk_kw('if'), ('defined', 'MACRO'), mk_nl()]
    assert keys == {mk_id('MACRO')}

def test_replace_unary_defined_with_parens() -> None:
    de = DefEvaluator(64, DefMap(None))
    teststr = '#if defined(MACRO)'
    tokens = TK.tokenize(teststr)
    keys: set[TokenType] = set()
    de.replace_unary_defined(tokens, keys)
    print(tokens)
    assert tokens == [mk_dir('#'), mk_kw('if'), ('defined', 'MACRO'), mk_nl()]
    assert keys == {mk_id('MACRO')}

def test_defevaluator_none() -> None:
    de = DefEvaluator(64, DefMap(None))
    assert de.evaluate_with_defs([mk_int(0)]) == (False, False, DefMap(de.defs))
    assert de.evaluate_with_defs([mk_int(1)]) == (True, True, DefMap(de.defs))
    assert de.evaluate_with_defs([mk_id('abc')]) == (False, False, DefMap(de.defs))
    assert de.evaluate_with_defs([mk_id('true')]) == (True, True, DefMap(de.defs))
    de.defs['abc'] = Def(DefOption([mk_int(1)]), undefined = True)
    assert de.evaluate_with_defs(TK.tokenize('abc == 2')) == (False, False, DefMap(de.defs))

def test_defevaluator_single() -> None:
    de = DefEvaluator(64, DefMap(None))
    de.defs['abc'] = Def(defined = True)
    assert de.evaluate_with_defs([mk_id('defined'), mk_op('('),
        mk_id('abc'), mk_op(')')]) == \
        (True, True, DefMap(de.defs, initial = {'abc': Def(defined = True)}))
    de.defs['abc'] = Def(DefOption([]), defined = True)
    assert de.evaluate_with_defs([mk_id('defined'), mk_id('abc')]) == \
        (True, True, DefMap(de.defs, initial = {'abc': Def(DefOption([]), defined = True)}))
    de.defs['abc'] = Def(DefOption([mk_int(3)]), defined = True)
    assert de.evaluate_with_defs([mk_id('defined'), mk_id('abc')]) == \
        (True, True, DefMap(de.defs, initial = {
            'abc': Def(DefOption([mk_int(3)]), defined = True)}))
    de.defs['abc'] = Def(undefined = True)
    assert de.evaluate_with_defs([mk_id('defined'), mk_id('abc')]) == \
        (False, False, DefMap(de.defs))

def test_defevaluator_multiple() -> None:
    de = DefEvaluator(64, DefMap(None))
    assert de.evaluate_with_defs(TK.tokenize('defined abc')) == \
        (True, False, DefMap(de.defs, initial = {'abc': Def(defined = True)}))
    de.defs['abc'] = Def(defined = True, undefined = True)
    assert de.evaluate_with_defs(TK.tokenize('defined abc')) == \
        (True, False, DefMap(de.defs, initial = {'abc': Def(defined = True)}))
    assert de.evaluate_with_defs(TK.tokenize('defined abc || !defined abc')) == \
        (True, True, DefMap(de.defs, initial = {
            'abc': Def(defined = True, undefined = True)}))
    de.defs['abc'] = Def(DefOption([mk_int(1)]), DefOption([mk_int(2)]),
        defined = True, undefined = True)
    assert de.evaluate_with_defs(TK.tokenize('!defined abc || abc == 2')) == \
        (True, False, DefMap(de.defs, initial = {
            'abc': Def(DefOption([mk_int(2)]), undefined = True)}))
    assert de.evaluate_with_defs(TK.tokenize('abc == 1 || abc == 2')) == \
        (True, False, DefMap(de.defs, initial = {
            'abc': Def(DefOption([mk_int(2)]), DefOption([mk_int(1)]))}))
