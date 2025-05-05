from typing import Optional, cast
from exert.parser.tokenmanager import TokenManager, is_id_or_kw
from exert.parser.defoption import DefOption
from exert.parser.defmap import DefMap
from exert.utilities.logic import OrElse
from exert.utilities.types.global_types import TokenType, TokenSeq

def parse_macro(tokmgr: TokenManager, defmap: DefMap) \
    -> tuple[Optional[TokenType], Optional[list[TokenSeq]]]:
    """
    Consume macro application syntax, e.g. an identifier for a variable-like
    macro and name(p1, p2, ...) for a function-like macro. Note that, for
    simplicity, all options for a definition must be either variable-like,
    or function-like with the same number of arguments.
    """

    # Back up the index in case of failure
    bindex = tokmgr.index

    # We only substitute identifiers or keywords
    name = tokmgr.next()
    if not name or not is_id_or_kw(name):
        return None, None

    # If the identifier isn't defined, we won't touch it
    defn = defmap[cast(str, name[1])]
    if not defn.defined or defn.is_empty_def():
        tokmgr.index = bindex
        return None, None

    # This is a variable-like macro, so just return the name
    plen = OrElse[int]()(defn.plen, -1)
    if plen == -1:
        return name, None

    # This is a function-like macro
    params: list[TokenSeq] = []
    if not tokmgr.consume_operator('('):
        tokmgr.index = bindex
        return None, None

    # Don't try to parse unless there's at least one param
    if not tokmgr.consume_operator(')'):
        # Parse all invocation arguments
        depth = 1
        pindex = tokmgr.index
        while tokmgr.has_next() and depth > 0:
            # Handle nested parentheses
            if tokmgr.consume_operator('('):
                depth += 1
            elif tokmgr.consume_operator(')'):
                depth -= 1
            # If we're at the base paren level and haven't reached the last param, add another.
            # This handles varargs by just treating everything at the last param and past as
            # one big param.
            elif tokmgr.consume_operator(',') and depth == 1 and len(params) < plen-1:
                params.append(tokmgr.tokens[pindex:tokmgr.index-1])
                pindex = tokmgr.index
            # Otherwise, increment and continue
            else:
                tokmgr.bump()

        # Add the last parameter
        params.append(tokmgr.tokens[pindex:tokmgr.index-1])

        # We ended up with mismatched parentheses
        if depth > 0:
            tokmgr.index = bindex
            return None, None

    # We had fewer params. That's a problem, so return none
    elif len(params) < plen:
        tokmgr.index = bindex
        return None, None

    # Everything else checks out, return the result
    return name, params

KeysType = Optional[set[TokenType]]

def subst_all(tokmgr: TokenManager, defmap: DefMap, keys: KeysType,
    expansion_stack: TokenSeq) -> TokenSeq:

    # For each token in tokmgr, try to substitute it and return the result
    result: TokenSeq = []
    while tokmgr.has_next():
        res = subst(tokmgr, defmap, keys, expansion_stack)
        if res is None:
            res = cast(TokenSeq, [tokmgr.next()])
        result += res

    return result

# Recursion helper function
def subst(tokmgr: TokenManager, defmap: DefMap, keys: KeysType,
    expansion_stack: TokenSeq) -> Optional[TokenSeq]:

    # First, try to parse a macro invocation
    index = tokmgr.index
    name, params = parse_macro(tokmgr, defmap)

    # If this is a macro, add it to the keys set
    macroname = OrElse[TokenType]()(name, cast(TokenType, tokmgr.peek()))
    if isinstance(keys, set) and is_id_or_kw(macroname) \
        and not defmap[cast(str, macroname[1])].is_initial():
        keys.add(macroname)

    # This isn't a macro, or it doesn't have any options
    if name is None:
        tokmgr.index = index
        return None

    # We've already expanded this one
    if name in expansion_stack:
        tokmgr.index = index
        return None

    # Let's proceed to expand
    substitutions: set[DefOption] = set()
    expansion_stack.append(name)

    # If we have any parameters, substitute them first
    if params is not None:
        params = [subst_all(TokenManager(p), defmap, keys, expansion_stack) \
            for p in params]

    # Find all replacements for this macro
    opts = defmap.get_replacements(name)

    # Recursively substitute each replacement
    for opt in opts:
        tokens: TokenSeq = []
        optmgr = TokenManager(opt.tokens)
        while optmgr.has_next():
            # Replace parameters if necessary
            nex = cast(TokenSeq, [optmgr.next()])
            if opt.params is not None and nex[0][0] in ['identifier', 'keyword']:
                opttok_name: str = cast(str, nex[0][1])
                if opttok_name in opt.params:
                    nex = (params or [])[opt.params.index(opttok_name)]

            # Substitute the replacement
            tokens += subst_all(TokenManager(nex), defmap, keys, expansion_stack)

        substitutions.add(DefOption(tokens))

    # We're done here, so we can pop the stack
    expansion_stack.pop()

    # We have more than one possible substitution, so return an ANY-form
    if len(substitutions) > 1:
        return [('any', name[1], substitutions)]

    # We only have one possible substitution, so return it as is.
    result: Optional[TokenSeq] = None
    for substitution in substitutions:
        result = substitution.tokens
    return result

def substitute(tokmgr: TokenManager, defmap: DefMap,
    keys: Optional[set[TokenType]] = None) -> TokenSeq:
    """
    Consume the tokmgr's next token and, if applicable, substitute it with the
    ANY-form of its relevant definition in defmap. Additionally, register substituted
    tokens in replmap/keys.
    """

    # We've reached EOF, so we won't substitute anything
    if not tokmgr.has_next():
        return []

    # Try to substitute the next token, return it unmodified otherwise
    return OrElse[TokenSeq]()(subst(tokmgr, defmap, keys, []),
        lambda: cast(TokenSeq, [tokmgr.next()]))
