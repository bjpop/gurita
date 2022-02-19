from hatch.utils import cm_to_inches
import pytest

def test_cm_to_inches_zero():
    result = cm_to_inches(0)
    assert result == 0

def test_cm_to_inches_zero():
    result = cm_to_inches(1)
    assert result == pytest.approx(0.393701)

def test_cm_to_inches_negative():
    result = cm_to_inches(-1)
    assert result == pytest.approx(-0.393701)
