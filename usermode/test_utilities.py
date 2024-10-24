from utilities import run_command, get_stdout, get_stderr

def test_run_command_success():
    result = run_command('"echo hi"', True)
    assert result is not None
    assert get_stdout(result).strip() == 'hi'
    assert get_stderr(result) == ''

def test_run_command_fail():
    result = run_command('>', True)
    assert result is not None
    assert get_stdout(result) == ''
    assert get_stderr(result) != ''

def test_get_stdout():
    result = run_command('"echo hi"', True)
    assert get_stdout(result).strip() == 'hi'

def test_get_stderr():
    result = run_command('"cd $"', True)
    assert len(get_stderr(result)) > 0
