from exert.utilities.tokenmanager import tok_seq
from exert.utilities.debug import dprint

def def_dict_str(defs):
    strs = [f'{key}: {str(defs[key])}' for key in defs]
    return f'{{ {", ".join(strs)} }}'

class DefOption:
    def __init__(self, tokens):
        self.tokens = tokens
        self.key = tok_seq(tokens)
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
        self.undefined = undefined
        self.defined = defined
        self.options = set()
        for option in options:
            self.define(option, keep = True)
        self.validate()

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

    def get_replacements(self, sym):
        """
        [ initial,   {}      ]: [[sym]]
        [ undefined, {}      ]: [[sym]]
        [ defined,   options ]: [options]
        [ uncertain, options ]: [[sym], options]
        """
        replacements = set()
        if self.undefined or not self.defined:
            replacements.add(DefOption([sym]))
        if self.defined:
            replacements |= self.options
        return replacements

    def invert(self):
        """
        [ initial,   {}      ]: [ initial,   {}      ]
        [ undefined, {}      ]: [ defined,   {}      ]
        [ defined,   options ]: [ undefined, {}      ]
        [ uncertain, options ]: [ undefined, {}      ]
        """
        if self.is_initial():
            pass
        elif self.is_undefined():
            self.undefined = False
            self.defined = True
        elif self.is_defined():
            self.undefined = True
            self.defined = False
            self.options.clear()
        else:
            self.defined = False
            self.options.clear()
        return self

    def combine(self, other, replace):
        if not isinstance(other, Def):
            raise TypeError(other)
        if replace:
            self.defined = other.defined
            self.undefined = other.undefined
            if not other.defined or len(other) > 0:
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
        if other.defined and len(other) == 0:
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

    def copy(self):
        new_defs = {}
        for key in self.defs:
            new_defs[key] = self.defs[key].copy()
        return DefMap(self.parent, self.skipping, new_defs)

    def getlocal(self, key):
        if key not in self.defs:
            self.defs[key] = Def()
        return self.defs[key]

    def __getitem__(self, key):
        if key in self.defs:
            return self.defs[key]
        if self.parent is not None:
            return self.parent[key]
        return Def()

    def __setitem__(self, key, item):
        if not isinstance(item, Def):
            raise TypeError(item)
        self.defs[key] = item

    def validate(self):
        for key in self.defs:
            self[key].validate()

    def undefine(self, key):
        if not self.skipping:
            self.getlocal(key).undefine(keep = False)

    def define(self, key, option):
        if not self.skipping:
            self.getlocal(key).define(option, keep = True)

    def invert(self):
        if not self.skipping:
            for key in self.defs:
                self[key] = self[key].copy().invert()
        return self

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

class DefLayer:
    """
    A definition layer represents the possible definition states among an entire
    macro scope set: #if/#ifdef/#ifndef, [#elif...], [#else], #endif. It also
    stores a reference to the parent scope's defmap, which is passed to sub-maps.
    
    As each defmap is added, the conditions map is applied as initial state. This
    is because, for example, #ifndef ABC would guarantee that ABC is undefined
    in all child maps. To handle #elif and #else, the condition's inverse is
    accumulated into the conditions map for further defmaps.
    
    The layer also stores a 'closed' flag, which determines whether #else was
    encountered. If so, one of the child maps must have been encountered, so
    we can safely replace parent state with accumulated child state. Otherwise,
    we have to include parent state as possible options alongside the merged
    child state.
    """

    def __init__(self, skipping):
        self.conditions = DefMap(None, skipping = skipping)
        self.accumulator = DefMap(None, skipping = skipping)
        self.any_kept = False
        self.current = None
        self.closed = False

    def reset_current(self):
        self.current = None

    def apply(self):
        if self.current is not None:
            self.accumulator.combine(self.current.defs, replace = False)
            self.reset_current()

    def add_map(self, conditions, skipping, closing = False):
        if conditions is not None and not isinstance(conditions, DefMap):
            raise TypeError(conditions)
        self.apply()
        if skipping:
            self.current = DefMap(None, skipping = True)
        else:
            self.current = conditions.copy()
            self.current.combine(self.conditions.defs, replace = False)
            self.any_kept = True
        self.conditions.combine(conditions.copy().invert().defs, replace = False)
        self.closed |= closing

class DefState:
    """
    The DefState tracks all possible definition values over the course of the
    preprocessor. As each directive is encountered, an internal hierarchy of
    definition maps is updated, each storing possible values and defined-ness
    of symbols.
    """

    def __init__(self, initial = None):
        self.keys = set()
        self.layers = [DefLayer(False)]
        self.layers[0].add_map(DefMap(None, False, initial), False, closing = True)

    def depth(self):
        return len(self.layers) - 1

    def is_skipping(self):
        return self.layers[-1].current.skipping

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

    def on_define(self, sym, params, tokens):
        if not self.is_skipping():
            dprint(3, '  ' * self.depth() + f'#define {sym} {tok_seq(tokens)}')
            self.keys.add(sym)
            self.layers[-1].current.define(sym, DefOption(tokens))

    def on_undef(self, sym):
        if not self.is_skipping():
            dprint(3, '  ' * self.depth() + f'#undef {sym}')
            self.keys.add(sym)
            self.layers[-1].current.undefine(sym)

    def on_if(self, conditions):
        dprint(2, '  ' * self.depth() + f'#if {def_dict_str(conditions)}')
        parent = self.layers[-1].current if len(self.layers) > 0 else None
        defmap = DefMap(parent, initial = conditions)
        skipping = not self.layers[-1].current.matches(defmap)
        self.layers.append(DefLayer(self.is_skipping()))
        self.layers[-1].add_map(defmap, skipping)
        return not skipping

    def on_ifdef(self, sym):
        return self.on_if({ sym: Def(defined = True) })

    def on_ifndef(self, sym):
        return self.on_if({ sym: Def(undefined = True) })

    def on_elif(self, conditions):
        dprint(2, '  ' * self.depth() + f'#elif {def_dict_str(conditions)}')
        defmap = DefMap(self.layers[-2].current, initial = conditions)
        skipping = not self.layers[-1].current.matches(defmap)
        self.layers[-1].add_map(defmap, skipping)
        return not skipping

    def on_elifdef(self, sym):
        return self.on_elif({ sym: Def(defined = True) })

    def on_elifndef(self, sym):
        return self.on_if({ sym: Def(undefined = True) })

    def on_else(self):
        dprint(2, '  ' * self.depth() + '#else')
        defmap = DefMap(self.layers[-2].current)
        skipping = not self.layers[-1].current.matches(defmap)
        self.layers[-1].add_map(defmap, skipping, closing = True)
        return not skipping

    def on_endif(self):
        dprint(2, '  ' * self.depth() + '#endif')
        self.layers[-1].apply()
        layer = self.layers.pop()
        self.layers[-1].current.combine(layer.accumulator.defs, replace = layer.closed)

    def get_replacements(self, sym_tok):
        replacements = self.layers[-1].current[sym_tok[1]].options.copy()
        if not self.layers[-1].current[sym_tok[1]].is_defined():
            replacements.add(DefOption([sym_tok]))
        return replacements
