type TokenType = (tuple[str, str | int] | tuple[str, str | int, str | set['DefOption']])

type TokenType3 = tuple[str, str | int, str | set['DefOption']]

type ExpressionTypes = 'Expression' | str | int

from exert.parser.defoption import DefOption # Even if the types are strings, the type parser still needs to be able to see them
from exert.parser.expressions import Expression
