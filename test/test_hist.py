import test.utils
from pathlib import Path


def test_hist_sepal_length_iris_png(capsys, tmpdir):
    Path("test/outputs").mkdir(parents=True, exist_ok=True)
    actual_out_file = Path("test/outputs", "test.hist.sepal_length.iris.png")
    command = f"in data/iris.csv + hist -x sepal_length --format png -o {str(actual_out_file)}"

    # Test that the command executes successfully without comparing binary image output 
    # to avoid fragility across different environment renderers or matplotlib versions (#52)
    test.utils.command_output(capsys, command, out_file=actual_out_file)

def test_hist_sepal_length_iris_svg(capsys, tmpdir):
    Path("test/outputs").mkdir(parents=True, exist_ok=True)
    actual_out_file = Path("test/outputs", "test.hist.sepal_length.iris.svg")
    command = f"in data/iris.csv + hist -x sepal_length --format svg -o {str(actual_out_file)}"

    # Test that the command executes successfully without comparing binary image output 
    # to avoid fragility across different environment renderers or matplotlib versions (#52)
    test.utils.command_output(capsys, command, out_file=actual_out_file)