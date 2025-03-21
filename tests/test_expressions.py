from tests import utils
from exert.parser import expressions
from exert.parser.tokenizer import Tokenizer

TOKENIZER = Tokenizer()

def expect_error(expr, bitsize, exception = AssertionError):
    utils.expect_error(lambda: \
        expressions.parse_expression(TOKENIZER.tokenize(expr), bitsize), exception)

def roundtrip(expr, bitsize, expected = None):
    if expected is None:
        expected = expr
    tokens = TOKENIZER.tokenize(expr)
    parsed = expressions.parse_expression(tokens, bitsize)
    assert str(parsed) == expected

def test_base():
    utils.expect_error(lambda: expressions.Expression().evaluate(32))
    assert str(expressions.Expression()) == ''

def test_parse():
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

def evaluate(expr, bitsize, expected, unsigned):
    tokens = TOKENIZER.tokenize(expr)
    parsed = expressions.parse_expression(tokens, bitsize)
    evaluator = expressions.Evaluator(bitsize)
    rint = parsed.evaluate(evaluator).evaluate(evaluator)
    result = expressions.eval_expression(parsed, bitsize)
    assert result == expected
    assert rint.value == expected
    assert rint.unsigned == unsigned

def test_eval():
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

def test_bitsize():
    evaluate('1 << 32', 32, 0, False)
    evaluate('1 << 32', 64, 2**32, False)
    evaluate('0xffffffffu + 1', 32, 0, True)
    evaluate('0xffffffffu + 1', 64, 2**32, True)

def test_evaluate():
    tokens = [
        ('integer', 1, ''),
        ('operator', '+'),
        ('integer', 3, '')
    ]
    result1 = expressions.evaluate(tokens, 32)
    result2 = expressions.eval_expression(expressions.parse_expression(tokens, 32), 32)
    assert result1 == result2 and result2 == 4
