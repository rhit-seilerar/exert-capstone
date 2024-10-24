import subprocess
import exert.utilities.command as cmd

def test_run_command_success():
    result = cmd.run_command('echo hi', True)
    assert result is not None
    assert cmd.get_stdout(result).strip() == 'hi'
    assert cmd.get_stderr(result) == ''

def test_run_command_fail():
    result = subprocess.run('>', check = False, shell = True, capture_output = True)
    assert result is not None
    assert cmd.get_stdout(result) == ''
    assert cmd.get_stderr(result) != ''

def test_get_stdout():
    result = cmd.run_command('echo hi', True)
    assert cmd.get_stdout(result).strip() == 'hi'

def test_get_stderr():
    result = subprocess.run('>', check = False, shell = True, capture_output = True)
    assert len(cmd.get_stderr(result)) > 0
