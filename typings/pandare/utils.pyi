from os import dup as dup, getenv as getenv, path as path
from pandare.pyplugin import PyPlugin

debug: bool

class GArrayIterator:
    current_idx: int
    def __del__(self) -> None: ...
