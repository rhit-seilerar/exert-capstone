from typing import Any
from exert.parser.parser import Parser
from exert.parser.definitions import DefOption

class DummyParser(Parser):
    def dfail(self, p:Any, f:Any)->Any:
        return f

    def dpass(self, p:Any, f:Any)->Any:
        self.index += 10
        return p

def test_unwrap():
    p = DummyParser()
    def j1(p1, f1):
        return p.dpass, (p.dpass, p1, f1), f1
    def j2(p1, f1):
        return p.dpass, (p.dfail, p1, f1), f1
    assert p.unwrap((j1, True, False))
    assert not p.unwrap((j2, True, False))

def test_chkpt():
    p = DummyParser()
    def joined(p1, f1):
        return p.dpass, (p.dfail, p1, f1), f1

    assert p.index == 0
    p.unwrap((joined, True, False))
    assert p.index == 10
    p.unwrap((p.chkpt(joined), True, False))
    assert p.index == 10

def test_opt():
    p = DummyParser()
    assert p.unwrap((p.opt(p.dfail), True, False))
    assert p.unwrap((p.opt(p.dpass), True, False))

def test_por():
    p = DummyParser()
    dpass = p.dpass
    dfail = p.dfail

    step1 = p.por()
    assert callable(step1)
    step2 = step1(True, False)
    assert not step2

    step1 = p.por(dpass)
    assert callable(step1)
    step2 = step1(True, False)
    assert step2[0] is dpass
    assert step2[1]
    assert callable(step2[2][0])
    nex = step2[2][0]
    assert step2[2][1]
    assert not step2[2][2]
    step3 = step2[0](step2[1], step2[2])
    assert step3

    step1 = p.por(dfail, dpass, dfail)
    assert callable(step1)
    step2 = step1(True, False)
    assert step2[0] is dfail
    assert step2[1]
    assert callable(step2[2][0])
    nex = step2[2][0]
    assert step2[2][1]
    assert not step2[2][2]
    step3 = step2[0](step2[1], step2[2])
    assert step3 == (nex, True, False)
    step4 = step3[0](step3[1], step3[2])
    assert step4[0] is dpass
    assert step4[1]
    assert step4[2][0] != nex
    nex = step4[2][0]
    assert step4[2][1]
    assert not step4[2][2]
    step5 = step4[0](step4[1], step4[2])
    assert step5

def test_pand():
    p = DummyParser()

    assert p.unwrap((p.pand(), True, False))
    assert p.index == 0

    assert not p.unwrap((p.pand(p.dfail), True, False))
    assert p.index == 0

    assert not p.unwrap((p.pand(p.dpass, p.dfail, p.dpass), True, False))
    assert p.index == 0

    assert p.unwrap((p.pand(p.dpass, p.dpass, p.dpass), True, False))
    assert p.index == 30

def test_any():
    p = DummyParser()
    assert p.unwrap((p.check_for_any, True, False))
    p.tokens = [('any', '', {
        DefOption([]),
        DefOption([('identifier', 'abc')])
    })]
    p.len = 1
    assert not p.unwrap((p.tok(('identifier', 'def')), True, False))
    assert p.index == 0
    assert p.unwrap((p.tok(('identifier', 'abc')), True, False))
