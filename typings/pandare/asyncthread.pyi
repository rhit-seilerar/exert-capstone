from _typeshed import Incomplete
from pandare.utils import debug as debug

# def progress(msg) -> None: ...

class AsyncThread:
    running: bool
    panda_started: Incomplete
    task_queue: Incomplete
    athread: Incomplete
    warned: bool
    ending: bool
    empty_at: Incomplete
    last_called: Incomplete
    def stop(self) -> None: ...

def test1() -> None: ...
def test2() -> None: ...
def test3() -> None: ...
