import itertools

from typing import Any

from exert.parser import expressions
from exert.parser.tokenmanager import tok_seq, mk_id, mk_op, mk_int
from exert.utilities.debug import dprint
# from exert.parser import DefOption


class DefOption:
    def __init__(self, tokens: list):
        assert isinstance(tokens, list)
        self.tokens = tokens
        self.key = tok_seq(tokens)
        self.len = len(tokens)
        self.hash = hash(self.key)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, DefOption) and other.key == self.key

    def __hash__(self) -> int:
        return self.hash

    def __len__(self) -> int:
        return self.len

    def __str__(self) -> str:
        return self.key

class Def:
    """
    This class stores potential values for a single definition. It consists of four states:
    [ !defined, !undefined  {}      ]: The default value, representing definitions that
      haven't been #defined or #undefined yet
    [ !defined,  undefined  {}      ]: This has been explicitly #undefined
    [  defined, !undefined, options ]: This has been explicitly #defined
    [  defined,  undefined, options ]: This was defined in one sub-scope and undefined in another
    """

    def __init__(self, *options: set, defined: bool = False, undefined: bool = False):
        self.options = set()
        self.undefined = undefined
        self.defined = defined
        if len(options) > 0:
            for option in options:
                self.define(option, keep = True)
            self.undefined = undefined

    def validate(self):
        if self.is_invalid():
            raise ValueError(self.options)

    def copy(self):
        return Def(*self.options, defined = self.defined, undefined = self.undefined)

    def is_invalid(self) -> bool:
        return not self.defined and len(self.options) > 0

    def is_initial(self) -> bool:
        return not self.undefined and not self.defined

    def is_undefined(self) -> bool:
        return self.undefined and not self.defined

    def is_defined(self) -> bool:
        return not self.undefined and self.defined

    def is_empty_def(self) -> bool:
        return self.defined and len(self.options) == 0

    def is_uncertain(self) -> bool:
        return self.undefined and self.defined

    def undefine(self, keep: bool = True):
        self.undefined = True
        if not keep:
            self.defined = False
            self.options.clear()

    def define(self, option: DefOption, keep: bool = True):
        if not isinstance(option, DefOption):
            raise TypeError(option)
        if self.is_undefined() or not keep:
            self.undefined = False
        self.options.add(option)
        self.defined = True

    def get_replacements(self, sym: Any) -> set:
        """
        [ initial,   {}      ]: [[{}]]
        [ undefined, {}      ]: [[sym]]
        [ defined,   options ]: [options]
        [ defined,   {}      ]: [[{}]]
        [ uncertain, options ]: [[sym], options]
        [ uncertain, {}      ]: [[sym], [{}]]
        """
        replacements = self.options.copy()
        if self.undefined:
            replacements.add(DefOption([sym]))
        elif len(self.options) == 0:
            replacements.add(DefOption([('any', sym[1], set())]))
        return replacements

    def combine(self, other, replace: Any):
        if not isinstance(other, Def):
            raise TypeError(other)
        if replace:
            self.defined = other.defined
            self.undefined = other.undefined
            if not other.is_empty_def():
                self.options = other.options.copy()
        else:
            self.defined |= other.defined
            self.undefined |= other.undefined
            self.options |= other.options
        return self

    def matches(self, other) -> bool:
        if not isinstance(other, Def):
            raise TypeError(other)
        if other.is_initial() or self.is_initial():
            return True
        if other.is_undefined():
            if self.is_undefined() or self.is_uncertain():
                return True
        if other.is_empty_def():
            return True
        if len(other.options & self.options) > 0:
            return True
        return False

    def __len__(self) -> int:
        return len(self.options)

    def __eq__(self, other) -> bool:
        return isinstance(other, Def) \
            and self.defined == other.defined \
            and self.undefined == other.undefined \
            and self.options == other.options

    def __str__(self) -> str:
        if self.is_invalid():
            return '<invalid>'
        if self.is_initial():
            return '<initial>'
        if self.is_undefined():
            return '<undefined>'
        replacements = self.get_replacements(('identifier', '<undefined>'))
        return f'{{ {", ".join(str(r) for r in replacements).strip()} }}'

