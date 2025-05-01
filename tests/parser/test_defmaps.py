from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.defmap import DefMap

def test_defmap_local() -> None:
    abc = Def(defined = True)
    defmap = DefMap(None, initial = {'abc': abc})
    assert defmap.getlocal('abc') == abc
    assert defmap.getlocal('def').is_initial()
    defmap.getlocal('def').undefine(keep = False)
    assert defmap.getlocal('def').is_undefined()

def test_defmap_lookup() -> None:
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

def test_defmap_undefine() -> None:
    skipping = DefMap(None, skipping = True, initial = {'abc': Def(defined = True)})
    skipping.undefine('abc')
    assert not skipping['abc'].undefined
    keeping = DefMap(None, initial = {'abc': Def(defined = True)})
    keeping.undefine('abc')
    assert keeping['abc'].undefined
    assert not keeping['abc'].defined

def test_defmap_define() -> None:
    skipping = DefMap(None, skipping = True, initial = {'abc': Def(undefined = True)})
    skipping.define('abc', DefOption([]))
    assert not skipping['abc'].defined
    keeping = DefMap(None, initial = {'abc': Def(undefined = True)})
    keeping.define('abc', DefOption([]))
    assert keeping['abc'].defined
    keeping['abc'].undefined = True
    keeping.define('abc', DefOption([]))
    assert keeping['abc'].undefined

def test_defmap_combine() -> None:
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

def test_defmap_matches() -> None:
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

def test_defmap_str() -> None:
    defmap = DefMap(None, skipping = True, initial = {'abc': Def(undefined = True)})
    assert str(defmap) == 'DefMap(parent = None, skipping = True, defs = ' \
        "{'abc': <undefined>})"
