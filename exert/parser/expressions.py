from collections.abc import Callable
import exert.parser.tokenmanager as tm
from exert.parser.definitions import DefOption, Def
from exert.utilities.types.global_types import TokenType, ExpressionTypes
from typing import NoReturn

class Expression:
    def evaluate(self, evaluator: 'Evaluator') -> 'Expression':
        assert False

    def __str__(self):
        return '<err>'

class Integer(Expression):
    def __init__(self, value: int, unsigned: bool):
        self.value = value
        self.unsigned = unsigned

    def evaluate(self, evaluator) -> 'Integer':
        base = 1 << evaluator.bitsize
        value = self.value % base
        if not self.unsigned and value >= base / 2:
            value -= base
        return Integer(value, self.unsigned)

    def __str__(self):
        return str(self.value) + ('u' if self.unsigned else '')

class Identifier(Integer):
    def __init__(self, a: str | int):
        super().__init__(1 if a == 'true' else 0, False)

class Wildcard(Expression):
    options: set[DefOption] = set()

    def evaluate(self, evaluator):
        return self

    def __str__(self):
        return '<wildcard>'

class Group(Expression):
    def __init__(self, expression: Expression):
        self.expression = expression

    def evaluate(self, evaluator):
        return self.expression.evaluate(evaluator)

    def __str__(self):
        return f'({str(self.expression)})'

class Operator(Expression):
    pass

class UnaryOperator(Operator):
    def __init__(self, a: ExpressionTypes, opname: str,
                 op: Callable[[int], int], signop: (Callable[[bool], bool] | None) = None):
        assert isinstance(a, (Expression, str))
        self.opname = opname
        self.op = op
        self.a: Expression | str = a
        self.signop = (lambda asig: asig) if signop is None else signop

    def evaluate(self, evaluator):
        assert isinstance(self.a, Integer)
        aint = self.a.evaluate(evaluator)
        if isinstance(aint, Wildcard):
            aint.options = set()
            return aint
        unsigned = self.signop(aint.unsigned)
        return Integer(self.op(aint.value), unsigned)

    def __str__(self):
        return self.opname + str(self.a)

class BinaryOperator(Operator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes, opname: str,
                 op: (Callable[[int, int], int] | None), signop: (Callable[[bool, bool], bool] | None) = None):
        assert isinstance(a, Expression)
        assert isinstance(b, Expression)
        self.opname = opname
        self.op = op
        self.a = a
        self.b = b
        self.signop = (lambda asig, bsig: asig or bsig) if signop is None else signop

    def evaluate(self, evaluator):
        aint = self.a.evaluate(evaluator)
        bint = self.b.evaluate(evaluator)
        if isinstance(aint, Wildcard):
            aint.options = set()
            return aint
        if isinstance(bint, Wildcard):
            bint.options = set()
            return bint
        assert isinstance(aint, Integer)
        assert isinstance(bint, Integer)
        unsigned = self.signop(aint.unsigned, bint.unsigned)
        assert self.op is not None
        return Integer(self.op(aint.value, bint.value), unsigned)

    def __str__(self):
        return str(self.a) + f' {self.opname} ' + str(self.b)

class UnaryDefined(UnaryOperator):
    def __init__(self, a: Expression | str | int):
        assert isinstance(a, (Expression, str))
        super().__init__(a, 'defined', lambda a: a)

    def evaluate(self, evaluator):
        if self.a in evaluator.lookup and evaluator.lookup[self.a].defined:
            evaluator.defines[self.a] = True
            return Integer(1, False)
        evaluator.defines[self.a] = False
        return Integer(0, False)

    def __str__(self):
        return f'defined({self.a})'

class UnaryPlus(UnaryOperator):
    def __init__(self, a: ExpressionTypes):
        super().__init__(a, '+', lambda a: a)

class UnaryMinus(UnaryOperator):
    def __init__(self, a: ExpressionTypes):
        super().__init__(a, '-', lambda a: -a, lambda asig: False)

class Add(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '+', lambda a, b: a + b)

class Subtract(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '-', lambda a, b: a - b)

class Multiply(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '*', lambda a, b: a * b)

