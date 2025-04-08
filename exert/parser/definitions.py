import itertools

from exert.parser import expressions
from exert.parser.tokenmanager import TokenManager, tok_seq, mk_id, mk_op, mk_int
from exert.utilities.debug import dprint

class DefOption:
    def __init__(self, tokens, params = None):
        assert isinstance(tokens, list)
        self.tokens = tokens
        self.params = params
        self.paramstr = '' if params is None else ','.join(params)
        self.key = tok_seq(tokens)
        if self.paramstr:
            self.key = self.paramstr + '$' + self.key
        self.len = len(tokens)
        self.hash = hash(self.key)

    def __eq__(self, other):
        return isinstance(other, DefOption) and other.key == self.key

    def __hash__(self):
        return self.hash

    def __len__(self):
        return self.len

    def __str__(self):
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

    def __init__(self, *options, defined = False, undefined = False):
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

    def is_invalid(self):
        return not self.defined and len(self.options) > 0

    def is_initial(self):
        return not self.undefined and not self.defined

    def is_undefined(self):
        return self.undefined and not self.defined

    def is_defined(self):
        return not self.undefined and self.defined

    def is_empty_def(self):
        return self.defined and len(self.options) == 0

    def is_uncertain(self):
        return self.undefined and self.defined

    def undefine(self, keep = True):
        self.undefined = True
        if not keep:
            self.defined = False
            self.options.clear()

    def define(self, option, keep = True):
        if not isinstance(option, DefOption):
            raise TypeError(option)
        if self.is_undefined() or not keep:
            self.undefined = False
        self.options.add(option)
        self.defined = True

    def get_replacements(self, sym, params = None):
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

    def combine(self, other, replace):
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

    def matches(self, other):
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

    def __len__(self):
        return len(self.options)

    def __eq__(self, other):
        return isinstance(other, Def) \
            and self.defined == other.defined \
            and self.undefined == other.undefined \
            and self.options == other.options

    def __str__(self):
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

    def __init__(self, parent, skipping = False, initial = None):
        assert parent is None or isinstance(parent, DefMap)
        assert initial is None or isinstance(initial, dict)
        self.skipping = skipping
        self.parent = parent
        self.defs = initial or {}
        self.validate()

    def getlocal(self, key):
        if key not in self.defs:
            self.defs[key] = Def()
        return self.defs[key]

    def __getitem__(self, key):
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

    def __setitem__(self, key, item):
        if not isinstance(item, Def):
            raise TypeError(item)
        self.defs[key] = item

    def get_replacements(self, sym_tok, params = None):
        return self[sym_tok[1]].get_replacements(sym_tok, params)

    def validate(self):
        for key in self.defs:
            self[key].validate()

    def undefine(self, key):
        if not self.skipping:
            self.getlocal(key).undefine(keep = False)

    def define(self, key, option):
        if not self.skipping:
            self.getlocal(key).define(option, keep = True)

    def combine(self, other, replace):
        if not isinstance(other, dict):
            raise TypeError(other)
        if not self.skipping:
            for key in other:
                self[key] = self[key].copy().combine(other[key], replace = replace)
        return self

    def matches(self, conditions):
        if not isinstance(conditions, DefMap):
            raise TypeError(conditions)
        for key in conditions.defs:
            if not self[key].matches(conditions[key]):
                return False
        return True

    def __eq__(self, other):
        return isinstance(other, DefMap) \
            and self.parent == other.parent \
            and self.skipping == other.skipping \
            and self.defs == other.defs

    def __str__(self):
        defs_strs = [f"'{key}': {str(self.defs[key])}" for key in self.defs]
        return f'DefMap(parent = {self.parent}, skipping = {self.skipping}, ' \
            f'defs = {{{", ".join(defs_strs)}}})'

def substitute(tokmgr, defmap, replmap = None, keys = None):
    def parse_macro(tokmgr):
        bindex = tokmgr.index
        if tokmgr.peek_type() not in ['identifier', 'keyword']:
            return None, []
        name = tokmgr.next()
        if not defmap[name[1]].defined:
            tokmgr.index = bindex
            return None, []
        params = []
        if tokmgr.consume_operator('('):
            depth = 1
            pindex = tokmgr.index
            while tokmgr.has_next() and depth > 0:
                if tokmgr.consume_operator('('):
                    depth += 1
                elif tokmgr.consume_operator(')'):
                    depth -= 1
                elif tokmgr.consume_operator(',') and depth == 1:
                    params.append(tokmgr.tokens[pindex:tokmgr.index])
                    pindex = tokmgr.index + 1
                else:
                    tokmgr.bump()
            if depth > 0:
                tokmgr.index = bindex
                return None, []
            params.append(tokmgr.tokens[pindex:tokmgr.index])
        return name, params

    expansion_stack = []
    def subst(tokmgr):
        index = tokmgr.index
        name, params = parse_macro(tokmgr)
        if name is None or name[1] in expansion_stack or defmap[name[1]].is_initial():
            tokmgr.index = index
            return None
        substitutions = set()
        if isinstance(keys, set):
            keys.add(name)
        opts = defmap.get_replacements(name, params)
        if opts == {DefOption([name])}:
            tokmgr.index = index
            return None
        if opts == {DefOption([])}:
            return []
        expansion_stack.append(name[1])
        for opt in opts:
            tokens = []
            optmgr = TokenManager(opt.tokens)
            while optmgr.has_next():
                tokens += subst(optmgr) or [optmgr.next()]
            if tokens:
                substitutions.add(DefOption(tokens))
        expansion_stack.pop()
        macroname = name[1]
        if len(params) > 0:
            macroname += '(' + ', '.join(tok_seq(p) for p in params) + ')'
        if replmap is not None:
            replmap[macroname] = substitutions
        if len(substitutions) > 1:
            return [('any', macroname, substitutions)]
        return list(substitutions)[0].tokens

    result = subst(tokmgr)
    return [tokmgr.next()] if result is None else result

