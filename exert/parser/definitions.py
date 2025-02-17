# class DefOption:
#     def __init__(self, tokens):
#         self.tokens = tokens
#         self.key = tok_seq(tokens)
#         self.len = len(self.tokens)
#         self.hash = hash(self.key)
# 
#     def __eq__(self, other):
#         return isinstance(other, DefOption) and other.key == self.key
# 
#     def __hash__(self):
#         return self.hash
# 
#     def __contains__(self, element):
#         return element in self.tokens
# 
#     def __iter__(self):
#         return iter(self.tokens)
# 
#     def __len__(self):
#         return self.len
# 
#     def __getitem__(self, key):
#         return self.tokens[key]
# 
# DefOption.UNDEF = DefOption([('optional', '<undef>')])
# DefOption.OTHER = DefOption([('optional', '<other>')])
# 
# class Def:
#     """
#     This class stores potential values for a single definition. It consists of four states:
#     [ !defined, !undefined  {}      ]: The default value, representing definitions that
#       haven't been #defined or #undefined yet
#     [ !defined,  undefined  {}      ]: This has been explicitly #undefined
#     [  defined, !undefined, options ]: This has been explicitly #defined
#     [  defined,  undefined, options ]: This was defined in one sub-scope and undefined in another
#     """
# 
#     def __init__(self, *options, defined = False, undefined = False):
#         self.undefined = undefined
#         self.defined = defined
#         self.options = set()
#         for option in options:
#             self.add(option)
# 
#     def is_initial(self):
#         return not self.undefined and not self.defined
# 
#     def is_undefined(self):
#         return self.undefined and not self.defined
# 
#     def is_defined(self):
#         return not self.undefined and self.defined
# 
#     def is_uncertain(self):
#         return self.undefined and self.defined
# 
#     def undefine(self, keep = True):
#         self.undefined = True
#         if not keep:
#             self.defined = False
#             self.options.clear()
# 
#     def define(self, option, keep = True):
#         assert isinstance(option, DefOption)
#         self.options.add(option)
#         if self.is_undefined() or not keep:
#             self.undefined = False
#         self.defined = True
# 
#     def get_replacements(self, sym):
#         """
#         [ initial,   {}      ]: [[sym]]
#         [ undefined, {}      ]: [[sym]]
#         [ defined,   options ]: [options]
#         [ uncertain, options ]: [[sym], options]
#         """
#         replacements = []
#         if self.undefined or not self.defined:
#             replacements.append([sym])
#         if self.defined:
#             replacements += self.options
#         return replacements
# 
#     def __str__(self):
#         if self.is_initial():
#             return '<initial>'
#         if self.is_undefined():
#             return '<undefined>'
#         return tok_seq_list(self.get_replacements(('identifier', '<undefined>')))
# 
# class DefMap:
#     """
#     DefMaps represent a possible state of definitions within a macro scope.
#     They store a reference to the outer scope's defmap, as well as a set of
#     mappings between symbols to their definitions.
#     """
# 
#     def __init__(self, parent, skipping = False, initial = None):
#         assert parent is None or isinstance(parent, DefMap)
#         assert initial is None or isinstance(initial, dict)
#         self.skipping = skipping
#         self.parent = parent
#         self.defs = initial or {}
# 
#     def copy(self):
#         return DefMap(self.parent, self.skipping, self.defs.copy())
# 
#     def getlocal(self, key):
#         if key not in self.defs:
#             self.defs[key] = Def()
#         return self.defs[key]
# 
#     def __getitem__(self, key):
#         if key in self.defs:
#             return self.defs[key]
#         if self.parent is not None:
#             return self.parent[key]
#         return Def()
# 
#     def __setitem__(self, key, item):
#         assert isinstance(item, Def)
#         self.defs[key] = item
# 
#     def undefine(self, key):
#         if not self.skipping:
#             self.getlocal(key).undefine(keep = False)
# 
#     def define(self, key, option):
#         if not self.skipping:
#             self.getlocal(key).define(option, keep = True)
#             if defn == Def.DEFAULT or defn == Def.UNDEF:
#                 self.defs[sym] = Def(option)
#             else:
#                 self.defs[sym].add(option)
#             dprint(4, f'::::Defining {sym}: {str(defn)} <- {str(self.defs[sym])}')
# 
#     def invert(self):
#         """
#         Invert all specified definitions in this map. Specifically:
#         - None -> None
#         - UNDEF -> []
#         - [UNDEF,...] -> [UNDEF]
#         - [...] -> UNDEF
#         """
#         result = self.copy()
#         dprint(4, f'::::Inverting (Skipping: {self.skipping})')
#         if not self.skipping:
#             for sym in self.defs:
#                 defn = self.defs.get(sym)
#                 if self.get(sym) == Def.DEFAULT:
#                     pass
#                 elif defn.is_undefined():
#                     result.defs[sym] = Def()
#                 elif defn.is_defined():
#                     result.defs[sym] = Def.UNDEF
#                 else:
#                     result.defs[sym] = Def(undefined = True)
#                 dprint(4, f'::::::Inverting {sym}: {tok_seq_list(defn)} -> ' \
#                     f'{tok_seq_list(result.defs[sym])}')
#         return result
# 
#     def overwrite(self, state):
#         """
#         For each key specified in state, overwrite the current definition with
#         its value. As a special case, empty definitions ([]) don't overwrite if
#         the existing value is defined. This allows #ifdef to work properly.
#         """
#         assert isinstance(state, dict)
#         dprint(4, f'::::Overwriting (Skipping: {self.skipping})')
#         if not self.skipping:
#             for sym in state:
#                 if not self.is_defined(sym) or state[sym] != {}:
#                     dprint(4, f'::::::Overwriting {sym}: {tok_seq_list(self.defs[sym])} <- ' \
#                         f'{tok_seq_list(state[sym])}')
#                     self.defs[sym] = state[sym]
# 
#     def merge(self, state):
#         """
#         For each key specified in state, merge with the current state. Specifically:
#         TODO merging with None means other options may still be possible
#         None + ??? -> ???
#         ??? + None -> ???
#         UNDEF + UNDEF -> UNDEF
#         UNDEF + [UNDEF,B] -> [UNDEF,B]
#         UNDEF + [B] -> [UNDEF,B]
#         [UNDEF,A] + UNDEF -> [UNDEF,A]
#         [UNDEF,A] + [UNDEF,B] -> [UNDEF,A,B]
#         [UNDEF,A] + [B] -> [UNDEF,A,B]
#         [A] + UNDEF -> [UNDEF,A]
#         [A] + [UNDEF,B] -> [UNDEF,A,B]
#         [A] + [B] -> [A, B]
#         """
#         assert isinstance(state, dict)
#         dprint(4, f'::::Merging (Skipping: {self.skipping})')
#         if self.skipping:
#             return
#         for sym in state:
#             defn1 = self.get(sym)
#             defn2 = state.get(sym)
#             if defn1 is None:
#                 self.defs[sym] = defn2
#             elif defn2 is None:
#                 pass
#             elif defn1 == DefMap.UNDEF:
#                 if defn2 == DefMap.UNDEF:
#                     self.defs[sym] = defn2
#                 elif len(defn2) and defn2[0] == DefMap.UNDEF:
#                     self.defs[sym] = defn2
#                 else:
#                     self.defs[sym] = [DefMap.UNDEF] + defn2
#             elif len(defn1) and defn1[0] == DefMap.UNDEF:
#                 if defn2 == DefMap.UNDEF:
#                     pass
#                 elif len(defn2) and defn2[0] == DefMap.UNDEF:
#                     self.defs[sym] = defn1[1:] + defn2[1:]
#                 else:
#                     self.defs[sym] = defn1[1:] + defn2
#             else:
#                 if defn2 == DefMap.UNDEF:
#                     self.defs[sym] = [DefMap.UNDEF] + defn1
#                 elif len(defn2) and defn2[0] == DefMap.UNDEF:
#                     self.defs[sym] = [DefMap.UNDEF] + defn1 + defn2[1:]
#                 else:
#                     self.defs[sym] = defn1 + defn2
#             dprint(4, f'::::::Merging {sym}: {tok_seq_list(self.defs.get(sym))} <- ' \
#                 f'{tok_seq_list(defn1)} + {tok_seq_list(defn2)}')
# 
# class DefLayer:
#     """
#     A definition layer represents the possible definition states among an entire
#     macro scope set: #if/#ifdef/#ifndef, [#elif...], [#else], #endif. It also
#     stores a reference to the parent scope's defmap, which is passed to sub-maps.
#     
#     As each defmap is added, the conditions map is applied as initial state. This
#     is because, for example, #ifndef ABC would guarantee that ABC is  undefined
#     in all child maps. To handle #elif and #else, the condition's inverse is
#     accumulated into the conditions map for further defmaps.
#     
#     The layer also stores a 'closed' flag, which determines whether #else was
#     encountered. If so, one of the child maps must have been encountered, so
#     we can safely replace parent state with accumulated child state. Otherwise,
#     we have to include parent state as possible options alongside the merged
#     child state.
#     """
# 
#     def __init__(self, skipping):
#         """
#         Construct a new layer given a parent defmap, or None if this is the root.
#         """
#         self.conditions = DefMap(None, skipping = skipping)
#         self.accumulator = DefMap(None, skipping = skipping)
#         self.any_kept = False
#         self.current = None
#         self.closed = False
# 
#     def reset_current(self):
#         self.current = None
# 
#     def apply(self):
#         """
#         Apply the current defmap to the accumulated state and reset it.
#         """
#         if self.current is not None:
#             dprint(4, '::Merging into accumulator')
#             self.accumulator.merge(self.current.defs)
#             self.reset_current()
# 
#     def add_map(self, conditions, skipping, closing = False):
#         """
#         Add a new defmap with the given conditions map and accumulate into the
#         overall conditions. If 'closing' is True, mark the layer as closed.
#         """
#         assert conditions is None or isinstance(conditions, DefMap)
#         self.apply()
#         dprint(4, f':Adding (Skipping: {skipping})')
#         if skipping:
#             self.current = DefMap(None, True)
#         else:
#             dprint(4, '::Merging previous conditions')
#             self.current = conditions.copy()
#             self.current.merge(self.conditions.defs)
#             dprint(4, '::Merging new conditions')
#             self.any_kept = True
#         self.conditions.merge(conditions.invert().defs)
#         self.closed |= closing
# 
# class DefState:
#     """
#     The DefState tracks all possible definition values over the course of the
#     preprocessor. As each directive is encountered, an internal hierarchy of
#     definition maps is updated, each storing possible values and defined-ness
#     of symbols.
#     """
# 
#     def __init__(self, initial = None):
#         self.keys = set()
#         self.layers = [DefLayer(False)]
#         self.layers[0].add_map(DefMap(None, False, initial), False, closing = True)
# 
#     def depth(self):
#         return len(self.layers) - 1
# 
#     def is_skipping(self):
#         return self.layers[-1].current.skipping
# 
#     def flat_defines(self):
#         result = {}
#         for key in self.keys:
#             defn = self.layers[-1].current.get(key) or {}
#             if len(defn) == 0 or defn[0] != DefMap.UNDEF:
#                 result[key] = defn
#         return result
# 
#     def flat_unknowns(self):
#         result = set()
#         for key in self.keys:
#             if self.layers[-1].current.is_unknown(key):
#                 result.add(key)
#         return result
# 
#     def on_define(self, sym, tokens):
#         if not self.is_skipping():
#             dprint(3, '  ' * self.depth() + f'#define {sym} {tok_seq(tokens)}')
#             self.keys.add(sym)
#             self.layers[-1].current.define(sym, tokens)
# 
#     def on_undef(self, sym):
#         if not self.is_skipping():
#             dprint(3, '  ' * self.depth() + f'#undef {sym}')
#             self.keys.add(sym)
#             self.layers[-1].current.undefine(sym)
# 
#     def test_conditions(self, conditions):
#         for sym in conditions.defs:
#             cond = conditions.get(sym)
#             defn = self.layers[-1].current.get(sym)
#             dprint(4, f'::Testing {sym}:', tok_seq_list(cond), '<=>', tok_seq_list(defn))
#             if cond is None or defn is None:
#                 continue
# 
#             is_unknown = self.layers[-1].current.is_unknown(sym)
#             is_undefined = self.layers[-1].current.is_undefined(sym)
#             if cond == DefMap.UNDEF:
#                 if is_unknown or is_undefined:
#                     continue
# 
#             if cond == set():
#                 continue
# 
#             cond_opts = set(tok_seq(t) for t in conditions.get(sym).opts)
#             defn_opts = set(tok_seq(t) for t in self.layers[-1].current.get(sym).opts)
#             if len(cond_opts & defn_opts) > 0:
#                 continue
# 
#             return False
#         return True
# 
#     def on_if(self, conditions):
#         dprint(2, '  ' * self.depth() + f'#if {conditions}')
#         parent = self.layers[-1].current if len(self.layers) > 0 else None
#         defmap = DefMap(parent, initial = conditions)
#         skipping = not self.test_conditions(defmap)
#         self.layers.append(DefLayer(self.is_skipping()))
#         self.layers[-1].add_map(defmap, skipping)
#         return not skipping
# 
#     def on_ifdef(self, sym):
#         return self.on_if({ sym: {} })
# 
#     def on_ifndef(self, sym):
#         return self.on_if({ sym: DefMap.UNDEF })
# 
#     def on_elif(self, conditions):
#         dprint(2, '  ' * self.depth() + f'#elif {conditions}')
#         defmap = DefMap(self.layers[-2].current, initial = conditions)
#         skipping = not self.test_conditions(defmap)
#         self.layers[-1].add_map(defmap, skipping)
#         return not skipping
# 
#     def on_elifdef(self, sym):
#         return self.on_elif({ sym: {} })
# 
#     def on_elifndef(self, sym):
#         return self.on_if({ sym: DefMap.UNDEF })
# 
#     def on_else(self):
#         dprint(2, '  ' * self.depth() + '#else')
#         defmap = DefMap(self.layers[-2].current)
#         defmap.skipping = not self.test_conditions(defmap)
#         self.layers[-1].add_map(defmap, True)
#         return not defmap.skipping
# 
#     def on_endif(self):
#         dprint(2, '  ' * self.depth() + '#endif')
#         self.layers[-1].apply()
#         layer = self.layers.pop()
#         if layer.closed:
#             self.layers[-1].current.overwrite(layer.accumulator.defs)
#         else:
#             self.layers[-1].current.merge(layer.accumulator.defs)
# 
#     def get_replacements(self, sym):
#         replacements = self.layers[-1].current.get_options(sym)
#         if not self.layers[-1].current.is_defined(sym):
#             replacements.append(sym)
#         return replacements
