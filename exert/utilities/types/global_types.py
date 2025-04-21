from exert.parser.definitions import Def, DefOption
from exert.parser.expressions import UnaryPlus, UnaryMinus, LogicalNot, BitwiseNot

type TokenType = (tuple[str, str | int] | tuple[str, str | int, str | set[DefOption]])