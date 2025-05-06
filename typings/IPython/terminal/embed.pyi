from IPython.core import compilerop as compilerop, magic_arguments as magic_arguments, ultratb as ultratb
from IPython.core.interactiveshell import InteractiveShell as InteractiveShell
from IPython.core.magic import Magics as Magics, line_magic as line_magic, magics_class as magics_class
from IPython.terminal.interactiveshell import TerminalInteractiveShell as TerminalInteractiveShell
from IPython.terminal.ipapp import load_default_config as load_default_config
from IPython.utils.io import ask_yes_no as ask_yes_no
from typing import Any

class KillEmbedded(Exception): ...
KillEmbeded = KillEmbedded

class EmbeddedMagics(Magics):
    def kill_embedded(self, parameter_s: str = '') -> None: ...
    def exit_raise(self, parameter_s: str = '') -> None: ...

def embed(*, header: str = '', compile_flags: Any | None = None, **kwargs: Any) -> None: ...
