from exert.parser.tokenizer import Tokenizer
import exert.parser.tokenmanager as tm
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.definitions import DefState

TK = Tokenizer()

def test_substitute():
    defstate = DefState(64)

    nosubst = TK.tokenize('static int a = b;')
    tokmgr = tm.TokenManager(nosubst)
    assert defstate.substitute(tokmgr) == [tm.mk_kw('static')]
    assert tokmgr.index == 1

    defstate.on_define('STRING', [('string', '%d', '"')])
    assert defstate.substitute(tm.mk_id('STRING')) == [('string', '%d', '"')]

    defstate.on_undef('STRING')
    assert defstate.substitute(tm.mk_id('STRING')) == [tm.mk_id('STRING')]

    defstate.on_undef('STRING')
    defstate.on_define('STRING', [tm.mk_id('SECOND')])
    defstate.on_define('SECOND', [tm.mk_id('THIRD')])
    assert defstate.substitute(tm.mk_id('STRING')) == [tm.mk_id('THIRD')]

    defstate.on_undef('SECOND')
    defstate.on_define('SECOND', [tm.mk_id('STRING')])
    assert defstate.substitute(tm.mk_id('STRING')) == [tm.mk_id('STRING')]

    defstate.on_undef('STRING')
    defstate.on_define('STRING', [])
    assert defstate.substitute(tm.mk_id('STRING')) == []

    defstate.on_undef('STRING')
    assert defstate.layers[-1].current is not None
    defstate.layers[-1].current['STRING'] = Def()
    assert defstate.substitute(tm.mk_id('STRING')) == [tm.mk_id('STRING')]
    defstate.layers[-1].current['STRING'] = Def(undefined = True)
    assert defstate.substitute(tm.mk_id('STRING')) == [tm.mk_id('STRING')]
    defstate.layers[-1].current['STRING'] = Def(defined = True)
    assert defstate.substitute(tm.mk_id('STRING')) == [('any', 'STRING', set())]
    defstate.on_undef('SECOND')
    defstate.on_undef('THIRD')
    defstate.layers[-1].current['STRING'] = Def(
        DefOption([('string', '%d', '"')]),
        DefOption([tm.mk_id('SECOND'), tm.mk_id('THIRD')]),
        undefined = True,
        defined = True)
    result = defstate.substitute(tm.mk_id('STRING'))
    assert len(result) == 1
    assert result[0] is not None
    assert len(result[0]) > 2
    assert result[0][0] == 'any'
    assert result[0][1] == 'STRING'
    assert isinstance(result[0][2], set)
    opts = [opt.tokens for opt in result[0][2]]
    assert [('string', '%d', '"')] in opts
    assert [tm.mk_id('STRING')] in opts
    assert [tm.mk_id('SECOND'), (tm.mk_id('THIRD'))] in opts

    defstate.layers[-1].current['SECOND'] = Def(
        DefOption([tm.mk_int(0)]),
        DefOption([tm.mk_int(1)]),
    )

    new_result = defstate.substitute(tm.mk_id('SECOND'))
    assert new_result[0] is not None
    assert new_result[0][0] == 'any'
