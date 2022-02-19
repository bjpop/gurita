from test.utils import command_output
from pathlib import Path

def test_hist_sepal_length_iris(capsys, tmpdir):
    actual_out_file = Path(tmpdir, "test.hist.sepal_length.iris.png")
    command = f"in data/iris.csv + hist -x sepal_length --format png -o {str(actual_out_file)}"
    expect_out_file = "test/expected/hist_sepal_length_iris.png"
    command_output(capsys, command, out_file=actual_out_file, expect_out_file=expect_out_file)
