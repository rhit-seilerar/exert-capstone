from exert.parser.tokenmanager import mk_op
from exert.parser.defmap import DefMap
from exert.parser.defevaluator import DefEvaluator
from exert.utilities.types.global_types import TokenType

class DefLayer:
    """
    A definition layer represents the possible definition states among an entire
    macro scope set: #if/#ifdef/#ifndef, [#elif...], [#else], #endif. It also
    stores a reference to the parent scope's defmap, which is passed to sub-maps.
    
    As each defmap is added, the condition accumulator is applied as initial
    state. This is because, for example, #ifndef ABC would guarantee that ABC
    is undefined in all child maps. To handle #elif and #else, the condition's
    inverse is accumulated for further defmaps.
    
    The layer also stores a 'closed' flag, which determines whether #else was
    encountered. If so, one of the child maps must have been encountered, so
    we can safely replace parent state with accumulated child state. Otherwise,
    we have to include parent state as possible options alongside the merged
    child state.
    """

    def __init__(self, parent: DefMap, bitsize: int, skip_all: bool):
        self.depth = 0
        self.evaluator = DefEvaluator(bitsize, parent)
        self.cond_acc: list[TokenType] = []
        self.cond: list[TokenType] = []
        self.accumulator = DefMap(None)
        self.skip_rest = skip_all
        self.current: (DefMap | None) = None
        self.closed = False
        self.emitted: list[TokenType] = []
        self.blocks: list[list[TokenType]] = []

    def apply(self) -> None:
        if self.current is not None and not self.current.skipping:
            self.accumulator.combine(self.current.defs, replace = False)
            self.current = None

    def add_map(self, cond_tokens: list[TokenType], closing: bool = False) -> None:
        self.depth += 1
        if self.skip_rest:
            self.apply()
            self.current = DefMap(None, skipping = True)
            return

        wrapped = [mk_op('(')] + cond_tokens + [mk_op(')')]
        if len(self.cond_acc) > 0:
            _, _, matches = self.evaluator.evaluate_with_defs(self.cond_acc)
            self.evaluator.defs = matches
            self.cond_acc.append(mk_op('&&'))
        self.cond = self.cond_acc + wrapped
        any_match, all_match, matches = self.evaluator.evaluate_with_defs(self.cond)
        self.cond_acc += [mk_op('!')] + wrapped

        self.apply()
        self.current = matches
        assert self.current is not None
        self.current.skipping = not any_match
        self.skip_rest |= all_match
        self.closed |= closing | self.skip_rest
