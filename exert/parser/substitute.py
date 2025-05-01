from typing import cast
from exert.parser.tokenmanager import TokenManager
from exert.parser.defoption import DefOption
from exert.parser.defmap import DefMap
from exert.utilities.logic import or_else
from exert.utilities.types.global_types import TokenType

def parse_macro(tokmgr: TokenManager, defmap: DefMap) \
    -> tuple[None | TokenType, None | list[list[TokenType]]]:
    """
    Consume macro application syntax, e.g. an identifier for a variable-like
    macro and name(p1, p2, ...) for a function-like macro. Note that, for
    simplicity, all options for a definition must be either variable-like,
    or function-like with the same number of arguments.
    """

    bindex = tokmgr.index
    # We only substitute identifiers or keywords
    if tokmgr.peek_type() not in ['identifier', 'keyword']:
        return None, None
    name = tokmgr.next()
    assert name is not None
    # If the identifier isn't defined, we won't touch it
    defn = defmap[name[1]]
    if not defn.defined or defn.is_empty_def():
        tokmgr.index = bindex
        return None, None

    # This is a variable-like macro, so just return the name
    if defn.plen == -1:
        return name, None

    # This is a function-like macro
    params = []
    if not tokmgr.consume_operator('('):
        tokmgr.index = bindex
        return None, None

    # Parse all invocation arguments
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

    # We ended up with mismatched parentheses
    if depth > 0:
        tokmgr.index = bindex
        return None, None

    # Add the last parameter and return
    params.append(tokmgr.tokens[pindex:tokmgr.index])
    return name, params

def substitute(tokmgr: TokenManager, defmap: DefMap, replmap: None = None,
    keys: set[TokenType] | None = None) -> list[TokenType]:
    """
    Consume the tokmgr's next token and, if applicable, substitute it with the
    ANY-form of its relevant definition in defmap. Additionally, register substituted
    tokens in replmap/keys.
    """

    # Each macro is only expanded once, so we track that here
    expansion_stack = []

    # Recursion helper function
    def subst(tokmgr: TokenManager) -> list[TokenType] | None:
        # First, try to parse a macro invocation
        index = tokmgr.index
        name, params = parse_macro(tokmgr, defmap)

        # This isn't a macro
        if name is None:
            return None

        # We've already expanded this one
        if name[1] in expansion_stack:
            tokmgr.index = index
            return None

        # Let's proceed to expand
        substitutions = set()
        if isinstance(keys, set):
            keys.add(name)

        # Find all replacements for this macro and mark it as expanded
        opts = defmap.get_replacements(name, params)
        expansion_stack.append(name[1])

        # Recursively substitute each replacement
        for opt in opts:
            tokens: list[TokenType] = []
            optmgr = TokenManager(opt.tokens)
            while optmgr.has_next():
                tokens += or_else(subst(optmgr), [cast(TokenType, optmgr.next())])
            substitutions.add(DefOption(tokens))

        # We're done here, so we can pop the stack
        expansion_stack.pop()

        # We have more than one possible substitution, so return an ANY-form
        if len(substitutions) > 1:
            return [('any', name[1], substitutions)]

        # We only have one possible substitution, so return it as is
        for substitution in substitutions:
            return substitution.tokens

        # There were no possible substitutions, likely because there were no
        # options, or that this was a wildcard. Return empty.
        return []

    # We've reached EOF, so we won't substitute anything
    if not tokmgr.has_next():
        return []

    # Try to substitute the next token, return it unmodified otherwise
    return or_else(subst(tokmgr), [cast(TokenType, tokmgr.next())])
