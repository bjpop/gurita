from hatch.hatch import main_args
import pytest
from filecmp import cmp


# Test a command and optionally compare its output file, stdout, stderr and exit status to expected values
def command_output(capsys, cmd, out_file=None, expect_out_file=None, stdout="", stderr="", exit=0):
    command_fields = cmd.split()

    with pytest.raises(SystemExit) as e:
        main_args(command_fields)

    if capsys is not None:
        captured = capsys.readouterr()
        assert captured.out == stdout 
        assert captured.err == stderr 
        assert e.type == SystemExit
        assert e.value.code == exit 

    if out_file is not None and expect_out_file is not None:
        assert cmp(out_file, expect_out_file, shallow=False)

