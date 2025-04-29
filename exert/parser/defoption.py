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
        self.paramstr = '' if params is None else '(' + ','.join(params) + ')'
        self.key = self.paramstr + '$' + tok_seq(tokens)
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
