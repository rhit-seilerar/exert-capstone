from exert.parser.tokenmanager import mk_op
from exert.parser.tokenizer import Tokenizer
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from tests.utils import expect_error

TK = Tokenizer()

def make_def_variants() -> list[Def]:
    option1 = DefOption([('number', 1)])
    option2 = DefOption([('number', 2)])
    return [
        Def(),
        Def(undefined = True),
        Def(option1, option2, defined = True),
        Def(option1, option2, defined = True, undefined = True),
        Def(defined = True),
        Def(undefined = True, defined = True),
    ]

def test_def_states() -> None:
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

def test_def_copy() -> None:
    defs = make_def_variants()
    for defn in defs:
        new_def = defn.copy()
        assert new_def.defined == defn.defined
        assert new_def.undefined == defn.undefined
        assert new_def.options == defn.options
        new_def.options |= {5} # type: ignore
        assert new_def.options != defn.options

def test_def_invalid() -> None:
    defn = Def(DefOption([('integer', 1, '')]))
    defn.defined = False
    expect_error(defn.validate, ValueError)

def test_def_undefine() -> None:
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

def test_def_define_keep() -> None:
    opt = DefOption([mk_op(';')])
    assert Def().define(opt, True) == Def(opt)
    assert Def(defined = True).define(opt, True) == Def(opt)
    assert Def(undefined = True).define(opt, True) == Def(opt, undefined = True)
    opt2 = DefOption([mk_op('.')])
    assert Def(opt2).define(opt, True) == Def(opt, opt2)
    assert Def(opt2, undefined = True).define(opt, True) \
        == Def(opt, opt2, undefined = True)

def test_def_define_nokeep() -> None:
    opt = DefOption([mk_op(';')])
    assert Def().define(opt, False) == Def(opt)
    assert Def(defined = True).define(opt, False) == Def(opt)
    assert Def(undefined = True).define(opt, False) == Def(opt)
    opt2 = DefOption([mk_op('.')])
    assert Def(opt2).define(opt, False) == Def(opt, opt2)
    assert Def(opt2, undefined = True).define(opt, False) \
        == Def(opt, opt2, undefined = True)

def test_def_get_replacements() -> None:
    defs = make_def_variants()
    sym = ('identifier', 'abc')
    options = {DefOption([('number', 1)]), DefOption([('number', 2)])}
    ident_opt = DefOption([sym])
    wildcard_opt = DefOption([('any', 'abc', set())])
    assert defs[0].get_replacements(sym) == {wildcard_opt}
    assert defs[1].get_replacements(sym) == {ident_opt}
    assert defs[2].get_replacements(sym) == options
    assert defs[3].get_replacements(sym) == options | {ident_opt}
    assert defs[4].get_replacements(sym) == {wildcard_opt}
    assert defs[5].get_replacements(sym) == {wildcard_opt, ident_opt}

def test_def_combine() -> None:
    replace_defs = make_def_variants()
    other_defs = make_def_variants()
    try:
        replace_defs[0].combine('abc', replace = True) # type: ignore
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
            assert test.options == (defn.options if other.is_empty_def() else other.options)
            if other.defined:
                other_other = other.copy()
                other_other.options = set()
                test = defn.copy()
                test.combine(other_other, replace = True)
                assert test.options == defn.options

def test_def_len() -> None:
    defs = make_def_variants()
    assert len(defs[0]) == 0
    assert len(defs[1]) == 0
    assert len(defs[2]) == 2
    assert len(defs[3]) == 2

def test_def_matches() -> None:
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
        defs[0].matches('123') # type: ignore
        assert False
    except TypeError:
        pass

def test_def_eq() -> None:
    defs1 = make_def_variants()
    defs2 = make_def_variants()
    for i in range(0, 4):
        for j in range(0, 4):
            assert (i == j) == (defs1[i] == defs2[j])

def test_def_str() -> None:
    defs = make_def_variants()
    assert str(defs[0]) == '<initial>'
    assert str(defs[1]) == '<undefined>'
    assert str(defs[2]).startswith('{ ') and str(defs[2]).endswith(' }') \
        and set(str(defs[2])[2:-2].split(', ')) == {'$1', '$2'}
    assert str(defs[3]).startswith('{ ') and str(defs[3]).endswith(' }') \
        and set(str(defs[3])[2:-2].split(', ')) == {'$1', '$2', '$<undefined>'}
    invl = Def(DefOption([('integer', 1, '')]))
    invl.defined = False
    assert str(invl) == '<invalid>'
