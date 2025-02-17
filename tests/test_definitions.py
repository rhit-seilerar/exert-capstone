from exert.parser.definitions import DefOption

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
    options = {
        DefOption([]),
        DefOption([('number', 1), ('number', 2)]),
        DefOption([('identifier', 'a'), ('identifier', 'b')])
    }
    new_options = set()
    for defoption in options:
        new_options.add(defoption)
    assert options == new_options

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
