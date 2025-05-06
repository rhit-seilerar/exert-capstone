from exert.utilities.types.global_types import TokenType
from exert.parser.tokenizer import Tokenizer
from exert.parser.tokenmanager import mk_id, mk_kw, mk_int, mk_op, mk_dir, mk_nl
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.defmap import DefMap
from exert.parser.defevaluator import DefEvaluator
from exert.parser.expressions import Wildcard, Integer

TK = Tokenizer()

def test_replace_unary_defined_none() -> None:
    de = DefEvaluator(64, DefMap(None))
    tokens = TK.tokenize('#if 0 + 3 < 4 defined')
    keys: set[TokenType] = set()
    result = de.replace_unary_defined(tokens, keys)
    assert result == tokens
    assert not keys

def test_replace_unary_defined_without_parens() -> None:
    de = DefEvaluator(64, DefMap(None))
    tokens = TK.tokenize('#if defined MACRO')
    keys: set[TokenType] = set()
    result = de.replace_unary_defined(tokens, keys)
    assert result == [mk_dir('#'), mk_kw('if'), ('defined', 'MACRO'), mk_nl()]
    assert keys == {mk_id('MACRO')}

def test_replace_unary_defined_with_parens() -> None:
    de = DefEvaluator(64, DefMap(None))
    tokens = TK.tokenize('#if defined(MACRO)')
    keys: set[TokenType] = set()
    result = de.replace_unary_defined(tokens, keys)
    assert result == [mk_dir('#'), mk_kw('if'), ('defined', 'MACRO'), mk_nl()]
    assert keys == {mk_id('MACRO')}

def test_replace_identifiers_true() -> None:
    de = DefEvaluator(64, DefMap(None))
    tokens = [mk_id('true')]
    result = de.replace_identifiers(tokens)
    assert result == [mk_int(1)]

def test_replace_identifiers_falsey() -> None:
    de = DefEvaluator(64, DefMap(None))
    tokens = [mk_id('false'), mk_id('a'), mk_kw('if')]
    result = de.replace_identifiers(tokens)
    assert result == [mk_int(0), mk_int(0), mk_int(0)]

def test_make_def_singletons_initial() -> None:
    de = DefEvaluator(64, DefMap(None))
    result = de.make_def_singletons(Def())
    assert len(result) == 2
    assert Def(defined = True) in result
    assert Def(undefined = True) in result

def test_make_def_singletons_undefined() -> None:
    de = DefEvaluator(64, DefMap(None))
    result = de.make_def_singletons(Def(undefined = True))
    assert result == [Def(undefined = True)]

def test_make_def_singletons_empty_def() -> None:
    de = DefEvaluator(64, DefMap(None))
    result = de.make_def_singletons(Def(defined = True))
    assert result == [Def(defined = True)]

def test_make_def_singletons_defined() -> None:
    de = DefEvaluator(64, DefMap(None))
    opts = [DefOption([mk_id('a')]), DefOption([mk_id('b')])]
    result = de.make_def_singletons(Def(*opts))
    assert len(result) == 2
    assert Def(opts[0]) in result
    assert Def(opts[1]) in result

def test_make_def_singletons_unsure() -> None:
    de = DefEvaluator(64, DefMap(None))
    opts = [DefOption([mk_id('a')]), DefOption([mk_id('b')])]
    result = de.make_def_singletons(Def(*opts, undefined = True))
    assert len(result) == 3
    assert Def(opts[0]) in result
    assert Def(opts[1]) in result
    assert Def(undefined = True) in result

def test_make_permuted_lookups_no_keys() -> None:
    de = DefEvaluator(64, DefMap(None, initial = {
        'MACRO': Def(DefOption([mk_int(1)]), DefOption([mk_int(2)]), undefined = True)
    }))
    tokens = TK.tokenize('int a = MACRO;')
    result = de.make_permuted_lookups(tokens, set())
    assert result == [{}]

def test_make_permuted_lookups() -> None:
    de = DefEvaluator(64, DefMap(None, initial = {
        'MACRO1': Def(undefined = True),
        'MACRO2': Def(DefOption([mk_int(1)]), DefOption([mk_int(2)]), undefined = True)
    }))
    tokens = TK.tokenize('int a = MACRO1 + MACRO2;')
    result = de.make_permuted_lookups(tokens, {mk_id('MACRO1'), mk_id('MACRO2')})
    assert len(result) == 3
    assert {
        'MACRO1': Def(undefined = True),
        'MACRO2': Def(DefOption([mk_int(1)]))
    } in result
    assert {
        'MACRO1': Def(undefined = True),
        'MACRO2': Def(DefOption([mk_int(2)]))
    } in result
    assert {
        'MACRO1': Def(undefined = True),
        'MACRO2': Def(undefined = True)
    } in result

def test_make_permuted_lookups_initial() -> None:
    de = DefEvaluator(64, DefMap(None))
    tokens = TK.tokenize('int a = MACRO;')
    result = de.make_permuted_lookups(tokens, {mk_id('MACRO')})
    assert len(result) == 2
    assert { 'MACRO': Def(undefined = True) } in result
    assert { 'MACRO': Def(defined = True) } in result

def test_subst_permutation_open_ended() -> None:
    de = DefEvaluator(64, DefMap(None))
    tokens: list[TokenType] = [('any', 'M', set())]
    result = de.subst_permutation({'M': Def(defined = True)}, tokens)
    assert result == tokens

