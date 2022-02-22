import test.utils
from pathlib import Path

def test_hist_sepal_length_iris(capsys, tmpdir):
    actual_out_file = Path(tmpdir, "test.hist.sepal_length.iris.svg")
    command = f"in data/iris.csv + hist -x sepal_length --format svg -o {str(actual_out_file)}"
    expect_out_file = "test/expected/hist_sepal_length_iris.svg"
    test.utils.command_output(capsys, command, out_file=actual_out_file, expect_out_file=expect_out_file)
