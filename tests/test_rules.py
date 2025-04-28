from exert.usermode import rules
from exert.usermode.rules import Rule, Bool, Int, Pointer, Array, Field, FieldGroup, Struct
from tests.test_context import DummyContext

def results(rule: Rule, buf: bytes = b'', address: int = 0x0, bits: int = 32) -> set[int]:
    return rule.test(DummyContext(buf, bits = bits), address, True)

def test_base():
    out = Rule().test(DummyContext(), 0x5, True)
    assert out == {0x5}

def test_cache():
    class DummyRule(Rule):
        def __init__(self) -> None:
            super().__init__()
            self.count = 0

        def _get_str(self):
            return 'DummyRule'

        def _test(self, context, address):
            self.count += 1
            return set() if self.count > 1 else {address}

    rule = DummyRule()
    assert rule.test(DummyContext(), 0x0, False) # count should be 0
    assert rule.test(DummyContext(), 0x0, False) # count should be 1, but the result is cached
    assert not rule.test(DummyContext(), 0x0, True)  # cache is empty, count is 1 -> fail

def test_bool():
    buf = b'\x00\x01\x02\x80'
    assert results(Bool(), buf, 0x0) == {1}
    assert results(Bool(), buf, 0x1) == {2}
    assert not results(Bool(), buf, 0x2)
    assert not results(Bool(), buf, 0x3)

def test_any():
    #TODO
    rule = rules.Any(Int(), Bool())
    rule.test(DummyContext(), 0x0, True)

def test_int():
    buf = b'\x00\x00\x00\x80\xFF\xFF\xFF\xFF'
    assert not results(Int(4, True, min_value = -1), buf, 0x0)
    assert results(Int(4, False, min_value = 2147483648), buf, 0x0) == {4}
    assert results(Int(4, True, min_value = -1), buf, 0x4) == {8}
    assert not results(Int(4, True, min_value = -1), buf, 0x8)

def test_long():
    buf = b'\x01\x00\x00\x00\x00\x00\x00\x80'
    assert results(Int(None, True, 1), buf, 0x0, 32) == {4}
    assert results(Int(None, False, 0x8000000000000001), buf, 0x0, 64) == {8}

def test_pointer():
    buf = b'\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80'
    assert not results(Pointer(Int(min_value = 2)), buf, 0x0)
    assert results(Pointer(Int(min_value = 0)), buf, 0x0) == {4}
    assert results(Pointer(Pointer(Int(min_value = 0))), buf, 0x4) == {8}
    assert not results(Pointer(Int(min_value = 2)), buf, 0x8)
    assert results(Pointer(Int(None, False, min_value = 0x8000000000000000)), buf, 0x0, 64)

def test_array():
    array = Array(Int(1, min_value = 2), 2, 4)
    assert not results(array, b'\x02\x03')
    assert results(array, b'\x02\x02\x03') == {2}
    assert results(array, b'\x02\x02\x02\x03') == {2, 3}
    assert results(array, b'\x02\x02\x02\x02\x03') == {2, 3, 4}
    assert results(array, b'\x02\x02\x02\x02\x02') == {2, 3, 4}
    assert results(array, b'\x02\x02\x03\x02\x02') == {2}

def test_struct():
    struct = Struct('', [
        FieldGroup([Field('', Int(size = 1, min_value = 3))], 'COND1'),
        FieldGroup([Field('', Int(size = 1, min_value = 5))]),
        FieldGroup([Field('', Int(size = 1, min_value = 9))], 'COND2')
    ])
    assert not results(struct, b'')                   # ___
    assert not results(struct, b'\x09')               # __9
    assert results(struct, b'\x05') == {1}            # _5_
    assert results(struct, b'\x05\x09') == {1, 2}     # _59
    assert not results(struct, b'\x03')               # 3__
    assert not results(struct, b'\x03\x09')           # 3_9
    assert results(struct, b'\x03\x05') == {2}        # 35_
    assert results(struct, b'\x03\x05\x09') == {2, 3} # 359

    fully_opt = Struct('', [
        FieldGroup([Field('', Int(size = 1, min_value = 2))], 'COND1'),
        FieldGroup([Field('', Int(size = 1, min_value = 4))], 'COND2')
    ])
    assert results(fully_opt, b'') == {0}
    assert results(fully_opt, b'\x02') == {0, 1}
    assert results(fully_opt, b'\x04') == {0, 1}
    assert results(fully_opt, b'\x02\x04') == {0, 1, 2}

def test_list_head():
    assert not results(rules.LIST_HEAD, b'') # no next data
    assert not results(rules.LIST_HEAD, b'\x08\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00', 0x8)
    assert not results(rules.LIST_HEAD,
        b'\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 0x8)
    assert not results(rules.LIST_HEAD, b'\x00\x60\x00\x00\x00\x00\x00\x00') # no next ptr
    assert not results(rules.LIST_HEAD, b'\x00\x00\x00\x00\x00\x07\x00\x00') # no prev ptr
    assert not results(rules.LIST_HEAD, b'\x04\x00\x00\x00\x00\x00\x00\x00') # bad next link
    assert not results(rules.LIST_HEAD, b'\x00\x00\x00\x00\x04\x00\x00\x00') # bad prev link
    assert results(rules.LIST_HEAD, b'\x00\x00\x00\x00\x00\x00\x00\x00') # valid
