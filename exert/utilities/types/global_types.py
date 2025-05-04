type TokenType2 = tuple[str, str | int]
type TokenType3 = tuple[str, str | int, str | set['DefOption']]
type TokenType = TokenType2 | TokenType3
type TokenSeq = list[TokenType]

type ExpressionTypes = 'Expression' | str | int
type DefmapKey = str | int
type DefmapBacking = dict[DefmapKey, 'Def']

# Even if the types are strings, the type parser still needs to be able to see them
from exert.parser.defoption import DefOption # pylint: disable=unused-import
from exert.parser.definition import Def # pylint: disable=unused-import
from exert.parser.expressions import Expression # pylint: disable=unused-import