class DefEvaluator(expressions.Evaluator):
    def __init__(self, bitsize, defmap):
        super().__init__(bitsize)
        self.defs = defmap

    def evaluate(self, tokens):
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
        tokmgr = TokenManager(tokens)
        while tokmgr.has_next():
            nex += substitute(tokmgr, self.defs, keys = keys)
        tokens = nex

        lookups = []
        if keys:
            # Note that this currently doesn't consider open-ended definitions correctly
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

        def insert_permutation(lookup, tokens):
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

    def __init__(self, parent, bitsize, skip_all):
        self.depth = 0
        self.evaluator = DefEvaluator(bitsize, parent)
        self.cond_acc = []
        self.cond = []
        self.accumulator = DefMap(None)
        self.skip_rest = skip_all
        self.current = None
        self.closed = False

    def apply(self):
        if self.current is not None and not self.current.skipping:
            self.accumulator.combine(self.current.defs, replace = False)
            self.current = None

    def add_map(self, cond_tokens, closing = False):
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

    def __init__(self, bitsize, initial = None):
        self.bitsize = bitsize
        self.keys = set()
        self.layers = [DefLayer(DefMap(None, initial = initial), bitsize, False)]
        self.layers[0].add_map([mk_int(1)], closing = True)
        if initial is not None:
            self.keys |= set(initial.keys())

    def depth(self):
        return len(self.layers) - 1

    def is_skipping(self):
        return self.layers[-1].current.skipping

    def is_guaranteed(self):
        return not self.is_skipping() and self.layers[-1].skip_rest

    def flat_defines(self):
        result = {}
        for key in self.keys:
            defn = self.layers[-1].current[key]
            if defn.is_defined():
                result[key] = defn
        return result

    def flat_unknowns(self):
        result = set()
        for key in self.keys:
            if self.layers[-1].current[key].is_uncertain():
                result.add(key)
        return result

    def on_define(self, sym, tokens, params = None):
        if not self.is_skipping():
            dprint(3, '  ' * self.depth() + f'#define {sym} {tok_seq(tokens)}')
            self.keys.add(sym)
            self.layers[-1].current.define(sym, DefOption(tokens, params))

    def on_undef(self, sym):
        if not self.is_skipping():
            dprint(3, '  ' * self.depth() + f'#undef {sym}')
            self.keys.add(sym)
            self.layers[-1].current.undefine(sym)

    def on_if(self, cond_tokens):
        dprint(2, '  ' * self.depth() + f'#if {tok_seq(cond_tokens)}')
        parent = self.layers[-1].current
        self.layers.append(DefLayer(parent, self.bitsize, self.is_skipping()))
        self.layers[-1].add_map(cond_tokens)

    def on_ifdef(self, sym):
        self.on_if([ mk_id('defined'), mk_id(sym) ])

    def on_ifndef(self, sym):
        self.on_if([ mk_op('!'), mk_id('defined'), mk_id(sym) ])

    def on_elif(self, cond_tokens):
        dprint(2, '  ' * self.depth() + f'#elif {tok_seq(cond_tokens)}')
        self.layers[-1].add_map(cond_tokens)

    def on_elifdef(self, sym):
        self.on_elif([ mk_id('defined'), mk_id(sym) ])

    def on_elifndef(self, sym):
        self.on_elif([ mk_op('!'), mk_id('defined'), mk_id(sym) ])

    def on_else(self):
        dprint(2, '  ' * self.depth() + '#else')
        self.layers[-1].add_map([mk_int(1)], closing = True)

    def on_endif(self):
        dprint(2, '  ' * self.depth() + '#endif')
        self.layers[-1].apply()
        layer = self.layers.pop()
        self.layers[-1].current.combine(layer.accumulator.defs, replace = layer.closed)

    def get_replacements(self, tok, params = None):
        return self.layers[-1].current.get_replacements(tok, params)

    def substitute(self, tokmgr):
        if isinstance(tokmgr, tuple):
            tok = tokmgr
            tokmgr = TokenManager([tok])
        return substitute(tokmgr, self.layers[-1].current)

    def get_cond_tokens(self):
        return self.layers[-1].cond
