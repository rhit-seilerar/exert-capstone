from exert.parser.tokenmanager import TokenManager, tok_seq
from exert.parser.defoption import DefOption
from exert.utilities.types.global_types import TokenType

def substitute(tokmgr: TokenManager, defmap, replmap = None, keys = None):
    def parse_macro(tokmgr: TokenManager):
        bindex = tokmgr.index
        if tokmgr.peek_type() not in ['identifier', 'keyword']:
            return None, []
        name = tokmgr.next()
        assert name is not None
        if not defmap[name[1]].defined:
            tokmgr.index = bindex
            return None, []
        params = []

        # If any options have params, we assert that they all must.
        # Technically this is inaccurate, but we'd have to track multiple
        # token cursors otherwise and it would be horribly impractical.
        hasparams = False
        for opt in defmap[name[1]].options:
            hasparams |= opt.params is not None
            assert hasparams == (opt.params is not None)

        # If this is a function-like macro, parse its arguments
        if hasparams and tokmgr.consume_operator('('):
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
    # Recursively substitute macros with their ANY forms, and track the
    # substitutions in replmap. Each macro will only be expanded once, e.g.
    # '#define ABC ABC' won't infinitely loop.
    def subst(tokmgr: TokenManager):
        index = tokmgr.index
        name, params = parse_macro(tokmgr)
        if name is None or name[1] in expansion_stack or defmap[name[1]].is_initial():
            # This isn't a macro, we've already expanded it, or it's default
            tokmgr.index = index
            return None
        substitutions = set()
        if isinstance(keys, set):
            keys.add(name)
        # Find all replacements that match the macro's invocation
        opts = defmap.get_replacements(name, params)
        if opts == {DefOption([name])}:
            # The macro is solely undefined, so we'll just keep its identifier
            tokmgr.index = index
            return None
        if opts == {DefOption([])}:
            # The macro is solely empty, so replace it with nothing
            return []
        expansion_stack.append(name[1])
        # Recursively substitute each replacement
        for opt in opts:
            tokens: list[TokenType] = []
            optmgr = TokenManager(opt.tokens)
            while optmgr.has_next():
                tokens += subst(optmgr) or [optmgr.next()]
            if tokens:
                substitutions.add(DefOption(tokens))
        expansion_stack.pop()
        macroname = name[1]
        if len(params) > 0:
            macroname += '(' + ', '.join(tok_seq(p) for p in params) + ')'
        # if replmap is not None:
        #     # Map macro name and arguments to a list of possible substitutions
        #     if not name[1] in replmap:
        #         replmap[name[1]] = {}
        #     if not params in replmap[name[1]]:
        #         replmap[name[1]][params] = []
        #     replmap[name[1]][params].append(substitutions)
        if len(substitutions) > 1:
            return [('any', macroname, substitutions)]
        if len(substitutions) == 1:
            return list(substitutions)[0].tokens
        return []

    result = subst(tokmgr)
    return [tokmgr.next()] if result is None else result
