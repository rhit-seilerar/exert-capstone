import os
from exert.utilities.tokenmanager import tok_seq_list, tok_seq, tok_str, TokenManager
from exert.utilities.debug import dprint

class DefMap:
    """
    DefMaps represent a possible state of definitions within a macro scope.
    They store a reference to the outer scope's defmap, as well as a set of
    mappings between symbols to their definitions.
    """

    UNDEF = 'undef'
    """
    The unique symbol marking definitions as explicitly undefined. While it
    could technically be any non-None, non-list value, having an explicit
    value is useful for debugging.
    """

    def __init__(self, parent, skipping = False, initial = None):
        """
        Constructs a new defmap. The parent is the previous layer's defmap,
        or None if this is the root. Optionally, initial state can be specified.
        """
        assert parent is None or isinstance(parent, DefMap)
        assert initial is None or isinstance(initial, dict)
        self.skipping = skipping
        self.parent = parent
        self.defs = initial or {}

    def copy(self):
        return DefMap(self.parent, self.skipping, self.defs.copy())

    def get(self, sym):
        """
        Retrieve this DefMap's value for a given symbol, or look it up from the
        parent if it's not found.
        """
        if sym in self.defs:
            return self.defs[sym]
        if self.parent is not None:
            return self.parent.get(sym)
        return None

    def get_options(self, sym):
        defn = self.get(sym)
        if defn is None or defn == DefMap.UNDEF:
            return []
        if len(defn) > 0 and defn[0] == DefMap.UNDEF:
            return defn[1:]
        return defn

    def is_unknown(self, sym):
        """
        Definitions are unknown if they're None, since all definitions default to
        unknown. Definitions are also unknown if they contain UNDEF as their first
        option, since we don't know if they're defined or not.
        """
        defn = self.get(sym)
        return defn is None or (isinstance(defn, list) and len(defn) and defn[0] == DefMap.UNDEF)

    def is_undefined(self, sym):
        """
        Definitions are undefined if their value equals UNDEF. They
        are only considered undefined after an explicit #undef, before any
        following #define.
        """
        return self.get(sym) == DefMap.UNDEF

    def is_defined(self, sym):
        """
        Definitions are defined if their value is a list, since definitions
        consist of lists of valid possibilities. However, they're only defined
        if the list doesn't contain UNDEF, since that would mean the defined-ness
        is unknown.
        """
        defn = self.get(sym)
        return isinstance(defn, list) and (len(defn) == 0 or defn[0] != DefMap.UNDEF)

    def undefine(self, sym):
        if not self.skipping:
            dprint(f'    Undefining {sym}: {tok_seq_list(self.defs.get(sym))} <- {DefMap.UNDEF}')
            self.defs[sym] = DefMap.UNDEF

    def define(self, sym, tokens):
        if not self.skipping:
            defn = self.defs.get(sym)
            if isinstance(defn, list):
                self.defs[sym].append(tokens)
            elif tokens == []:
                self.defs[sym] = []
            else:
                self.defs[sym] = [tokens]
            dprint(f'    Defining {sym}: {tok_seq_list(defn)} <- {tok_seq_list(self.defs[sym])}')

    def invert(self):
        """
        Invert all specified definitions in this map. Specifically:
        - None -> None
        - [...] -> UNDEF
        - UNDEF -> []
        - [UNDEF,...] -> [UNDEF]
        """
        result = self.copy()
        dprint(f'    Inverting (Skipping: {self.skipping})')
        if not self.skipping:
            for sym in self.defs:
                defn = self.defs.get(sym)
                if self.get(sym) is None:
                    pass
                elif defn == DefMap.UNDEF:
                    result.defs[sym] = []
                elif len(defn) and defn[0] == DefMap.UNDEF:
                    result.defs[sym] = [DefMap.UNDEF]
                else:
                    result.defs[sym] = DefMap.UNDEF
                dprint(f'      Inverting {sym}: {tok_seq_list(defn)} -> ' \
                    f'{tok_seq_list(result.defs[sym])}')
        return result

    def overwrite(self, state):
        """
        For each key specified in state, overwrite the current definition with
        its value. As a special case, empty definitions ([]) don't overwrite if
        the existing value is defined. This allows #ifdef to work properly.
        """
        assert isinstance(state, dict)
        dprint(f'    Overwriting (Skipping: {self.skipping})')
        if not self.skipping:
            for sym in state:
                if not self.is_defined(sym) or state[sym] != []:
                    dprint(f'      Overwriting {sym}: {tok_seq_list(self.defs[sym])} <- ' \
                        f'{tok_seq_list(state[sym])}')
                    self.defs[sym] = state[sym]

    def merge(self, state):
        """
        For each key specified in state, merge with the current state. Specifically:
        TODO merging with None means other options may still be possible
        None + ??? -> ???
        ??? + None -> ???
        UNDEF + UNDEF -> UNDEF
        UNDEF + [UNDEF,B] -> [UNDEF,B]
        UNDEF + [B] -> [UNDEF,B]
        [UNDEF,A] + UNDEF -> [UNDEF,A]
        [UNDEF,A] + [UNDEF,B] -> [UNDEF,A,B]
        [UNDEF,A] + [B] -> [UNDEF,A,B]
        [A] + UNDEF -> [UNDEF,A]
        [A] + [UNDEF,B] -> [UNDEF,A,B]
        [A] + [B] -> [A, B]
        """
        assert isinstance(state, dict)
        dprint(f'    Merging (Skipping: {self.skipping})')
        if self.skipping:
            return
        for sym in state:
            defn1 = self.get(sym)
            defn2 = state.get(sym)
            if defn1 is None:
                self.defs[sym] = defn2
            elif defn2 is None:
                pass
            elif defn1 == DefMap.UNDEF:
                if defn2 == DefMap.UNDEF:
                    self.defs[sym] = defn2
                elif len(defn2) and defn2[0] == DefMap.UNDEF:
                    self.defs[sym] = defn2
                else:
                    self.defs[sym] = [DefMap.UNDEF] + defn2
            elif len(defn1) and defn1[0] == DefMap.UNDEF:
                if defn2 == DefMap.UNDEF:
                    pass
                elif len(defn2) and defn2[0] == DefMap.UNDEF:
                    self.defs[sym] = defn1[1:] + defn2[1:]
                else:
                    self.defs[sym] = defn1[1:] + defn2
            else:
                if defn2 == DefMap.UNDEF:
                    self.defs[sym] = [DefMap.UNDEF] + defn1
                elif len(defn2) and defn2[0] == DefMap.UNDEF:
                    self.defs[sym] = [DefMap.UNDEF] + defn1 + defn2[1:]
                else:
                    self.defs[sym] = defn1 + defn2
            dprint(f'      Merging {sym}: {tok_seq_list(self.defs[sym])} <- ' \
                f'{tok_seq_list(defn1)} + {tok_seq_list(defn2)}')

