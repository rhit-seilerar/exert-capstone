from typing import Optional
from exert.utilities.logic import OrElse

OR_ELSE_COUNTER: int = 0
def or_else_helper() -> str:
    global OR_ELSE_COUNTER
    OR_ELSE_COUNTER = 1
    return 'Whoops!'

def test_or_else_value() -> None:
    assert OrElse[str]()('123', 'Whoops!') == '123'

def test_or_else_value_lambda_not_called() -> None:
    global OR_ELSE_COUNTER
    OR_ELSE_COUNTER = 0
    assert OrElse[str]()('123', or_else_helper) == '123'
    assert OR_ELSE_COUNTER == 0

def test_or_else_default_value() -> None:
    assert OrElse[str]()(None, 'Whoops!') == 'Whoops!'

def test_or_else_default_lambda() -> None:
    global OR_ELSE_COUNTER
    OR_ELSE_COUNTER = 0
    val: Optional[str] = None
    assert OrElse[str]()(val, or_else_helper) == 'Whoops!'
    assert OR_ELSE_COUNTER == 1
