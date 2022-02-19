import test.utils

def test_pretty_iris(capsys):
    with open("test/expected/pretty_iris.stdout") as expected_file:
       expected_stdout = expected_file.read()
    test.utils.command_stdout_stderr(capsys, "in data/iris.csv + pretty", expected_stdout)
