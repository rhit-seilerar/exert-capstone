from pandare.utils import debug as debug

class AsyncThread:
    running: bool
    warned: bool
    ending: bool
    def stop(self) -> None: ...

def test1() -> None: ...
def test2() -> None: ...
def test3() -> None: ...
