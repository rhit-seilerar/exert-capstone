import itertools
from typing import cast
from exert.parser.tokenmanager import TokenManager, mk_id
from exert.parser.definition import Def
from exert.parser.defmap import DefMap
from exert.parser.substitute import subst_all
from exert.parser.expressions import Evaluator, Wildcard, Integer, parse_expression
from exert.utilities.types.global_types import TokenType, TokenType3, TokenSeq

# This file evaluates preprocessor-time constants in #if statements.
# The C spec states that first all unary 'defined' operators are evaluated,
# then all macros are expanded, and finally the remaining identifiers are
# replaced with 0, or 1 if it's 'true'.
#
# However, we want to extract some information from these expressions,
# so we handle it a bit differently. 'defined' operators can mark whether
# values may be defined or undefined within the #if block based on the
# truthiness of the result. Other information could be extracted too,
# such as definition values, but that's beyond scope.

class DefEvaluator(Evaluator):
    def __init__(self, bitsize: int, defmap: DefMap):
        super().__init__(bitsize)
        self.defs = defmap

    def replace_unary_defined(self, tokens: TokenSeq, keys: set[TokenType]) -> None:
        # Modifications made to tokmgr.tokens will reflect in tokens
        tokmgr = TokenManager(tokens)
        while tokmgr.has_next():
            # parse 'defined MACRO' or 'defined(MACRO)'
            if tokmgr.consume_identifier('defined'):
                # Grab the token and handle parenthses
                parens = bool(tokmgr.consume_operator('('))
                tok = tokmgr.next()
                if parens and not tokmgr.consume_operator(')'):
                    tok = None

                # If the token is an identifier, replace it with a marker
                if tok and tok[0] in ['identifier', 'keyword']:
                    marker = ('defined', tok[1])
                    tokmgr.tokens[tokmgr.index - 1 - parens] = marker
                    keys.add(tok)
            else:
                tokmgr.bump()

    # Convert a def into a list of singleton defs, each with one option or none
    def make_def_singletons(self, defn: Def) -> list[Def]:
        defs: list[Def] = []

        # If it's not strictly defined, it might be undefined
        if not defn.is_defined():
            defs.append(Def(undefined = True))

        # If it's not strictly undefined, it might be open-ended.
        if not defn.is_undefined():
            defs.append(Def(defined = True))

        # Any specified option might be valid
        for opt in defn.options:
            defs.append(Def(opt, defined = True))

        return defs

    def make_permuted_lookups(self, tokens: TokenSeq,
        keys: set[TokenType]) -> list[dict[str, Def]]:

        # There aren't any macros, so return an empty lookup
        if not keys:
            return [{}]

        # Cast keys into a list for consistent ordering
        keylist = [cast(str, k[1]) for k in keys]

        # Map each macro into singletons
        lists = [self.make_def_singletons(self.defs[k]) for k in keylist]

        # Actually do the permutation
        permutations = list(itertools.product(*lists))

        # Transform the permutation into lookup tables
        return [{k: p[i] for (i, k) in enumerate(keylist)} \
            for p in permutations]

    # Replace all ANY tokens with their values in the lookup table
    # TODO: Move this into substitute.py
    def subst_permutation(self, lookup: dict[str, Def], tokens: TokenSeq) -> TokenSeq:
        nex = []
        for tok in tokens:
            if tok[0] == 'any':
                anytok = cast(TokenType3, tok)
                # Ignore open-ended tokens, they'll be handled by expressions.py
                if len(anytok[2]) > 0:
                    key = cast(str, tok[1])
                    repls = lookup[key].get_replacements(mk_id(key))
                    # Recursively substitute
                    for repl in repls:
                        nex += self.subst_permutation(lookup, repl.tokens)
            else:
                nex.append(tok)
        return nex

    def evaluate_permutation(self, lookup: dict[str, Def], tokens: TokenSeq) -> None:
        # Subsitute the current permutation into tokens
        current = self.subst_permutation(lookup, tokens) if lookup else tokens

        # Parse the substituted expression
        parsed = parse_expression(current)

        # Set up a clean slate and evaluate
        self.defines = {}
        result = parsed.evaluate(self).evaluate(self)

        # Validity is dependent on an open-ended macro, so conceptually at least
        # one option might match, but another might not.
        if isinstance(result, Wildcard):
            self.any_match = True
            self.all_match = False
            return

        assert isinstance(result, Integer)

        # The expression is falsey, so not all options match.
        if result.value == 0:
            self.all_match = False
            return

        # Otherwise, the expression was truthy, so at least one option matches.
        self.any_match = True

        # Since the expression was truthy, mark the defined-ness of all
        # unary defined macros as possible.
        for key, is_defined in (self.defines or {}).items():
            if is_defined:
                self.matches.getlocal(key).defined = True
            else:
                self.matches.getlocal(key).undefine()

        for lookup_key, lookup_def in lookup.items():
            if len(lookup_def) > 0:
                self.matches.define(lookup_key, list(lookup_def.options)[0])

    def evaluate_with_defs(self, tokens: TokenSeq) -> tuple[bool, bool, DefMap]:
        # This tracks the possible values of macros within the upcoming #if block
        self.matches = DefMap(self.defs)

        # Track the ids of all relevant macros
        keys: set[TokenType] = set()

        # First we run through and replace all defined(MACRO) with a special
        # token so we don't substitute it later. This token will never be
        # serialized, but expressions.py knows how to handle it
        self.replace_unary_defined(tokens, keys)

        # Next we run through and replace all remaining macros with their ANY
        # forms. The replacement itself isn't strictly necessary, the main goal
        # is to construct replmap, which is what we'll permute.
        tokens = subst_all(TokenManager(tokens), self.defs, keys, [])

        # Now we permute all relevant macros' options and insert them.
        # Ideally this would be done like in the parser, with continuations,
        # but that's currently out of scope.
        lookups = self.make_permuted_lookups(tokens, keys)

        # Next, we actually evaluate each permutation. We'll also track whether
        # any permutation passed, as well as if all passed, for evaluating
        # whether the #if block should be skipped or closed.
        self.any_match = False
        self.all_match = True
        for lookup in lookups:
            self.evaluate_permutation(lookup, tokens)

        # Return the results and we're done!
        return self.any_match, self.all_match, self.matches
