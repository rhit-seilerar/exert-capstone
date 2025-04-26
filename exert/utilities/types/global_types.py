from exert.parser.definitions import DefOption
from exert.parser.expressions import Expression
from typing import TypeVar

type TokenType = (tuple[str, str | int] | tuple[str, str | int, str | set[DefOption]])

type TokenType3 = tuple[str, str | int, str | set[DefOption]]

type ExpressionTypes = (Expression | str | int)