class DefLayer:
    """
    A definition layer represents the possible definition states among an entire
    macro scope set: #if/#ifdef/#ifndef, [#elif...], [#else], #endif. It also
    stores a reference to the parent scope's defmap, which is passed to sub-maps.
    
    As each defmap is added, the conditions map is applied as initial state. This
    is because, for example, #ifndef ABC would guarantee that ABC is  undefined
    in all child maps. To handle #elif and #else, the condition's inverse is
    accumulated into the conditions map for further defmaps.
    
    The layer also stores a 'closed' flag, which determines whether #else was
    encountered. If so, one of the child maps must have been encountered, so
    we can safely replace parent state with accumulated child state. Otherwise,
    we have to include parent state as possible options alongside the merged
    child state.
    """

    def __init__(self, skipping):
        """
        Construct a new layer given a parent defmap, or None if this is the root.
        """
        self.conditions = DefMap(None, skipping = skipping)
        self.accumulator = DefMap(None, skipping = skipping)
        self.any_kept = False
        self.current = None
        self.closed = False

    def reset_current(self):
        self.current = None

    def apply(self):
        """
        Apply the current defmap to the accumulated state and reset it.
        """
        if self.current is not None:
            dprint('  Merging into accumulator')
            self.accumulator.merge(self.current.defs)
            self.reset_current()

    def add_map(self, conditions, skipping, closing = False):
        """
        Add a new defmap with the given conditions map and accumulate into the
        overall conditions. If 'closing' is True, mark the layer as closed.
        """
        assert conditions is None or isinstance(conditions, DefMap)
        self.apply()
        dprint(f' Adding (Skipping: {skipping})')
        if skipping:
            self.current = DefMap(None, True)
        else:
            dprint('  Merging previous conditions')
            self.current = conditions.copy()
            self.current.merge(self.conditions.defs)
            dprint('  Merging new conditions')
            self.any_kept = True
        self.conditions.merge(conditions.invert().defs)
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

    def is_skipping(self):
        return self.layers[-1].current.skipping

    def flat_defines(self):
        result = {}
        for key in self.keys:
            defn = self.layers[-1].current.get(key) or []
            if len(defn) == 0 or defn[0] != DefMap.UNDEF:
                result[key] = defn
        return result

    def flat_unknowns(self):
        result = set()
        for key in self.keys:
            if self.layers[-1].current.is_unknown(key):
                result.add(key)
        return result

    def on_define(self, sym, tokens):
        if not self.is_skipping():
            dprint(f'#define {sym} {tok_seq(tokens)}')
            self.keys.add(sym)
            self.layers[-1].current.define(sym, tokens)

    def on_undef(self, sym):
        if not self.is_skipping():
            dprint(f'#undef {sym}')
            self.keys.add(sym)
            self.layers[-1].current.undefine(sym)

    def test_conditions(self, conditions):
        for sym in conditions.defs:
            cond = conditions.get(sym)
            defn = self.layers[-1].current.get(sym)
            dprint(f'  Testing {sym}:', tok_seq_list(cond), '<=>', tok_seq_list(defn))
            if cond is None or defn is None:
                continue

            is_unknown = self.layers[-1].current.is_unknown(sym)
            is_undefined = self.layers[-1].current.is_undefined(sym)
            if cond == DefMap.UNDEF:
                if is_unknown or is_undefined:
                    continue

            if cond == []:
                continue

            cond_opts = set(tok_seq(t) for t in conditions.get_options(sym))
            defn_opts = set(tok_seq(t) for t in self.layers[-1].current.get_options(sym))
            if len(cond_opts & defn_opts) > 0:
                continue

            return False
        return True

    def on_if(self, conditions):
        dprint(f'#if {conditions}')
        parent = self.layers[-1].current if len(self.layers) > 0 else None
        defmap = DefMap(parent, initial = conditions)
        skipping = not self.test_conditions(defmap)
        self.layers.append(DefLayer(self.is_skipping()))
        self.layers[-1].add_map(defmap, skipping)
        return not skipping

    def on_ifdef(self, sym):
        return self.on_if({ sym: [] })

    def on_ifndef(self, sym):
        return self.on_if({ sym: DefMap.UNDEF })

    def on_elif(self, conditions):
        dprint(f'#elif {conditions}')
        defmap = DefMap(self.layers[-2].current, initial = conditions)
        skipping = not self.test_conditions(defmap)
        self.layers[-1].add_map(defmap, skipping)
        return not skipping

    def on_elifdef(self, sym):
        return self.on_elif({ sym: [] })

    def on_elifndef(self, sym):
        return self.on_if({ sym: DefMap.UNDEF })

    def on_else(self):
        dprint('#else')
        defmap = DefMap(self.layers[-2].current)
        defmap.skipping = not self.test_conditions(defmap)
        self.layers[-1].add_map(defmap, True)
        return not defmap.skipping

    def on_endif(self):
        dprint('#endif')
        self.layers[-1].apply()
        layer = self.layers.pop()
        if layer.closed:
            self.layers[-1].current.overwrite(layer.accumulator.defs)
        else:
            self.layers[-1].current.merge(layer.accumulator.defs)

    def get_replacements(self, sym):
        replacements = self.layers[-1].current.get_options(sym)
        if not self.layers[-1].current.is_defined(sym):
            replacements.append(sym)
        return replacements

