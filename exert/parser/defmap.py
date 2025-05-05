from typing import cast, Self
from exert.parser.defoption import DefOption
from exert.parser.definition import Def
from exert.utilities.types.global_types import TokenType

class DefMap:
    """
    DefMaps represent a possible state of definitions within a macro scope.
    They store a reference to the outer scope's defmap, as well as a set of
    mappings between symbols to their definitions.
    """

    def __init__(self, parent: 'DefMap | None', skipping: bool = False,
        initial: (dict[str, Def] | None) = None):
        assert parent is None or isinstance(parent, DefMap)
        assert initial is None or isinstance(initial, dict)
        self.skipping = skipping
        self.parent = parent
        self.defs = initial or {}
        self.validate()

    def getlocal(self, key: str) -> Def:
        if key not in self.defs:
            self.defs[key] = Def()
        return self.defs[key]

    def __getitem__(self, key: str) -> Def:
        if key in self.defs:
            defn = self.getlocal(key)
            if defn.is_empty_def() and self.parent is not None:
                return Def(
                    *self.parent[key].options,
                    defined = defn.defined,
                    undefined = defn.undefined)
            return defn
        if self.parent is not None:
            return self.parent[key]
        return Def()

    def __setitem__(self, key: str, item: Def) -> None:
        if not isinstance(item, Def):
            raise TypeError(item)
        self.defs[key] = item

    def get_replacements(self, sym_tok: TokenType) -> set[DefOption]:
        return self[cast(str, sym_tok[1])].get_replacements(sym_tok)

    def validate(self) -> None:
        for key in self.defs:
            self[key].validate()

    def undefine(self, key: str) -> None:
        if not self.skipping:
            self.getlocal(key).undefine(keep = False)

    def define(self, key: str, option: DefOption) -> None:
        if not self.skipping:
            self.getlocal(key).define(option, keep = True)

    def combine(self, other: dict[str, Def], replace: bool) -> Self:
        if not isinstance(other, dict):
            raise TypeError(other)
        if not self.skipping:
            for key in other:
                self[key] = self[key].copy().combine(other[key], replace = replace)
        return self

    def matches(self, conditions: object) -> bool:
        if not isinstance(conditions, DefMap):
            raise TypeError(conditions)
        for key in conditions.defs:
            if not self[key].matches(conditions[key]):
                return False
        return True

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DefMap) \
            and self.parent == other.parent \
            and self.skipping == other.skipping \
            and self.defs == other.defs

    def __str__(self) -> str:
        defs_strs = [f"'{key}': {str(self.defs[key])}" for key in self.defs]
        return f'DefMap(parent = {self.parent}, skipping = {self.skipping}, ' \
            f'defs = {{{", ".join(defs_strs)}}})'
