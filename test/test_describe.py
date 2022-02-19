import test.utils

# NOTE, the describe command can be nondeterministic in its output
# with respect to the top feature identified in the input file.
# In this case we test with an input file ("titanic.csv") known to always
# give the same result each time.

def test_describe_titanic(capsys):
    with open("test/expected/describe_titanic.stdout") as expected_file:
       expected_stdout = expected_file.read()
    test.utils.command_stdout_stderr(capsys, "in data/titanic.csv + describe", expected_stdout)
