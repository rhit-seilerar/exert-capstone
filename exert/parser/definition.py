from typing import Self, Optional
from exert.parser.defoption import DefOption
from exert.utilities.types.global_types import TokenType

class Def:
    """
    This class stores potential values for a single definition. It consists of four states:
    [ !defined, !undefined  {}      ]: The default value, representing definitions that
      haven't been #defined or #undefined yet
    [ !defined,  undefined  {}      ]: This has been explicitly #undefined
    [  defined, !undefined, options ]: This has been explicitly #defined
    [  defined,  undefined, options ]: This was defined in one sub-scope and undefined in another
    """

    def __init__(self, *options: DefOption, defined: bool = False, undefined: bool = False) -> None:
        self.options: set[DefOption] = set()
        self.undefined = undefined
        self.defined = defined
        self.plen: Optional[int] = None
        if len(options) > 0:
            for option in options:
                self.define(option, keep = True)
            self.undefined = undefined

    def validate(self) -> None:
        if self.is_invalid():
            raise ValueError(self.options)

    def copy(self) -> 'Def':
        return Def(*self.options, defined = self.defined, undefined = self.undefined)

    def is_invalid(self) -> bool:
        return not self.defined and len(self.options) > 0

    def is_initial(self) -> bool:
        return not self.undefined and not self.defined

    def is_undefined(self) -> bool:
        return self.undefined and not self.defined

    def is_defined(self) -> bool:
        return not self.undefined and self.defined

    def is_empty_def(self) -> bool:
        return self.defined and len(self.options) == 0

    def is_uncertain(self) -> bool:
        return self.undefined and self.defined

    def undefine(self, keep: bool = True) -> None:
        self.undefined = True
        if not keep:
            self.defined = False
            self.options.clear()

    def define(self, option: Optional[DefOption] = None, keep: bool = True) -> Self:
        if not keep and self.is_undefined():
            self.undefined = False
        if option is not None:
            self.options.add(option)
            if self.plen is None:
                self.plen = -1 if option.params is None else len(option.params)
            else:
                assert self.plen == \
                    (-1 if option.params is None else len(option.params))
        self.defined = True
        return self

    def get_replacements(self, sym: TokenType) -> set[DefOption]:
        """
        [ initial,   {}      ]: [[{}]]
        [ undefined, {}      ]: [[sym]]
        [ defined,   options ]: [options]
        [ defined,   {}      ]: [[{}]]
        [ uncertain, options ]: [[sym], options]
        [ uncertain, {}      ]: [[sym], [{}]]
        """
        replacements: set[DefOption] = set()
        for opt in self.options:
            replacements.add(opt)
        if self.undefined:
            replacements.add(DefOption([sym]))
        if (self.defined or not self.undefined) and len(self.options) == 0:
            macroname = '<empty>' if sym[1] == '<undefined>' else sym[1]
            replacements.add(DefOption([('any', macroname, set())]))
        return replacements

    def combine(self, other: 'Def', replace: bool) -> Self:
        if not isinstance(other, Def):
            raise TypeError(other)
        assert other.plen is None or self.plen is None or other.plen == self.plen
        if replace:
            self.defined = other.defined
            self.undefined = other.undefined
            if not other.is_empty_def():
                self.options = other.options.copy()
        else:
            self.defined |= other.defined
            self.undefined |= other.undefined
            self.options |= other.options
        return self

    def matches(self, other: 'Def') -> bool:
        if not isinstance(other, Def):
            raise TypeError(other)
        if other.is_initial() or self.is_initial():
            return True
        if other.is_undefined():
            if self.is_undefined() or self.is_uncertain():
                return True
        if other.is_empty_def():
            return True
        if len(other.options & self.options) > 0:
            return True
        return False

    def __len__(self) -> int:
        return len(self.options)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Def) \
            and self.defined == other.defined \
            and self.undefined == other.undefined \
            and self.options == other.options

    def __str__(self) -> str:
        if self.is_invalid():
            return '<invalid>'
        if self.is_initial():
            return '<initial>'
        if self.is_undefined():
            return '<undefined>'
        replacements = self.get_replacements(('identifier', '<undefined>'))
        return f'{{ {", ".join(str(r) for r in replacements).strip()} }}'
