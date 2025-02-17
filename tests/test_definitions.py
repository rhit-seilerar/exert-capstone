from exert.parser.definitions import DefOption, Def, DefMap

def test_defoption_eq():
    empty = DefOption([])
    defoption12 = DefOption([('number', 1), ('number', 2)])
    defoptionab = DefOption([('identifier', 'a'), ('identifier', 'b')])
    assert empty != defoption12
    assert empty != 'abc'
    assert empty == DefOption([])
    assert empty == empty
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

def test_defoption_iter():
    option = DefOption([('identifier', 'a'), ('identifier', 'b')])
    tokens = []
    for defoption in option:
        tokens.append(defoption)
    assert option.tokens == tokens

def test_defoption_len():
    assert len(DefOption([])) == 0
    assert len(DefOption([('number', 1)])) == 1
    assert len(DefOption([('identifier', 'a'), ('identifier', 'b')])) == 2

def test_defoption_getitem():
    try:
        assert DefOption([])[0]
    except IndexError:
        pass
    assert DefOption([('number', 1)])[0] == ('number', 1)
    defoptionab = DefOption([('identifier', 'a'), ('identifier', 'b')])
    assert defoptionab[0] == ('identifier', 'a')
    assert defoptionab[1] == ('identifier', 'b')

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
    option = DefOption([('integer', 4)])
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
    assert defs[0].get_replacements(sym) == {DefOption([sym])}
    assert defs[1].get_replacements(sym) == {DefOption([sym])}
    assert defs[2].get_replacements(sym) == options
    assert defs[3].get_replacements(sym) == options | {DefOption([sym])}

def test_def_combine():
    replace_defs = make_def_variants()
    other_defs = make_def_variants()
    try:
        assert replace_defs[0].combine('abc', replace = True)
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
        defmap['abc'] = 'abc'
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

def test_defmap_str():
    defmap = DefMap(None, skipping = True, initial = {'abc': Def(undefined = True)})
    assert str(defmap) == 'DefMap(parent = None, skipping = True, defs = ' \
        "{'abc': <undefined>})"