class DefMap:
    """
    DefMaps represent a possible state of definitions within a macro scope.
    They store a reference to the outer scope's defmap, as well as a set of
    mappings between symbols to their definitions.
    """

    def __init__(self, parent, skipping: bool = False, initial: dict | None = None):
        assert parent is None or isinstance(parent, DefMap)
        assert initial is None or isinstance(initial, dict)
        self.skipping = skipping
        self.parent = parent
        self.defs = initial or {}
        self.validate()

    def getlocal(self, key: Any) -> dict:
        if key not in self.defs:
            self.defs[key] = Def()
        return self.defs[key]

    def __getitem__(self, key: Any) -> (Def | dict | Any):
        if key in self.defs:
            defn = self.getlocal(key)
            if defn.is_empty_def() and self.parent is not None:
                return Def(
                    *self.parent[key].options,
                    defined = defn.defined,
                    undefined = defn.undefined)
            return defn
        if self.parent is not None:
            return self.parent[key]
        return Def()

    def __setitem__(self, key: Any, item: Def):
        if not isinstance(item, Def):
            raise TypeError(item)
        self.defs[key] = item

    def get_replacements(self, sym_tok: Any) -> (set|Any):
        return self[sym_tok[1]].get_replacements(sym_tok)

    def validate(self):
        for key in self.defs:
            self[key].validate()

    def undefine(self, key: Any):
        if not self.skipping:
            self.getlocal(key).undefine(keep = False)

    def define(self, key: Any, option: Any):
        if not self.skipping:
            self.getlocal(key).define(option, keep = True)

    def combine(self, other: dict, replace: Any):
        if not isinstance(other, dict):
            raise TypeError(other)
        if not self.skipping:
            for key in other:
                self[key] = self[key].copy().combine(other[key], replace = replace)
        return self

    def matches(self, conditions: object) -> bool:
        if not isinstance(conditions, DefMap):
            raise TypeError(conditions)
        for key in conditions.defs:
            if not self[key].matches(conditions[key]):
                return False
        return True

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DefMap) \
            and self.parent == other.parent \
            and self.skipping == other.skipping \
            and self.defs == other.defs

    def __str__(self) -> str:
        defs_strs = [f"'{key}': {str(self.defs[key])}" for key in self.defs]
        return f'DefMap(parent = {self.parent}, skipping = {self.skipping}, ' \
            f'defs = {{{", ".join(defs_strs)}}})'

def substitute(defmap: list, tok: Any, keys: set = None) -> (list[Any] | list | list[tuple[str, Any, set]] | Any):
    expansion_stack = []
    def subst(token: tuple) -> (list | list[tuple[str, Any, set]] | Any | None):
        if token[0] not in ['identifier', 'keyword']:
            return None
        if token[1] in expansion_stack:
            return None
        if defmap[token[1]].is_initial():
            return None
        substitutions = set()
        if isinstance(keys, set):
            keys.add(token)
        opts = defmap.get_replacements(token)
        if opts == {DefOption([token])}:
            return None
        if opts == {DefOption([])}:
            return []
        expansion_stack.append(token[1])
        for opt in opts:
            tokens = []
            for opt_token in opt.tokens:
                tokens += subst(opt_token) or [opt_token]
            if tokens:
                substitutions.add(DefOption(tokens))
        expansion_stack.pop()
        if len(substitutions) > 1:
            return [('any', token[1], substitutions)]
        return list(substitutions)[0].tokens
    result = subst(tok)
    return [tok] if result is None else result