class Preprocessor(TokenManager):
    def __init__(self, tokenizer, includes):
        super().__init__()
        self.tokenizer = tokenizer
        self.includes = includes
        self.unresolved = list()
        self.defs = DefState()

    def load_file(self, path, is_relative):
        if self.defs.is_skipping():
            return

        includes = self.includes.copy()
        if is_relative:
            includes.insert(0, os.path.dirname(self.file))
        for include in includes:
            load_path = ''
            if isinstance(include, tuple):
                load_path = os.path.join(include[0], include[1](path))
            else:
                load_path = os.path.join(include, path)

            data = ''
            try:
                with open(load_path, 'r', encoding = 'utf-8') as file:
                    dprint(f'Loading path: {load_path}')
                    data = file.read()
            except IOError:
                continue
            prefix = f'#line 1 "{load_path}"\n'
            suffix = f'\n#line 1 "{self.file}"' if self.file else '\n#line 1'
            to_insert = prefix + data + suffix
            self.insert(to_insert)
            return True
        self.unresolved.append(path)
        self.err('Failed to include', path)
        return True

    def push_optional(self, name):
        self.conditions.append(name)
        self.insert(('optional', name), True)

    def pop_optional(self):
        self.insert(('optional', None), True)
        return self.conditions.pop()

    def skip_to_newline(self, offset = 0):
        tokens = []
        while not self.peek_type() == 'newline':
            tokens.append(self.next())
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(len(tokens) + 3 + offset)
        return tokens

    def handle_line(self):
        if not (line := self.consume_type('integer')):
            return self.err('#line must be followed by a line number')
        if (file := self.consume_type('string')):
            self.file = file[1]
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        dprint("#line", line, f'"{file}"' if file else '')
        self.remove(5 if file else 4)
        return True

    def handle_include(self):
        if not (file := self.consume_type('string')):
            return self.err('#include must be followed by a path')
        if file[2] not in ['', '<']:
            return self.err('#include cannot have string literal modifiers')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        dprint('#include', f'<{file}>' if file[2] == '<' else f'"{file}"')
        self.remove(4)
        return self.load_file(file[1], file[2] != '<')

    def handle_define(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#define must be followed by an identifier')
        if (tokens := self.skip_to_newline(1)) is None:
            return False
        self.defs.on_define(name, tokens)
        return True

    def handle_undef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#undef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        self.defs.on_undef(name)
        return True

    def handle_ifdef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#ifdef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        if self.defs.on_ifdef(name):
            self.push_optional(f'defined({name})')
        return True

    def handle_ifndef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#ifndef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        if self.defs.on_ifndef(name):
            self.push_optional(f'!defined({name})')
        return True

    def handle_elifdef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#elifdef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(4)
        condition = None
        if self.defs.layers[-1].any_kept:
            condition = self.pop_optional()
        if self.defs.on_elifdef(name):
            if condition is not None:
                self.push_optional(f'!({condition}) && defined({name})')
            else:
                self.push_optional(f'defined({name})')
        return True

    def handle_elifndef(self):
        if not (name := self.parse_ident_or_keyword()):
            return self.err('#elifndef must be followed by an identifier')
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        condition = None
        if self.defs.layers[-1].any_kept:
            condition = self.pop_optional()
        if self.defs.on_elifndef(name):
            if condition is not None:
                self.push_optional(f'!({condition}) && !defined({name})')
            else:
                self.push_optional(f'!defined({name})')
        self.remove(4)
        return True

    def handle_if(self):
        if not (tokens := self.skip_to_newline()):
            return False
        if self.defs.on_if({}):
            self.push_optional(' '.join(str(n[1]) for n in tokens))
        return True

    def handle_elif(self):
        if not (tokens := self.skip_to_newline()):
            return False
        condition = None
        if self.defs.layers[-1].any_kept:
            condition = self.pop_optional()
        if self.defs.on_elif({}):
            cond_str = " ".join(str(n) for n in tokens)
            if condition is not None:
                self.push_optional(f'!({condition}) && ({cond_str})')
            else:
                self.push_optional(f'{cond_str}')
        return True

    def handle_else(self):
        #TODO get cond str from defmap conditions
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(3)
        condition = None
        if self.defs.layers[-1].any_kept:
            condition = self.pop_optional()
        if self.defs.on_else():
            if condition is not None:
                self.push_optional(f'!({condition})')
            else:
                self.push_optional('')
        return True

    def handle_endif(self):
        if not self.consume_type('newline'):
            return self.err('Directives must end with a linebreak')
        self.remove(3)
        if self.defs.layers[-1].any_kept:
            self.pop_optional()
        self.defs.on_endif()
        return True

    def handle_error(self):
        dprint('#error')
        return self.skip_to_newline()

    def handle_warning(self):
        dprint('#warning')
        return self.skip_to_newline()

    def handle_pragma(self):
        dprint('#pragma')
        return self.skip_to_newline()

    def parse_directive(self):
        result = None
        if self.consume(('identifier', 'line')):
            result = self.handle_line()
        elif self.consume_identifier('include'):
            result = self.handle_include()
        elif self.consume_identifier('define'):
            result = self.handle_define()
        elif self.consume_identifier('undef'):
            result = self.handle_undef()
        elif self.consume_identifier('ifdef'):
            result = self.handle_ifdef()
        elif self.consume_identifier('ifndef'):
            result = self.handle_ifndef()
        elif self.consume_identifier('elifdef'):
            result = self.handle_elifdef()
        elif self.consume_identifier('elifndef'):
            result = self.handle_elifndef()
        elif self.consume_keyword('if'):
            result = self.handle_if()
        elif self.consume_identifier('elif'):
            result = self.handle_elif()
        elif self.consume_keyword('else'):
            result = self.handle_else()
        elif self.consume_identifier('endif'):
            result = self.handle_endif()
        elif self.consume_identifier('error'):
            result = self.handle_error()
        elif self.consume_identifier('warning'):
            result = self.handle_warning()
        elif self.consume_identifier('pragma'):
            result = self.handle_pragma()
        else:
            return self.err(f'Unknown preprocessor directive #{self.next()[1]}')
        return result

    def insert(self, tokens, before = False):
        if isinstance(tokens, str):
            tokens = self.tokenizer.tokenize(tokens)
        if isinstance(tokens, tuple):
            tokens = [tokens]
        prefix = self.tokens[:self.index]
        suffix = self.tokens[self.index:]
        size = len(tokens)
        self.tokens = prefix + tokens + suffix
        self.len += size
        if before:
            self.index += size

    def remove(self, count, index = None):
        index = index if index else self.index
        assert index <= self.index
        del self.tokens[index-count:index]
        self.len -= count
        self.index -= count

    def substitute(self):
        def subst(token):
            if token[0] not in ['identifier', 'keyword']:
                return None
            substitutions = []
            opts = self.defs.get_replacements(token[1])
            if opts == [token[1]]:
                return None
            for opt in opts:
                tokens = []
                for token in (opt or []):
                    tokens += subst(token) or [token]
                if tokens:
                    substitutions.append(tokens)
            if len(substitutions) > 1:
                return [('any', substitutions)]
            elif len(substitutions) == 1:
                return substitutions[0]
            return []

        tok = self.next()
        result = subst(tok)
        if result is not None:
            dprint(f"Substituting {tok[0]} '{tok[1]}': {tok_seq(result)}")
            self.remove(1)
            self.insert(result)

    def preprocess(self, data):
        super().reset()
        self.conditions = []
        self.depth = 0
        self.file = ''
        self.insert(data)

        # String combination not implemented
        # Stringification and concatenation not implemented

        while self.has_next() and not self.has_error:
            if self.consume_directive('#'):
                self.parse_directive()
                continue

            if self.defs.is_skipping():
                self.next()
                continue

            if self.peek_type() in ['identifier', 'keyword']:
                self.substitute()
                continue

            self.bump()

        return self

    def __str__(self):
        tokens = tok_seq(self.tokens)
        definitions = '\n'.join(f'{d[0]}: {tok_seq_list(d[1])}' \
            for d in self.defs.flat_defines().items())
        unknowns = '\n'.join(self.defs.flat_unknowns())
        return f'\n===== TOKENS =====\n{tokens}\n' \
            f'\n===== DEFINITIONS =====\n{definitions}\n' \
            f'\n===== UNKNOWNS =====\n{unknowns}\n'
