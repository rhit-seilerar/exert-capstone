from exert.parser import expressions
import exert.parser.tokenmanager as tm
from exert.parser.definition import Def
from exert.parser.expressions import Evaluator, parse_expression
from exert.parser.tokenizer import Tokenizer
from tests import utils

TOKENIZER = Tokenizer()

def expect_error(expr:str, bitsize:int, exception: type[AssertionError] = AssertionError) -> None:
    utils.expect_error(lambda: \
        parse_expression(TOKENIZER.tokenize(expr)), exception)

def roundtrip(expr:str, bitsize:int, expected:(str | None) = None) -> None:
    if expected is None:
        expected = expr
    tokens = TOKENIZER.tokenize(expr)
    parsed = parse_expression(tokens)
    assert str(parsed) == expected

def test_base() -> None:
    utils.expect_error(lambda: expressions.Expression().evaluate(32)) # type: ignore
    assert str(expressions.Expression()) == '<err>'

def test_parse() -> None:
    expect_error('', 32)
    expect_error('#if', 32)
    roundtrip('1', 32)
    roundtrip('1u', 32)
    expect_error('+', 32)
    roundtrip('+0x100', 32, '+256')
    roundtrip('-3203', 32)
    roundtrip('0b101 * 3', 32, '5 * 3')
    roundtrip('~-4u', 32)
    roundtrip('4 % !0 && 1', 32)
    roundtrip('2 + 4', 32)
    roundtrip('4 % !0', 32)
    roundtrip('2 + 3 % 4', 32)
    roundtrip('~-4u / 2 + 4 % !0 && 1', 32)
    roundtrip('1 * 2 / 3 % 4', 32)
    roundtrip('5 * 3 ? 1 : ~-4u / 2 + 4 % !0 && 1', 32)
    roundtrip('(1 * 2)', 32)
    roundtrip('((1 + 2) - 3) == 1', 32)
    roundtrip('5 * 3 ? 1 : ~-4u / (2 + 4) % !(0 && 1)', 32)
    roundtrip('+-!~1 * 2 / 3 % 4 + 5 - 6 << 7 >> 8 < 9 <= 10' \
        ' > 11 >= 12 == 13 != 14 & 15 ^ 16 | 17 && 18 || 19 ? 20 : 21', 32)

def evaluate(expr:str, bitsize:int, expected: (int | bool), expected_unsigned:bool) -> None:
    tokens = TOKENIZER.tokenize(expr)
    result = Evaluator(bitsize).evaluate(tokens)
    assert isinstance(result, tuple)
    value = result[0]
    unsigned = result[1]
    assert value == expected
    assert unsigned == expected_unsigned

def test_eval() -> None:
    evaluate('1u', 32, 1, True)
    evaluate('(1u)', 32, 1, True)
    evaluate('-(1u)', 32, -1, False)
    evaluate('+(1u)', 32, 1, True)
    evaluate('-(1 + 2) * 3', 32, -9, False)
    evaluate('1 ? -4 : -6', 32, -4, False)
    evaluate('0 ? -4 : -6', 32, -6, False)
    evaluate('((1 + 2) - 3) == 1', 32, 0, False)
    evaluate('((1 + 2) - 3) == 1 ? -4 : -6', 32, -6, False)
    evaluate('1 << -1', 32, 0, False)
    evaluate('1u << -1', 32, 0, True)
    evaluate('1 << 32', 32, 0, False)
    evaluate('1 << 2', 32, 4, False)
    evaluate('-1 << 2', 32, -4, False)
    evaluate('1 >> -1', 32, 0, False)
    evaluate('1 >> 32', 32, 0, False)
    evaluate('-1 >> 32', 32, -1, False)
    evaluate('-1 >> 31', 32, -1, False)
    evaluate('8 >> 2', 32, 2, False)
    evaluate('8 >> 2u', 32, 2, False)
    evaluate('8u >> 2', 32, 2, True)
    evaluate('abc', 32, 0, False)
    evaluate('true', 32, 1, False)

    evlr = Evaluator(32)
    evlr.lookup = {'abc': Def(defined = True)}
    assert isinstance(evlr.evaluate([('any', 'abc', set())]), expressions.Wildcard)
    assert str(expressions.Wildcard()) == '<wildcard>'
    assert isinstance(evlr.evaluate([
        tm.mk_op('-'),
        ('any', 'a', set()),
    ]), expressions.Wildcard)
    assert isinstance(evlr.evaluate([
        tm.mk_int(1),
        tm.mk_op('+'),
        ('any', 'a', set()),
    ]), expressions.Wildcard)
    assert isinstance(evlr.evaluate([
        ('any', 'a', set()),
        tm.mk_op('+'),
        tm.mk_int(1),
    ]), expressions.Wildcard)
    assert isinstance(evlr.evaluate([
        ('any', 'a', set()),
        tm.mk_op('<<'),
        tm.mk_int(1),
    ]), expressions.Wildcard)
    assert isinstance(evlr.evaluate([
        tm.mk_int(1),
        tm.mk_op('<<'),
        ('any', 'a', set()),
    ]), expressions.Wildcard)
    assert isinstance(evlr.evaluate([
        ('any', 'a', set()),
        tm.mk_op('>>'),
        tm.mk_int(1),
    ]), expressions.Wildcard)
    assert isinstance(evlr.evaluate([
        tm.mk_int(1),
        tm.mk_op('>>'),
        ('any', 'a', set()),
    ]), expressions.Wildcard)
    assert isinstance(evlr.evaluate([
        ('any', 'a', set()),
        tm.mk_op('?'),
        tm.mk_int(1),
        tm.mk_op(':'),
        tm.mk_int(2),
    ]), expressions.Wildcard)
    assert isinstance(evlr.evaluate([
        tm.mk_int(1),
        tm.mk_op('?'),
        ('any', 'a', set()),
        tm.mk_op(':'),
        tm.mk_int(2),
    ]), expressions.Wildcard)
    assert isinstance(evlr.evaluate([
        tm.mk_int(0),
        tm.mk_op('?'),
        tm.mk_int(2),
        tm.mk_op(':'),
        ('any', 'a', set()),
    ]), expressions.Wildcard)

def test_bitsize() -> None:
    evaluate('1 << 32', 32, 0, False)
    evaluate('1 << 32', 64, 2**32, False)
    evaluate('0xffffffffu + 1', 32, 0, True)
    evaluate('0xffffffffu + 1', 64, 2**32, True)