class DefEvaluator(expressions.Evaluator):
    def __init__(self, bitsize: int, defmap: list):
        super().__init__(bitsize)
        self.defs = defmap

    def evaluate(self, tokens: list) -> tuple[bool, bool, DefMap]:
        self.matches = DefMap(self.defs)

        keys = set()
        identlike = ['identifier', 'keyword']
        nex = []
        i = 0
        while i < len(tokens):
            if tokens[i] == mk_id('defined'):
                if i+1 < len(tokens) and tokens[i+1][0] in identlike:
                    nex.append(('defined', tokens[i+1][1]))
                    keys.add(tokens[i+1])
                    i += 2
                    continue
                if i+3 < len(tokens) and tokens[i+1] == mk_op('(') \
                    and tokens[i+2][0] in identlike and tokens[i+3] == mk_op(')'):
                    nex.append(('defined', tokens[i+2][1]))
                    keys.add(tokens[i+2])
                    i += 4
                    continue
            nex.append(tokens[i])
            i += 1
        tokens = nex

        nex = []
        for tok in tokens:
            nex += substitute(self.defs, tok, keys)
        tokens = nex

        lookups = []
        if keys:
            # Permute all multi-value macros into a chain of 'or's
            # TODO please improve this
            # Note that this currently doesn't consider open-ended
            # definitions correctly
            # Also, wildcards could be improved in accuracy
            lists = []
            keylist = list(keys)
            for i, k in enumerate(keylist):
                lists.append([])
                defn = self.defs[k[1]]
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
                for i, k in enumerate(keylist):
                    lookups[-1][k[1]] = p[i]
        else:
            lookups = [{}]

        self.any_match = False
        self.all_match = True

        def insert_permutation(lookup: dict, tokens: list) -> list:
            nex = []
            for tok in tokens:
                if tok[0] == 'any' and len(tok[2]) > 0:
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
            elif result.value == 0:
                self.all_match = False
            else:
                for k, v in self.defines.items():
                    if v:
                        self.matches.getlocal(k).defined = True
                    else:
                        self.matches.getlocal(k).undefined = True
                for k, v in lookup.items():
                    if len(v) > 0:
                        self.matches.define(k, list(v.options)[0])
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

    def __init__(self, parent: list, bitsize: int, skip_all):
        self.depth = 0
        self.evaluator = DefEvaluator(bitsize, parent)
        self.cond_acc = []
        self.cond = []
        self.accumulator = DefMap(None)
        self.skip_rest = skip_all
        self.current = None
        self.closed = False

    def apply(self):
        if self.current is not None:
            self.accumulator.combine(self.current.defs, replace = False)
            self.current = None

    def add_map(self, cond_tokens: list, closing: bool = False):
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

    def __init__(self, bitsize: int, initial: Any|None = None):
        self.bitsize = bitsize
        self.keys = set()
        self.layers = [DefLayer(DefMap(None, initial = initial), bitsize, False)]
        self.layers[0].add_map([mk_int(1)], closing = True)
        if initial is not None:
            self.keys |= set(initial.keys())

    def depth(self) -> int:
        return len(self.layers) - 1

    def is_skipping(self) -> bool:
        return self.layers[-1].current.skipping

    def is_guaranteed(self) -> bool:
        return not self.is_skipping() and self.layers[-1].skip_rest

    def flat_defines(self) -> dict:
        result = {}
        for key in self.keys:
            defn = self.layers[-1].current[key]
            if defn.is_defined():
                result[key] = defn
        return result

    def flat_unknowns(self) -> set:
        result = set()
        for key in self.keys:
            if self.layers[-1].current[key].is_uncertain():
                result.add(key)
        return result

    def on_define(self, sym: Any, params:list, tokens: tuple):
        if not self.is_skipping():
            dprint(3, '  ' * self.depth() + f'#define {sym} {tok_seq(tokens)}')
            self.keys.add(sym)
            self.layers[-1].current.define(sym, DefOption(tokens))

    def on_undef(self, sym: Any):
        if not self.is_skipping():
            dprint(3, '  ' * self.depth() + f'#undef {sym}')
            self.keys.add(sym)
            self.layers[-1].current.undefine(sym)

    def on_if(self, cond_tokens: list):
        dprint(2, '  ' * self.depth() + f'#if {tok_seq(cond_tokens)}')
        parent = self.layers[-1].current
        self.layers.append(DefLayer(parent, self.bitsize, self.is_skipping()))
        self.layers[-1].add_map(cond_tokens)

    def on_ifdef(self, sym: Any):
        self.on_if([ mk_id('defined'), mk_id(sym) ])

    def on_ifndef(self, sym: Any):
        self.on_if([ mk_op('!'), mk_id('defined'), mk_id(sym) ])

    def on_elif(self, cond_tokens: list):
        dprint(2, '  ' * self.depth() + f'#elif {tok_seq(cond_tokens)}')
        self.layers[-1].add_map(cond_tokens)

    def on_elifdef(self, sym: Any):
        self.on_elif([ mk_id('defined'), mk_id(sym) ])

    def on_elifndef(self, sym: Any):
        self.on_elif([ mk_op('!'), mk_id('defined'), mk_id(sym) ])

    def on_else(self):
        dprint(2, '  ' * self.depth() + '#else')
        self.layers[-1].add_map([mk_int(1)], closing = True)

    def on_endif(self):
        dprint(2, '  ' * self.depth() + '#endif')
        self.layers[-1].apply()
        layer = self.layers.pop()
        self.layers[-1].current.combine(layer.accumulator.defs, replace = layer.closed)

    def get_replacements(self, tok) -> (set|Any):
        return self.layers[-1].current.get_replacements(tok)

    def substitute(self, tok: Any)-> (list[Any] | list | list[tuple[str, Any, set]] | Any):
        return substitute(self.layers[-1].current, tok)

    def get_cond_tokens(self) -> list:
        return self.layers[-1].cond
