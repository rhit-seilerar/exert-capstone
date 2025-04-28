from exert.parser.tokenmanager import tok_seq
from exert.utilities.types.global_types import TokenType

class DefOption:
    """
    DefOption represents a single replacement option for a macro. It's immutable,
    which is useful for hashing to guarantee uniqueness in a set.
    Each DefOption has a set of tokens, which is the replacement's unsubstituted
    form, as well as a list of parameter names. During replacement, these
    parameter names are replaced with other token lists, which then constructs
    the substituted form.
    """
    def __init__(self, tokens: list[TokenType], params: (list[str] | None) = None):
        assert isinstance(tokens, list)
        self.tokens = tokens
        self.params = params
        self.paramstr = '' if params is None else ','.join(params)
        self.key = tok_seq(tokens)
        if self.paramstr:
            self.key = self.paramstr + '$' + self.key
        self.len = len(tokens)
        self.hash = hash(self.key)

    # def withParams(self, params: list[list[TokenType]]) -> list[TokenType]:
    #     """
    #     If this is a function-like macro, substitute params with the provided
    #     token lists. Otherwise, return this option's replacement list.
    #     """
    #     if self.params is None:
    #         return self.tokens
    #     assert len(params) == len(self.params)
    #     idtypes = ['identifier', 'keyword']
    #     pparams = { p: params[i] for i, p in enumerate(self.params) }
    #     return [ts for t in self.tokens for ts in \
    #         (pparams.get(t[1], [t]) if t[0] in idtypes else [t])]

    def __eq__(self, other):
        return isinstance(other, DefOption) and other.key == self.key

    def __hash__(self):
        return self.hash

    def __len__(self):
        return self.len

    def __str__(self):
        return self.key
