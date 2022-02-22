import test.utils

def test_help_short(capsys, tmpdir):
    with open("test/expected/help.stdout") as expected_file:
       stdout = expected_file.read()
    test.utils.command_output(capsys, "-h", stdout=stdout)

def test_help_long(capsys, tmpdir):
    with open("test/expected/help.stdout") as expected_file:
       stdout = expected_file.read()
    test.utils.command_output(capsys, "--help", stdout=stdout)
