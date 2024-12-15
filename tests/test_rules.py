from exert.usermode import rules
from exert.usermode.context import Context
from tests.test_context import DummyPanda

def test_base():
    assert rules.Rule().test(Context(DummyPanda(), 0x0))

def test_cache():
    class DummyRule(rules.Rule):
        def __init__(self):
            self.count = 0

        def _test(self, context):
            self.count += 1
            return self._cache[(self, context.address)] and self.count == 1

    context = Context(DummyPanda(), 0x0)
    rule = DummyRule()
    assert rule.test(context)
    assert rule.test(context)

def test_int():
    context = Context(DummyPanda(buf = b'\x00\x00\x00\x80\xFF\xFF\xFF\xFF'), 0x0)
    assert not rules.Int(-1, 4, True).test(context)
    assert rules.Int(2147483648, 4, False).test(context)
    assert rules.Int(-1, 4, True).test(context)
    assert not rules.Int(-1, 4, True).test(context)

def test_pointer():
    context = Context(DummyPanda(buf = b'\x04\x00\x00\x00\x00\x00\x00\x00'), 0x0)
    assert not rules.Pointer(rules.Int(2)).test(context)
    assert rules.Pointer(rules.Int(0)).test(context)
    assert rules.Pointer(rules.Pointer(rules.Int(0))).test(context)
    assert not rules.Pointer(rules.Int(2)).test(context)

def test_list_head():
    context = Context(DummyPanda(buf = b'\x00\x60\x00\x00\x00\x00\x00\x00'), 0x0)
    assert not rules.ListHead().test(context) #no valid next pointer
    context = Context(DummyPanda(buf = b'\x00\x00\x00\x00\x00\x07\x00\x00'), 0x0)
    assert not rules.ListHead().test(context) #no valid prev pointer
    context = Context(DummyPanda(buf = b'\x04\x00\x00\x00\x00\x00\x00\x00'), 0x0)
    assert not rules.ListHead().test(context) #next doesnt point at current
    context = Context(DummyPanda(buf = b'\x00\x00\x00\x00\x04\x00\x00\x00'), 0x0)
    assert not rules.ListHead().test(context) #prev doesnt point back at current
    context = Context(DummyPanda(buf = b'\x00\x00\x00\x00\x00\x00\x00\x00'), 0x0)
    assert rules.ListHead().test(context) #valid
