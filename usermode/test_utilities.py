from utilities import run_command, run_commands, get_stdout, get_stderr

def test_run_command_success():
    result = run_command('echo hi', True)
    assert result is not None
    assert get_stdout(result) == 'hi\n'
    assert get_stderr(result) == ''

def test_run_command_fail():
    result = run_command('>', True)
    assert result is not None
    assert get_stdout(result) == ''
    assert get_stderr(result) != ''

def test_run_commands_one():
    result = run_command(['echo hi'], True)
    assert get_stdout(result) == 'hi\n'
    assert get_stderr(result) == ''

def test_run_commands_multiple():
    result = run_commands(['echo hi', 'echo bye'], True)
    assert get_stdout(result) == 'hi\nbye\n'
    assert get_stderr(result) == ''

def test_get_stdout():
    result = run_command('echo hi', True)
    assert get_stdout(result) == 'hi\n'

def test_get_stderr():
    result = run_command('cd $', True)
    assert len(get_stderr(result)) > 0