class Divide(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '/', lambda a, b: a // b)

class Remainder(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '%', lambda a, b: abs(a) % abs(b) * (1 - 2 * (a < 0)))

class BitwiseNot(UnaryOperator):
    def __init__(self, a: ExpressionTypes):
        super().__init__(a, '~', lambda a: ~a)

class BitwiseAnd(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '&', lambda a, b: a & b)

class BitwiseOr(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '|', lambda a, b: a | b)

class BitwiseXor(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '^', lambda a, b: a ^ b)

class LeftShift(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '<<', None)

    def evaluate(self, evaluator):
        aint = self.a.evaluate(evaluator)
        bint = self.b.evaluate(evaluator)
        if isinstance(aint, Wildcard):
            aint.options = set()
            return aint
        if isinstance(bint, Wildcard):
            bint.options = set()
            return bint
        assert isinstance(aint, Integer)
        assert isinstance(bint, Integer)
        unsigned = aint.unsigned
        return Integer(0 if bint.value < 0 or bint.value >= evaluator.bitsize
            else aint.value << bint.value, unsigned)

class RightShift(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '>>', None)

    def evaluate(self, evaluator):
        aint = self.a.evaluate(evaluator)
        bint = self.b.evaluate(evaluator)
        if isinstance(aint, Wildcard):
            aint.options = set()
            return aint
        if isinstance(bint, Wildcard):
            bint.options = set()
            return bint
        assert isinstance(aint, Integer)
        assert isinstance(bint, Integer)
        unsigned = aint.unsigned
        return Integer(0 if bint.value < 0
            else -1 if bint.value >= evaluator.bitsize and aint.value < 0
            else 0 if bint.value >= evaluator.bitsize
            else aint.value >> bint.value, unsigned)

class LogicalNot(UnaryOperator):
    def __init__(self, a: ExpressionTypes):
        super().__init__(a, '!', lambda a: 1 if not a else 0)

class LogicalAnd(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '&&', lambda a, b: 1 if a and b else 0)

class LogicalOr(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '||', lambda a, b: 1 if a or b else 0)

class Equal(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '==', lambda a, b: 1 if a == b else 0, lambda asig, bsig: False)

class NotEqual(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '!=', lambda a, b: 1 if a != b else 0, lambda asig, bsig: False)

class LessThan(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '<', lambda a, b: 1 if a < b else 0, lambda asig, bsig: False)

class GreaterThan(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '>', lambda a, b: 1 if a > b else 0, lambda asig, bsig: False)

class LessThanOrEqual(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '<=', lambda a, b: 1 if a <= b else 0, lambda asig, bsig: False)

class GreaterThanOrEqual(BinaryOperator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes):
        super().__init__(a, b, '>=', lambda a, b: 1 if a >= b else 0, lambda asig, bsig: False)

class Conditional(Operator):
    def __init__(self, a: ExpressionTypes, b: ExpressionTypes, c: ExpressionTypes):
        self.a = a
        self.b = b
        self.c = c

    def evaluate(self, evaluator):
        assert isinstance(self.a, Expression)
        assert isinstance(self.b, Expression)
        assert isinstance(self.c, Expression)
        aint = self.a.evaluate(evaluator)
        bint = self.b.evaluate(evaluator)
        cint = self.c.evaluate(evaluator)
        if isinstance(aint, Wildcard):
            aint.options = set()
            return aint
        if isinstance(bint, Wildcard):
            bint.options = set()
            return bint
        if isinstance(cint, Wildcard):
            cint.options = set()
            return cint
        assert isinstance(bint, Integer)
        assert isinstance(cint, Integer)
        assert isinstance(aint, Integer)
        unsigned = bint.unsigned or cint.unsigned
        return Integer(bint.value if aint.value else cint.value, unsigned)

    def __str__(self):
        return f'{str(self.a)} ? {str(self.b)} : {str(self.c)}'

PRECEDENCE_MAP: list[dict[str, tuple[int, type[Operator]]]] = [
    {
        '+': (2, UnaryPlus),
        '-': (2, UnaryMinus),
        '!': (2, LogicalNot),
        '~': (2, BitwiseNot)
    },
    {
        '*': (3, Multiply),
        '/': (3, Divide),
        '%': (3, Remainder)
    },
    {
        '+': (3, Add),
        '-': (3, Subtract)
    },
    {
        '<<': (3, LeftShift),
        '>>': (3, RightShift)
    },
    {
        '<': (3, LessThan),
        '<=': (3, LessThanOrEqual),
        '>': (3, GreaterThan),
        '>=': (3, GreaterThanOrEqual)
    },
    {
        '==': (3, Equal),
        '!=': (3, NotEqual)
    },
    {
        '&': (3, BitwiseAnd)
    },
    {
        '^': (3, BitwiseXor)
    },
    {
        '|': (3, BitwiseOr)
    },
    {
        '&&': (3, LogicalAnd)
    },
    {
        '||': (3, LogicalOr)
    },
    {
        '?': (5, Conditional)
    }
]

def parse_expression(tokens: list[TokenType]):
    assert len(tokens) > 0

    # Handle groups, identifiers, defined(), and terminals
    nex: list[ExpressionTypes] = []
    gstart = None
    indent = 0
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == tm.mk_op('('):
            if indent == 0:
                gstart = i+1
            indent += 1
        elif token == tm.mk_op(')'):
            indent -= 1
            if indent == 0:
                assert gstart is not None
                nex.append(Group(parse_expression(tokens[gstart:i])))
                gstart = None
        elif gstart is None:
            if token[0] == 'integer':
                assert type(token[1]) == int
                assert len(token) > 2
                nex.append(Integer(token[1], 'u' in token[2]))
            elif token[0] == 'defined':
                nex.append(UnaryDefined(token[1]))
            elif token[0] in ['identifier', 'keyword']:
                nex.append(Identifier(token[1]))
            elif token[0] == 'operator':
                nex.append(token[1])
            elif token[0] == 'any' and len(token) > 2 and len(token[2]) == 0:
                nex.append(Wildcard())
        i += 1
    assert gstart is None
    cur = nex

    # Scan through for each precedence level
    precedence = 0
    while precedence < len(PRECEDENCE_MAP):
        opset = PRECEDENCE_MAP[precedence]
        merged_any = False
        nex = []
        args: list[ExpressionTypes] = []
        op = None

        prev = None
        for item in cur:
            if isinstance(item, str):
                if isinstance(prev, str): # Something like 1 + -2, or ! ~ 2
                    nex += args
                    args = []
                    op = None
                if item in opset and bool(len(args) == 0) == bool(opset[item][0] == 2):
                    op = opset[item]
                    nex += args[0:-1]
                    del args[0:-1]

            args.append(item)

            if op is not None and len(args) == op[0]:
                value = op[1]
                if op[0] == 2:
                    assert issubclass(value, (UnaryPlus, UnaryMinus, LogicalNot, BitwiseNot))
                    nex.append(value(args[1]))
                elif op[0] == 3:
                    assert issubclass(value, (Multiply, Divide, Remainder, Add, Subtract, LeftShift, RightShift, LessThan, LessThanOrEqual, GreaterThan, GreaterThanOrEqual, Equal, NotEqual, BitwiseAnd, BitwiseXor, BitwiseOr, LogicalAnd, LogicalOr))
                    nex.append(value(args[0], args[2]))
                else:
                    assert issubclass(value, Conditional)
                    nex.append(value(args[0], args[2], args[4]))

                # nex.append(op[1](args[1]) if op[0] == 2
                #     else op[1](args[0], args[2]) if op[0] == 3
                #     else op[1](args[0], args[2], args[4]))
                op = None
                merged_any = True
                args = []

            prev = item

        nex += args
        cur = nex

        if not merged_any:
            precedence += 1

    assert len(cur) == 1 and isinstance(cur[0], Expression)
    return cur[0]

class Evaluator:
    def __init__(self, bitsize: int):
        self.bitsize = bitsize
        self.lookup: (dict[str | int, Def] | None) = None
        self.defines: (dict[Expression | str, bool] | None) = None

    def evaluate(self, tokens: list[TokenType]):
        parsed = parse_expression(tokens)
        result = parsed.evaluate(self).evaluate(self)
        if isinstance(result, Wildcard):
            return result
        return result.value, result.unsigned
