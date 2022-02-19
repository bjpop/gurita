from hatch.hatch import main_args
import pytest


# Test a command and compare its stdout, stderr and exit status to expected values
def command_stdout_stderr(capsys, command, expected_stdout="", expected_stderr="", expected_exit_status=0):
    command_fields = command.split()

    with pytest.raises(SystemExit) as e:
        main_args(command_fields)

    captured = capsys.readouterr()
    assert captured.out == expected_stdout
    assert captured.err == expected_stderr
    assert e.type == SystemExit
    assert e.value.code == expected_exit_status 
