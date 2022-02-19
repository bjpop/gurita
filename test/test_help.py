import test.utils

def test_help_short(capsys):
    with open("test/expected/help.stdout") as expected_file:
       expected_stdout = expected_file.read()
    test.utils.command_stdout_stderr(capsys, "-h", expected_stdout)

def test_help_long(capsys):
    with open("test/expected/help.stdout") as expected_file:
       expected_stdout = expected_file.read()
    test.utils.command_stdout_stderr(capsys, "--help", expected_stdout)