def test_subst_permutation_flat() -> None:
    de = DefEvaluator(64, DefMap(None))
    tokens = [mk_id('a'), ('any', 'M', {DefOption([mk_op('.')])})]
    result = de.subst_permutation({'M': Def(DefOption([mk_op(';')]))}, tokens)
    assert result == [mk_id('a'), mk_op(';')]

def test_subst_permutation_defined() -> None:
    de = DefEvaluator(64, DefMap(None))
    tokens = [mk_id('a'), ('defined', 'M'), ('defined', 'N')]
    result = de.subst_permutation({
        'M': Def(DefOption([mk_op(';')])),
        'N': Def(undefined = True)
    }, tokens)
    assert result == [mk_id('a'), mk_int(1), mk_int(0)]

def test_subst_permutation_recurse() -> None:
    de = DefEvaluator(64, DefMap(None))
    inner = [mk_id('b'), ('any', 'N', {DefOption([mk_op('.')])})]
    tokens = [mk_id('a'), ('any', 'M', {DefOption([mk_op('.')])})]
    result = de.subst_permutation({
        'N': Def(DefOption([mk_id('c')])),
        'M': Def(DefOption(inner))
    }, tokens)
    assert result == [mk_id('a'), mk_id('b'), mk_id('c')]

def test_apply_evaluation_result_wildcard() -> None:
    de = DefEvaluator(64, DefMap(None))
    de.apply_evaluation_result(Wildcard(), {})
    assert hasattr(de, 'any_match') and de.any_match
    assert hasattr(de, 'all_match') and not de.all_match

def test_apply_evaluation_result_falsey() -> None:
    de = DefEvaluator(64, DefMap(None))
    de.apply_evaluation_result(Integer(0, False), {})
    assert not hasattr(de, 'any_match')
    assert hasattr(de, 'all_match') and not de.all_match

def test_apply_evaluation_result_truthy() -> None:
    de = DefEvaluator(64, DefMap(None))
    de.matches = DefMap(de.defs, initial = {
        'A': Def(undefined = True),
        'B': Def(DefOption([mk_op(';')]))
    })
    de.apply_evaluation_result(Integer(1, False), {
        'A': Def(DefOption([mk_id('a')])),
        'B': Def(DefOption([mk_id('b')]))
    })
    assert hasattr(de, 'any_match') and de.any_match
    assert not hasattr(de, 'all_match')
    assert de.matches == DefMap(de.defs, initial = {
        'A': Def(DefOption([mk_id('a')]), undefined = True),
        'B': Def(DefOption([mk_id('b')]), DefOption([mk_op(';')]))
    })

def test_evaluate_with_defs_value_matching() -> None:
    de = DefEvaluator(64, DefMap(None, initial = {
        'A': Def(DefOption([mk_int(1)]), DefOption([mk_int(2)])),
        'B': Def(DefOption([mk_int(2)]), DefOption([mk_int(3)])),
    }))
    tokens = TK.tokenize('A == B')
    anym, allm, m = de.evaluate_with_defs(tokens)
    assert anym
    assert not allm
    assert m == DefMap(de.defs, initial = {
        'A': Def(DefOption([mk_int(2)])),
        'B': Def(DefOption([mk_int(2)]))
    })

def test_evaluate_with_defs_value_matching_with_wildcard() -> None:
    de = DefEvaluator(64, DefMap(None, initial = {
        'A': Def(DefOption([mk_int(1)]), DefOption([mk_int(2)])),
        'B': Def(DefOption([mk_int(2)]), DefOption([mk_int(3)])),
        'E': Def()
    }))
    tokens = TK.tokenize('E || A == B')
    anym, allm, m = de.evaluate_with_defs(tokens)
    assert anym
    assert not allm
    assert m == DefMap(de.defs, initial = {
        'A': Def(DefOption([mk_int(2)])),
        'B': Def(DefOption([mk_int(2)]))
    })

def test_evaluate_with_defs_falsey_unary_defined() -> None:
    de = DefEvaluator(64, DefMap(None, initial = {
        'C': Def(defined = True),
        'D': Def(undefined = True),
    }))
    tokens = TK.tokenize('(!defined(C) || !!defined D) ? true : false')
    anym, allm, m = de.evaluate_with_defs(tokens)
    assert not anym
    assert not allm
    assert m == DefMap(de.defs)

def test_evaluate_with_defs_truthy_unary_defined() -> None:
    de = DefEvaluator(64, DefMap(None, initial = {
        'C': Def(),
        'D': Def(defined = True, undefined = True),
    }))
    tokens = TK.tokenize('(!defined(C) || !!defined D) ? true : false')
    anym, allm, m = de.evaluate_with_defs(tokens)
    assert anym
    assert not allm
    assert m == DefMap(de.defs, initial = {
        'C': Def(defined = True, undefined = True),
        'D': Def(defined = True, undefined = True)
    })

def test_evaluate_with_defs_valued_unary_defined() -> None:
    de = DefEvaluator(64, DefMap(None, initial = {
        'C': Def(DefOption([mk_op(';')]), undefined = True)
    }))
    tokens = TK.tokenize('defined C')
    anym, allm, m = de.evaluate_with_defs(tokens)
    assert anym
    assert not allm
    assert m == DefMap(de.defs, initial = {
        'C': Def(DefOption([mk_op(';')])),
    })

def test_evaluate_with_defs_value_matching_empty() -> None:
    de = DefEvaluator(64, DefMap(None, initial = {
        'E': Def(defined = True)
    }))
    tokens = TK.tokenize('E == 1')
    anym, allm, m = de.evaluate_with_defs(tokens)
    assert anym
    assert not allm
    print(m)
    assert m == DefMap(de.defs)
