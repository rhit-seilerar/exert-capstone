import itertools

from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.parser.defmap import DefMap
from exert.parser.substitute import substitute
from exert.parser import expressions
from exert.parser.tokenmanager import TokenManager, tok_seq, mk_id, mk_op, mk_int
from exert.utilities.debug import dprint
from exert.utilities.types.global_types import TokenType

class DefEvaluator(expressions.Evaluator):
    def __init__(self, bitsize: int, defmap: DefMap):
        super().__init__(bitsize)
        self.defs = defmap

    def evaluate(self, tokens: list[TokenType]) -> tuple[bool, bool, DefMap]:
        self.matches = DefMap(self.defs)

        # First we run through and replace all defined(MACRO) with a special
        # token so we don't substitute it later. This token will never be
        # serialized, but expressions.py knows how to handle it
        keys: set[TokenType] = set()
        identlike = ['identifier', 'keyword']
        # replmap: dict[str | int, dict[None, list[set[DefOption]]]] = {}
        nex = []
        index = 0
        while index < len(tokens):
            deftok = None
            delta = 1
            if tokens[index] == mk_id('defined'):
                # 'defined MACRO' form
                if index+1 < len(tokens) and tokens[index+1][0] in identlike:
                    deftok = tokens[index+1]
                    delta = 2
                # 'defined ( MACRO )' form
                elif index+3 < len(tokens) and tokens[index+1] == mk_op('(') \
                    and tokens[index+2][0] in identlike and tokens[index+3] == mk_op(')'):
                    deftok = tokens[index+2]
                    delta = 4
            if deftok is None:
                nex.append(tokens[index])
            else:
                nex.append(('defined', deftok[1]))
                keys.add(deftok)
                # if deftok[1] not in replmap:
                #     replmap[deftok[1]] = {None: []}
                # replmap[deftok[1]][None].append({DefOption([deftok])})
            index += delta
        tokens = nex

        # Next we run through and replace all remaining macros with their ANY
        # forms. The replacement itself isn't strictly necessary, the main goal
        # is to construct replmap, which is what we'll permute.
        nex = []
        # replmap = {}
        tokmgr = TokenManager(tokens)
        while tokmgr.has_next():
            nex += substitute(tokmgr, self.defs, keys = keys)#, replmap = replmap)
        tokens = nex

        lookups: list[dict[str | int, Def]] = []
        if keys:
        # if replmap:
            # Note that this currently doesn't consider open-ended definitions correctly
            # Also, wildcards could be improved in accuracy
            lists: list[list[Def]] = []
            keylist = list(keys)
            for index, key in enumerate(keylist):
                lists.append([])
                defn = self.defs[key[1]]
                if not defn.is_defined():
                    lists[-1].append(Def(undefined = True))
                if defn.is_initial() or defn.is_empty_def():
                    lists[-1].append(Def(defined = True))
                for opt in defn.options:
                    lists[-1].append(Def(opt, defined = True))
            permutations = list(itertools.product(*lists))
            lookups = []
            for p in permutations:
                lookups.append({})
                for index, key in enumerate(keylist):
                    lookups[-1][key[1]] = p[index]
        else:
            lookups = [{}]

        self.any_match = False
        self.all_match = True

        def insert_permutation(lookup: dict[str | int, Def], tokens: list[TokenType]) -> list[TokenType]:
            nex = []
            for tok in tokens:
                if tok[0] == 'any' and len(tok) > 2 and len(tok[2]) > 0:
                    repl = lookup[tok[1]].get_replacements(('identifier', tok[1]))
                    repl_toks = list(repl)[0].tokens
                    nex += insert_permutation(lookup, repl_toks)
                else:
                    nex.append(tok)
            return nex

        for lookup in lookups:
            self.defines = {}
            self.lookup = lookup
            current = insert_permutation(lookup, tokens) if lookup else tokens
            parsed = expressions.parse_expression(current)
            result = parsed.evaluate(self).evaluate(self)
            if isinstance(result, expressions.Wildcard):
                self.any_match = True
                self.all_match = False
            elif isinstance(result, expressions.Integer) and result.value == 0:
                self.all_match = False
            else:
                for expression, is_defined in self.defines.items():
                    if is_defined:
                        self.matches.getlocal(expression).defined = True
                    else:
                        self.matches.getlocal(expression).undefined = True

                for lookup_key, lookup_def in lookup.items():
                    if len(lookup_def) > 0:
                        self.matches.define(lookup_key, list(lookup_def.options)[0])
                self.any_match = True
        return self.any_match, self.all_match, self.matches

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
            _, _, matches = self.evaluator.evaluate(self.cond_acc)
            self.evaluator.defs = matches
            self.cond_acc.append(mk_op('&&'))
        self.cond = self.cond_acc + wrapped
        any_match, all_match, matches = self.evaluator.evaluate(self.cond)
        self.cond_acc += [mk_op('!')] + wrapped

        self.apply()
        self.current = matches
        assert self.current is not None
        self.current.skipping = not any_match
        self.skip_rest |= all_match
        self.closed |= closing | self.skip_rest

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
        self.layers = [DefLayer(DefMap(None, initial = cast(dict[ExpressionTypes, Def], initial)), bitsize, False)]
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

    def flat_defines(self) -> dict[ExpressionTypes, Def]:
        result: dict[ExpressionTypes, Def] = {}
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

    def on_define(self, sym: str, tokens: list[TokenType], params: (list[str] | None) = None) -> None:
        if not self.is_skipping():
            dprint(3, '  ' * self.depth() + f'#define {sym} {tok_seq(tokens)}')
            self.keys.add(sym)
            assert self.layers[-1].current is not None
            self.layers[-1].current.define(sym, DefOption(tokens, params))

    def on_undef(self, sym: str) -> None:
        if not self.is_skipping():
            dprint(3, '  ' * self.depth() + f'#undef {sym}')
            self.keys.add(sym)
            assert self.layers[-1].current is not None
            self.layers[-1].current.undefine(sym)

    def on_if(self, cond_tokens: list[TokenType]) -> None:
        dprint(2, '  ' * self.depth() + f'#if {tok_seq(cond_tokens)}')
        parent = self.layers[-1].current
        assert parent is not None
        self.layers.append(DefLayer(parent, self.bitsize, self.is_skipping()))
        self.layers[-1].add_map(cond_tokens)

    def on_ifdef(self, sym: str | int) -> None:
        self.on_if([ mk_id('defined'), mk_id(sym) ])

    def on_ifndef(self, sym: str | int) -> None:
        self.on_if([ mk_op('!'), mk_id('defined'), mk_id(sym) ])

    def on_elif(self, cond_tokens: list[TokenType]) -> None:
        dprint(2, '  ' * self.depth() + f'#elif {tok_seq(cond_tokens)}')
        self.layers[-1].add_map(cond_tokens)

    def on_elifdef(self, sym: str | int) -> None:
        self.on_elif([ mk_id('defined'), mk_id(sym) ])

    def on_elifndef(self, sym: str | int) -> None:
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

    def get_replacements(self, tok: TokenType, params: (list[list[TokenType]] | None) = None) -> set[DefOption]:
        assert self.layers[-1].current is not None
        return self.layers[-1].current.get_replacements(tok, params)

    def substitute(self, tokmgr: (TokenManager | TokenType)) -> list[TokenType]:
        if isinstance(tokmgr, tuple):
            tok = tokmgr
            tokmgr = TokenManager([tok])
        assert self.layers[-1].current is not None
        return substitute(tokmgr, self.layers[-1].current)

    def get_cond_tokens(self) -> list[TokenType]:
        return self.layers[-1].cond
