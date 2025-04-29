import itertools
from exert.parser.tokenmanager import TokenManager, mk_id, mk_op
from exert.parser.definition import Def
from exert.parser.defmap import DefMap
from exert.parser.substitute import substitute
from exert.parser.expressions import Evaluator, Wildcard, Integer, parse_expression
from exert.utilities.types.global_types import TokenType

class DefEvaluator(Evaluator):
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
                assert self.defs is not None
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

        def insert_permutation(lookup: dict[str | int, Def], tokens: list[TokenType]) \
            -> list[TokenType]:
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
            parsed = parse_expression(current)
            result = parsed.evaluate(self).evaluate(self)
            if isinstance(result, Wildcard):
                self.any_match = True
                self.all_match = False
            elif isinstance(result, Integer) and result.value == 0:
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
