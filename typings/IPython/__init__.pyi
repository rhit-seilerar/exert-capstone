from .terminal.embed import embed as embed
from _typeshed import Incomplete

__all__ = ['start_ipython', 'embed', 'embed_kernel']

def embed_kernel(module: Incomplete | None = None, local_ns: Incomplete | None = None, **kwargs) -> None: ...
def start_ipython(argv: Incomplete | None = None, **kwargs): ...
