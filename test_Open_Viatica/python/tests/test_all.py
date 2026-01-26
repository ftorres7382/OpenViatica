import pytest
import test_Open_Viatica


def test_sum_as_string():
    assert test_Open_Viatica.sum_as_string(1, 1) == "2"
