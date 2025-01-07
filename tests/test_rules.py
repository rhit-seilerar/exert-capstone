from exert.usermode import rules
from exert.usermode.rules import Rule, Int, Pointer, Field, FieldGroup, Struct
from exert.usermode.context import Context
from tests.test_context import DummyPanda

def test_base():
    assert Rule().ctest(Context(DummyPanda(), 0x0))

def test_cache():
    class DummyRule(Rule):
        def __init__(self):
            self.count = 0

        def _test(self, context):
            self.count += 1
            return self._cache[(self, context.address)] and self.count == 1

    context = Context(DummyPanda(), 0x0)
    rule = DummyRule()
    assert rule.test(context)
    assert rule.test(context)
    assert not rule.ctest(context)

def test_int():
    context = Context(DummyPanda(buf = b'\x00\x00\x00\x80\xFF\xFF\xFF\xFF'), 0x0)
    assert not Int(-1, 4, True).ctest(context)
    assert Int(2147483648, 4, False).ctest(context)
    assert Int(-1, 4, True).ctest(context)
    assert not Int(-1, 4, True).ctest(context)

def test_pointer():
    context = Context(DummyPanda(buf = b'\x04\x00\x00\x00\x00\x00\x00\x00'), 0x0)
    assert not Pointer(Int(2)).ctest(context)
    assert Pointer(Int(0)).ctest(context)
    assert Pointer(Pointer(Int(0))).ctest(context)
    assert not Pointer(Int(2)).ctest(context)

def test_field_group():
    context = Context(DummyPanda(buf = b'\x00\x00\x00\x00\x00\x00\x00\x00'), 0x0)
    # Passes when empty
    assert FieldGroup([]).ctest(context)
    # Passes when all of two fields passes
    assert FieldGroup([Field('',Rule()), Field('',Rule())]).ctest(context)
    # Fails when one of the fields fails
    assert not FieldGroup([Field('',Rule()), Field('',Int(3))]).ctest(context)

def test_struct():
    context = Context(DummyPanda(buf = b'\x00\x00\x00\x00\x00\x00\x00\x00'), 0x0)
    passing_group = FieldGroup([])
    failing_group = FieldGroup([Field('',Int(3))])
    passing_group_opt = FieldGroup([], True)
    failing_group_opt = FieldGroup([Field('',Int(3))], True)
    # Base case - len(groups) == 0
    assert Struct('', [passing_group]).ctest(context)
    # test passing required and true
    assert Struct('', [passing_group, passing_group]).ctest(context)
    # test passing required and false
    assert not Struct('', [passing_group, failing_group]).ctest(context)
    # test failing required and true
    assert not Struct('', [failing_group, passing_group]).ctest(context)
    # test failing required and false
    assert not Struct('', [failing_group, failing_group]).ctest(context)
    # test passing optional and true
    assert Struct('', [passing_group_opt, passing_group]).ctest(context)
    # test passing optional and false
    assert not Struct('', [passing_group_opt, failing_group]).ctest(context)
    # test failing optional and true
    assert Struct('', [failing_group_opt, passing_group]).ctest(context)
    # test failing optional and false
    assert not Struct('', [failing_group_opt, failing_group]).ctest(context)

def test_list_head():
    context = Context(DummyPanda(buf = b'\x00\x60\x00\x00\x00\x00\x00\x00'), 0x0)
    assert not rules.LIST_HEAD.ctest(context) #no valid next pointer
    context = Context(DummyPanda(buf = b'\x00\x00\x00\x00\x00\x07\x00\x00'), 0x0)
    assert not rules.LIST_HEAD.ctest(context) #no valid prev pointer
    context = Context(DummyPanda(buf = b'\x04\x00\x00\x00\x00\x00\x00\x00'), 0x0)
    assert not rules.LIST_HEAD.ctest(context) #next doesnt point at current
    context = Context(DummyPanda(buf = b'\x00\x00\x00\x00\x04\x00\x00\x00'), 0x0)
    assert not rules.LIST_HEAD.ctest(context) #prev doesnt point back at current
    context = Context(DummyPanda(buf = b'\x00\x00\x00\x00\x00\x00\x00\x00'), 0x0)
    assert rules.LIST_HEAD.ctest(context) #valid

def test_task_struct():
    context = Context(DummyPanda(buf = bytes(4096)), 0x0)
    assert rules.TASK_STRUCT.ctest(context)
