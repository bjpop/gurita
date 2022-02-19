from test.utils import command_output

def test_pretty_iris(capsys, tmpdir):
    with open("test/expected/pretty_iris.stdout") as expected_file:
       stdout = expected_file.read()
    command_output(capsys, "in data/iris.csv + pretty", stdout=stdout)
