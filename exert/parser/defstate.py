from typing import cast, Optional
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.defmap import DefMap
from exert.parser.deflayer import DefLayer
from exert.parser.substitute import substitute
from exert.parser.tokenmanager import TokenManager, tok_seq, mk_id, mk_op, mk_int
from exert.utilities.debug import dprint
from exert.utilities.types.global_types import TokenType, TokenSeq, DefmapBacking

class DefState:
    """
    The DefState tracks all possible definition values over the course of the
    preprocessor. As each directive is encountered, an internal hierarchy of
    definition maps is updated, each storing possible values and defined-ness
    of symbols.
    """

    def __init__(self, bitsize: int, initial: (dict[str, Def] | None) = None):
        self.bitsize = bitsize
        self.keys: set[str] = set()
        self.layers = [DefLayer(DefMap(None, initial = cast(DefmapBacking, initial)), \
            bitsize, False)]
        self.layers[0].add_map([mk_int(1)], closing = True)
        if initial is not None:
            self.keys |= set(initial.keys())

    def depth(self) -> int:
        return len(self.layers) - 1

    def is_skipping(self) -> bool:
        assert self.layers[-1].current is not None
        return self.layers[-1].current.skipping

    def is_guaranteed(self) -> bool:
        return not self.is_skipping() and self.layers[-1].skip_rest

    def flat_defines(self) -> DefmapBacking:
        result: DefmapBacking = {}
        for key in self.keys:
            assert self.layers[-1].current is not None
            defn = self.layers[-1].current[key]
            if defn.is_defined():
                result[key] = defn
        return result

    def flat_unknowns(self) -> set[str]:
        result: set[str] = set()
        assert self.layers[-1].current is not None
        for key in self.keys:
            if self.layers[-1].current[key].is_uncertain():
                result.add(key)
        return result

    def on_define(self, sym: str, tokens: TokenSeq,
        params: Optional[list[str]] = None) -> None:

        if not self.is_skipping():
            dprint(3, '  ' * self.depth() + f'#define {sym} {tok_seq(tokens)}')
            self.keys.add(sym)
            assert self.layers[-1].current is not None
            self.layers[-1].current.define(sym, DefOption(tokens, params), keep = False)

    def on_undef(self, sym: str) -> None:
        if not self.is_skipping():
            dprint(3, '  ' * self.depth() + f'#undef {sym}')
            self.keys.add(sym)
            assert self.layers[-1].current is not None
            self.layers[-1].current.undefine(sym)

    def on_if(self, cond_tokens: TokenSeq) -> None:
        dprint(2, '  ' * self.depth() + f'#if {tok_seq(cond_tokens)}')
        parent = self.layers[-1].current
        assert parent is not None
        self.layers.append(DefLayer(parent, self.bitsize, self.is_skipping()))
        self.layers[-1].add_map(cond_tokens)

    def on_ifdef(self, sym: str) -> None:
        self.on_if([ mk_id('defined'), mk_id(sym) ])

    def on_ifndef(self, sym: str) -> None:
        self.on_if([ mk_op('!'), mk_id('defined'), mk_id(sym) ])

    def on_elif(self, cond_tokens: list[TokenType]) -> None:
        dprint(2, '  ' * self.depth() + f'#elif {tok_seq(cond_tokens)}')
        self.layers[-1].add_map(cond_tokens)

    def on_elifdef(self, sym: str) -> None:
        self.on_elif([ mk_id('defined'), mk_id(sym) ])

    def on_elifndef(self, sym: str) -> None:
        self.on_elif([ mk_op('!'), mk_id('defined'), mk_id(sym) ])

    def on_else(self) -> None:
        dprint(2, '  ' * self.depth() + '#else')
        self.layers[-1].add_map([mk_int(1)], closing = True)

    def on_endif(self) -> None:
        dprint(2, '  ' * self.depth() + '#endif')
        self.layers[-1].apply()
        layer = self.layers.pop()
        assert self.layers[-1].current is not None
        self.layers[-1].current.combine(layer.accumulator.defs, replace = layer.closed)

    def get_replacements(self, tok: TokenType) -> set[DefOption]:
        assert self.layers[-1].current is not None
        return self.layers[-1].current.get_replacements(tok)

    def get_current(self, key: str) -> Def:
        assert self.layers[-1].current is not None
        return self.layers[-1].current[key]

    def substitute(self, tokmgr: (TokenManager | TokenType)) -> TokenSeq:
        if isinstance(tokmgr, tuple):
            tok = tokmgr
            tokmgr = TokenManager([tok])
        assert self.layers[-1].current is not None
        return substitute(tokmgr, self.layers[-1].current)

    def get_cond_tokens(self) -> TokenSeq:
        return self.layers[-1].cond
